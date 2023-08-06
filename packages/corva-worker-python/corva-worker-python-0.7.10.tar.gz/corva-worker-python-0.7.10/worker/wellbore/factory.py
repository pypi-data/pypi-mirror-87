from typing import Union

from worker.data.operations import get_data_by_path, get_drillstring_by_id

from worker import API
from worker.exceptions import MissingConfigError

from worker.wellbore.model.drillstring import Drillstring
from worker.wellbore.model.enums import HoleType
from worker.wellbore.model.hole import Hole
from worker.wellbore.model.hole_section import HoleSection
from worker.wellbore.wellbore import Wellbore


def set_drillstring_and_create_wellbore(wits: dict) -> Union[Wellbore, None]:
    """
    Get the wits record and create a wellbore
    :param wits: wits records in json format
    :return: a wellbore
    """
    if wits is None:
        return None

    api_worker = API()

    drillstring_id = get_data_by_path(wits, "metadata.drillstring", str)

    if not drillstring_id:
        return None

    drillstring = get_drillstring_by_id(drillstring_id)

    if not drillstring:
        return None
    active_drillstring_number = drillstring.get("data", {}).get("id")

    # setting active drillstring
    drillstring = Drillstring(drillstring)

    bit = drillstring.get_bit()
    if not bit:
        raise MissingConfigError(f"Bit was not found in the drillstring with _id='{drillstring_id}'")

    asset_id = wits['asset_id']
    bit_size = bit.size

    bit_depth = get_data_by_path(wits, "data.bit_depth", float)
    hole_depth = get_data_by_path(wits, "data.hole_depth", float)

    # setting cased-hole sections
    query = "{data.inner_diameter#gte#%s}" % bit_size
    casings = api_worker.get(
        path="/v1/data/corva", collection="data.casing", asset_id=asset_id, query=query, limit=100
    ).data

    hole = Hole()
    hole.set_casings(casings)
    smallest_cased_hole_diameter = hole.get_min_inner_diameter() or 100

    # ====== setting open-hole sections
    query = "{data.id#lte#%s}" % active_drillstring_number
    sort = "{data.id:1}"
    drillstrings = api_worker.get(
        path="/v1/data/corva", collection="data.drillstring", asset_id=asset_id, query=query, sort=sort, limit=100
    ).data

    # setting open-hole sections
    for ds in drillstrings:
        bit = Drillstring(ds).get_bit()
        if not bit:
            drillstring_id = ds.get("_id")
            raise MissingConfigError(f"Bit was not found in the drillstring with _id='{drillstring_id}'")

        bit_size = bit.size
        # only keeping the DSs that ran below the smallest casing
        if bit_size > smallest_cased_hole_diameter:
            continue

        start_depth = ds.get("data", {}).get("start_depth")

        # if due to the side track the hole depth reduced, then it should update the setting depths in the open hole
        hole.sections = [
            sec for sec in hole.sections
            if sec.hole_type != HoleType.OPEN_HOLE or sec.top_depth <= hole_depth
        ]

        # if a new open-hole section is created in addition to the previous one,
        # the previous bottom depth may need to be modified.
        previous_hole_section = hole.get_last_hole_section()

        top_depth = hole.get_bottom_depth()
        bottom_depth = top_depth + 0.0001
        current_hole_section = HoleSection(
            top_depth=top_depth,
            bottom_depth=bottom_depth,
            inner_diameter=bit_size,
            hole_type=HoleType.OPEN_HOLE
        )

        is_equal_previous_section = False
        if previous_hole_section:
            # The casing bottom depth can't be modified if the difference is more than 300 ft
            cased_hole_condition = previous_hole_section.hole_type == HoleType.CASED_HOLE and start_depth - previous_hole_section.bottom_depth < 300
            if cased_hole_condition or previous_hole_section.hole_type == HoleType.OPEN_HOLE:
                previous_hole_section.set_bottom_depth(start_depth)
                previous_hole_section.set_length()

            is_equal_previous_section = current_hole_section.eq_without_length(previous_hole_section)

        if is_equal_previous_section:
            continue

        current_hole_section.set_length()
        hole.add_section(current_hole_section)

    # In some cases the DS setting depth doesn't match the hole depth so the wits data overrides it;
    # this is only applied to the top depth of the last section and bottom depth of the previous section.
    # Note: only in cases that the wits hole_depth < setting depth
    # Condition: the number of open hole sections should be at least two needs to be satisfied first
    if len(hole) - len(hole.get_cased_hole()) > 1 and 1 < hole_depth < hole[-1].top_depth:
        hole[-2].set_bottom_depth(hole_depth)
        hole[-2].set_length()

        hole[-1].set_top_depth(hole_depth)
        hole[-1].set_length()

    return Wellbore(
        drillstring=drillstring,
        hole=hole,
        bit_depth=bit_depth,
        hole_depth=hole_depth,
    )
