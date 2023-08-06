from copy import deepcopy
from typing import Union

from worker.data.operations import get_data_by_path, nanround

from worker.data.serialization import serialization
from worker.wellbore.model.annulus import Annulus
from worker.wellbore.model.drillstring import Drillstring
from worker.wellbore.model.hole import Hole


@serialization
class Wellbore:
    SERIALIZED_VARIABLES = {
        'original_drillstring': Drillstring,
        'original_hole': Hole,
        'bit_depth': float,
        'hole_depth': float,
        'last_hole_depth': float,
        'last_non_decreasing_hole_depth': float,
    }

    def __init__(self, **kwargs):
        super().__init__()

        self.original_drillstring: Drillstring = kwargs.get('original_drillstring') or kwargs.get('drillstring')
        self.actual_drillstring: Drillstring = kwargs.get('actual_drillstring')

        self.original_hole: Hole = kwargs.get('original_hole') or kwargs.get('hole')
        self.actual_hole: Hole = kwargs.get('actual_hole')

        self.actual_annulus: Annulus = kwargs.get('actual_annulus')

        self.bit_depth: float = kwargs.get('bit_depth') or 0.0
        self.hole_depth: float = kwargs.get('hole_depth')

        self.last_hole_depth: float = kwargs.get('last_hole_depth') or self.hole_depth
        self.last_non_decreasing_hole_depth: float = kwargs.get('last_non_decreasing_hole_depth') or self.last_hole_depth

        self.update()

    @property
    def annulus(self):
        return self.actual_annulus

    def update(self, bit_depth: Union[float, dict] = None, hole_depth: float = None) -> None:
        """

        :param bit_depth: a wits dict (that will be used for both bit and hole depths) or actual bit depth
        :param hole_depth: actual hole depth value
        :return:
        """
        if self.original_drillstring is None:
            return

        if isinstance(bit_depth, dict):
            bit_depth = get_data_by_path(bit_depth, "data.bit_depth", float)
            hole_depth = get_data_by_path(bit_depth, "data.hole_depth", float)

        self.bit_depth = bit_depth or self.bit_depth or 0.0

        # a qc for the hole depth: if bit depth > hole depth override it with bit depth
        if hole_depth is None:
            hole_depth = self.hole_depth or self.original_hole.get_bottom_depth()
        hole_depth = max(hole_depth, self.bit_depth)
        self.hole_depth = hole_depth

        self.actual_drillstring = deepcopy(self.original_drillstring)
        self.actual_drillstring.update(self.bit_depth)

        self.last_non_decreasing_hole_depth = max(self.last_non_decreasing_hole_depth, self.hole_depth)

        if self.hole_depth > self.last_hole_depth and self.last_hole_depth <= self.last_non_decreasing_hole_depth <= self.hole_depth:
            self.actual_hole = deepcopy(self.original_hole)

        self.actual_hole = deepcopy(self.original_hole)
        self.actual_hole.update(self.hole_depth)

        self.actual_annulus = Annulus(drillstring=self.actual_drillstring, hole=self.actual_hole)

        self.last_hole_depth = self.hole_depth

    def update_casing(self, casings: Hole) -> None:
        """
        If there is any update in the casings
        :param casings:
        :return:
        """
        self.original_hole.update_casings(casings)
        self.actual_hole.update_casings(casings)
        self.update()

    def trim_after_hole_depth_reduction(self, hole_depth: float) -> None:
        self.last_non_decreasing_hole_depth = hole_depth
        self.original_hole = deepcopy(self.actual_hole)

        self.actual_hole.sections = [sec for sec in self.actual_hole.sections if sec.top_depth <= hole_depth]
        if self.actual_hole:
            self.actual_hole[-1].bottom_depth = hole_depth
            self.actual_hole[-1].set_length()

        self.update(hole_depth, hole_depth)

    def compute_get_drillstring_body_volume_change(self, from_bit_depth: float, to_bit_depth: float) -> float:
        """
        Compute the change in the drillstring body volume between two bit depths
        :param from_bit_depth: start bit depth
        :param to_bit_depth: end bit depth
        :return: volume in FOOT^3
        """
        ds_from = deepcopy(self.original_drillstring)
        ds_from.update(from_bit_depth)
        body_volume_from = ds_from.compute_get_body_volume()

        ds_to = deepcopy(self.original_drillstring)
        ds_to.update(to_bit_depth)
        body_volume_to = ds_to.compute_get_body_volume()

        return body_volume_to - body_volume_from

    def compute_get_drillstring_outside_volume_change(self, from_bit_depth: float, to_bit_depth: float) -> float:
        """
        Compute the change in the drillstring solid volume between two bit depths using OD
        :param from_bit_depth: start bit depth
        :param to_bit_depth: end bit depth
        :return: volume in FOOT^3
        """
        ds_from = deepcopy(self.original_drillstring)
        ds_from.update(from_bit_depth)
        outside_volume_from = ds_from.compute_get_outside_volume()

        ds_to = deepcopy(self.original_drillstring)
        ds_to.update(to_bit_depth)
        outside_volume_to = ds_to.compute_get_outside_volume()

        return outside_volume_to - outside_volume_from

    def __repr__(self):
        return f"Wellbore:\n" \
               f"===Bit Depth / Hole Depth = {nanround(self.bit_depth)} / {nanround(self.hole_depth)}\n" \
               f"===Drillstring:\n{self.actual_drillstring}\n" \
               f"===Hole:\n{self.actual_hole}\n" \
               f"===Annulus:\n{self.actual_annulus}\n\n" \
               f"===Given Drillstring:\n{self.actual_drillstring}\n"
