import os
import unittest

from worker.data.operations import get_data_by_path, get_one_data_record
from worker.data.serialization import obj2json, json2obj
from worker.test.utils import file_to_json
from worker.wellbore.factory import set_drillstring_and_create_wellbore
from worker.wellbore.measured_depth_finder import get_unique_measured_depths
from worker.wellbore.model.annulus import Annulus
from worker.wellbore.model.drillstring import Drillstring
from worker.wellbore.model.enums import HoleType, PipeType
from worker.wellbore.model.hole import Hole
from worker.wellbore.model.hole_section import HoleSection


class TestSections(unittest.TestCase):
    def test_hole_section(self):
        hole_section1 = HoleSection(inner_diameter=5, top_depth=0, bottom_depth=20_000, hole_type=HoleType.OPEN_HOLE)

        hole_section1.set_length()

        self.assertEqual(20_000, hole_section1.length)

        expected_area = 19.634954084936208  # in INCH^2
        expected_volume = 2727.07695624114  # in FOOT^3

        self.assertAlmostEqual(expected_area, hole_section1.compute_get_area(), places=10)
        self.assertAlmostEqual(expected_volume, hole_section1.compute_get_volume(), places=10)

    def test_hole(self):
        casings = os.path.abspath(
            os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources", "test", "casings.json")
        )
        casings = file_to_json(casings)

        hole = Hole()
        hole.set_casings(casings)
        self.assertEqual(2, len(hole))

        hole_section1 = hole[0]
        self.assertAlmostEqual(6.88, hole_section1.inner_diameter, 10)
        self.assertAlmostEqual(6_770, hole_section1.length, 10)
        self.assertAlmostEqual(0, hole_section1.top_depth, 10)
        self.assertAlmostEqual(6_770, hole_section1.bottom_depth, 10)
        self.assertEqual(HoleType.CASED_HOLE, hole_section1.hole_type)

        hole_section2 = hole[1]
        self.assertAlmostEqual(4.67, hole_section2.inner_diameter, 10)
        self.assertAlmostEqual(14192, hole_section2.length, 10)
        self.assertAlmostEqual(6_770, hole_section2.top_depth, 10)
        self.assertAlmostEqual(20_962, hole_section2.bottom_depth, 10)
        self.assertEqual(HoleType.CASED_HOLE, hole_section2.hole_type)

        self.assertAlmostEqual(20_962, hole.get_bottom_depth(), 10)

        # Open hole
        open_hole = HoleSection(inner_diameter=4.5, top_depth=1111, bottom_depth=21_000, hole_type=HoleType.OPEN_HOLE)
        hole.add_section(open_hole)
        hole_section3 = hole[2]
        self.assertAlmostEqual(4.5, hole_section3.inner_diameter, 10)
        self.assertAlmostEqual(21_000 - 20_962, hole_section3.length, 10)
        self.assertAlmostEqual(20_962, hole_section3.top_depth, 10)
        self.assertAlmostEqual(21_000, hole_section3.bottom_depth, 10)
        self.assertEqual(HoleType.OPEN_HOLE, hole_section3.hole_type)

        self.assertAlmostEqual(21_000, hole.get_bottom_depth(), 10)

        # test fetching of the correct casing at a given depth
        casing1 = hole.find_section_at_measured_depth(10_000, False)
        self.assertEqual(id(hole_section2), id(casing1))

        # testing unique boundary depths
        mds = get_unique_measured_depths(hole)
        self.assertListEqual(mds, [0, 6770.0, 20962.0, 21000.0])

        # test serialization
        ser_str = obj2json(hole)
        hole_des = json2obj(ser_str)
        self.assertEqual(len(hole), len(hole_des))
        self.assertAlmostEqual(hole_des[1].inner_diameter, hole[1].inner_diameter, 10)
        self.assertAlmostEqual(hole_des[1].top_depth, hole[1].top_depth, 10)

        print("Hole:")
        print(hole)
        return hole

    def test_drillstring(self):
        drillstring_json_file = os.path.abspath(
            os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources", "test", "drillstring.json")
        )
        drillstring_json = file_to_json(drillstring_json_file)

        drillstring = Drillstring()
        drillstring.set_drillstring(drillstring_json)

        component_1 = drillstring[0]
        self.assertAlmostEqual(3.826, component_1.inner_diameter, 10)
        self.assertAlmostEqual(4.5, component_1.outer_diameter, 10)
        self.assertAlmostEqual(31, component_1.joint_length, 10)
        self.assertAlmostEqual(31, component_1.length, 10)

        component_6 = drillstring[5]
        self.assertAlmostEqual(2.75, component_6.inner_diameter, 10)
        self.assertAlmostEqual(4.75, component_6.outer_diameter, 10)
        self.assertAlmostEqual(29.09, component_6.joint_length, 10)
        self.assertAlmostEqual(29.09, component_6.length, 10)

        bit = drillstring[-1]
        self.assertAlmostEqual(6.75, bit.size, 10)
        self.assertAlmostEqual(1.1780972450961724, bit.tfa, 10)
        self.assertEqual(PipeType.BIT.value, bit.pipe_type.value, 10)

        # test for adjusting depths using bit depth
        wits = get_wits()
        drillstring.update(wits)
        self.assertAlmostEqual(wits.get('data', {}).get('bit_depth'), drillstring[-1].bottom_depth, 10)

        # test for finding drillstring section at a measured depth
        drillstring_section3 = drillstring.find_section_at_measured_depth(8_000, False)
        self.assertAlmostEqual(3.83, drillstring_section3.inner_diameter, 1)
        self.assertAlmostEqual(4.5, drillstring_section3.outer_diameter, 10)

        print("Drillstring")
        print(drillstring)
        return drillstring

    def test_annulus(self):
        drillstring = self.test_drillstring()
        hole = self.test_hole()
        annulus = Annulus(drillstring=drillstring, hole=hole)
        print("Annulus:")
        print(annulus)

        # 2nd DP should be split into two segments
        section2, section3 = annulus[2: 4]
        self.assertAlmostEqual(6.88, section2.inner_diameter_hole, 10)
        self.assertEqual(HoleType.CASED_HOLE, section2.hole_type)
        self.assertAlmostEqual(4.67, section3.inner_diameter_hole, 10)
        self.assertEqual(HoleType.CASED_HOLE, section3.hole_type)

        # the segment above the is extended to the bit depth
        last_section = annulus[-1]

        component_above_bit, bit = drillstring[-2:]
        combined_length = component_above_bit.length + bit.length

        self.assertAlmostEqual(combined_length, last_section.length, 10)

    def test_wellbore_creation_with_factory(self):
        """
        In this test case the creation of the wellbore through
        factory is shown; note that only the wits record is used
        and the other elements (casings, drillstrings) are fetched
        from the API.
        :return:
        """
        wits = get_wits()
        bit_depth = get_data_by_path(wits, 'data.bit_depth', float)
        hole_depth = get_data_by_path(wits, 'data.hole_depth', float)
        wellbore = set_drillstring_and_create_wellbore(wits)

        print("\n Hole configuration is:")
        hole = wellbore.actual_hole
        print(hole)
        self.assertEqual(2, len(hole))
        self.assertEqual(HoleType.CASED_HOLE, hole[0].hole_type)
        self.assertEqual(HoleType.OPEN_HOLE, hole[1].hole_type)
        self.assertAlmostEqual(hole_depth, hole.get_bottom_depth(), 10)

        print("\n Drillstring configuration is:")
        drillstring = wellbore.actual_drillstring
        self.assertAlmostEqual(bit_depth, drillstring.bit_depth, 10)
        print(drillstring)

        print("\n Annulus configuration is:")
        annulus = wellbore.actual_annulus
        print(annulus)

        # testing drilling body volume change
        vol_change_calculated = wellbore.compute_get_drillstring_body_volume_change(6000, 5900)
        area_dp = wellbore.actual_drillstring[0].compute_body_cross_sectional_area_tj_adjusted()  # in INCH^2
        vol_expected = area_dp / 144 * -100
        self.assertAlmostEqual(vol_change_calculated, vol_expected, 10)

        # testing drilling outer solid volume change
        vol_change_calculated = wellbore.compute_get_drillstring_outside_volume_change(6000, 5900)
        area_dp = wellbore.actual_drillstring[0].compute_outer_area_tool_joint_adjusted()  # in INCH^2
        vol_expected = area_dp / 144 * -100
        self.assertAlmostEqual(vol_change_calculated, vol_expected, 10)

        # test serialization
        ser_str = obj2json(wellbore)
        wellbore_des = json2obj(ser_str)
        self.assertEqual(len(wellbore.actual_drillstring), len(wellbore_des.actual_drillstring))
        self.assertAlmostEqual(wellbore.actual_drillstring[1].inner_diameter, wellbore_des.actual_drillstring[1].inner_diameter, 10)
        self.assertAlmostEqual(wellbore.actual_drillstring[1].top_depth, wellbore_des.actual_drillstring[1].top_depth, 10)

    def test_overlapping_liners(self):
        """
        In this test case we are checking if the casings and liners
        are set correctly even if the there are overlapping liners.
        :return:
        """

        wits = get_one_data_record(asset_id=3083, collection="wits")
        wellbore = set_drillstring_and_create_wellbore(wits)

        hole: Hole = wellbore.actual_hole
        hole_depth = 25633.01

        self.assertEqual(3, len(hole))

        self.assertEqual(HoleType.CASED_HOLE, hole[0].hole_type)
        self.assertAlmostEqual(0.0, hole[0].top_depth, 1)
        self.assertAlmostEqual(20633.0, hole[0].bottom_depth, 1)
        self.assertAlmostEqual(4.28, hole[0].inner_diameter, 0.01)

        self.assertEqual(HoleType.CASED_HOLE, hole[1].hole_type)
        self.assertAlmostEqual(20633.0, hole[1].top_depth, 1)
        self.assertAlmostEqual(23000.0, hole[1].bottom_depth, 1)
        self.assertAlmostEqual(3.0, hole[1].inner_diameter, 0.01)

        self.assertEqual(HoleType.OPEN_HOLE, hole[2].hole_type)
        self.assertAlmostEqual(23000.0, hole[2].top_depth, 1)
        self.assertAlmostEqual(hole_depth, hole[2].bottom_depth, 1)
        self.assertAlmostEqual(2.85, hole[2].inner_diameter, 0.01)

    def test_creating_wellbore_with_missing_drillstring(self):
        wits_record = {
            "collection": "wits",
            "asset_id": 10477107,
            "metadata": {
                'drillstring': '5f4d5bf1150c40007f3a12fc'
            },
            "data": {
                "bit_depth": 1111,
                "hole_depth": 1111
            }
        }

        wellbore = set_drillstring_and_create_wellbore(wits_record)
        self.assertIsNone(wellbore)

    def test_riserless(self):
        wits_json_file = os.path.abspath(
            os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources", "test", "wits_riserless.json")
        )
        wits = file_to_json(wits_json_file)
        wellbore = set_drillstring_and_create_wellbore(wits)

        hole: Hole = wellbore.actual_hole

        self.assertEqual(2, len(hole))

        self.assertEqual(HoleType.CASED_HOLE, hole[0].hole_type)
        self.assertAlmostEqual(3000.0, hole[0].top_depth, 1)
        self.assertAlmostEqual(10000.0, hole[0].bottom_depth, 1)
        self.assertAlmostEqual(7000.0, hole[0].length, 1)
        self.assertAlmostEqual(12.415, hole[0].inner_diameter, 0.01)

        self.assertEqual(HoleType.OPEN_HOLE, hole[1].hole_type)
        self.assertAlmostEqual(10_000.0, hole[1].top_depth, 1)
        self.assertAlmostEqual(15000, hole[1].bottom_depth, 1)

        drillstring = wellbore.actual_drillstring
        self.assertAlmostEqual(0.0, drillstring[0].top_depth, 1)
        self.assertAlmostEqual(15_000.0, drillstring[-1].bottom_depth, 1)

        annulus = wellbore.actual_annulus
        self.assertAlmostEqual(3_000.0, annulus[0].top_depth, 1)
        self.assertAlmostEqual(10_000.0, annulus[0].bottom_depth, 1)
        self.assertAlmostEqual(12.415, annulus[0].inner_diameter_hole, 0.01)
        self.assertEqual(HoleType.CASED_HOLE, annulus[0].hole_type)

        self.assertAlmostEqual(10_000.0, annulus[1].top_depth, 1)
        self.assertAlmostEqual(14_895.9, annulus[1].bottom_depth, 1)
        self.assertEqual(HoleType.OPEN_HOLE, annulus[1].hole_type)

        self.assertAlmostEqual(14906.77, annulus[3].top_depth, 1)
        self.assertAlmostEqual(15_000.0, annulus[3].bottom_depth, 1)
        self.assertAlmostEqual(8.5, annulus[3].inner_diameter_hole, 0.01)
        self.assertEqual(HoleType.OPEN_HOLE, annulus[3].hole_type)


def get_wits():
    wits_json_file = os.path.abspath(
        os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources", "test", "wits.json")
    )
    return file_to_json(wits_json_file)
