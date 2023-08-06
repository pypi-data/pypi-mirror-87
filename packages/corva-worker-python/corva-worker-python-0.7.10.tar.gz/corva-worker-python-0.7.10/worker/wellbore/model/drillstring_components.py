from copy import deepcopy

import numpy as np

from worker.data.serialization import serialization
from worker.data.unit_conversions import US_LIQUID_GAL_to_INCH3
from worker.wellbore.model.element import Element
from worker.wellbore.model.enums import PipeType, PipeMaterial
from worker.data.operations import nanround, equal


@serialization
class Pipe(Element):
    SERIALIZED_VARIABLES = {
        'top_depth': float,
        'bottom_depth': float,
        'length': float,

        'inner_diameter': float,
        'outer_diameter': float,

        'joint_length': float,
        'max_outer_diameter': float,
        'inner_diameter_tooljoint': float,
        'outer_diameter_tooljoint': float,
        'tool_joint_length_per_joint': float,
        'linear_mass_in_air': float,
        'order': float,

        'pipe_material': PipeMaterial,
        'grade': float,

        'tool_joint_length_ratio': float,
        'pipe_type': PipeType,
    }

    """
    The pipe object can be used for the following components directly:
    - drill pipe (DP)
    - drill collar (DC)
    - heavy weight drill pipe (HWDP)
    - subs
    - stabilizers

    This class is extended by the other drillpipe components.
    """
    def __init__(self, **kwargs):
        super(Pipe, self).__init__(**kwargs)

        self.inner_diameter = kwargs['inner_diameter']
        self.outer_diameter = kwargs['outer_diameter']

        self.joint_length = kwargs.get('component_length', kwargs.get('joint_length'))
        self.max_outer_diameter = kwargs.get('max_outer_diameter')
        self.inner_diameter_tooljoint = kwargs.get('inner_diameter_tooljoint')
        self.outer_diameter_tooljoint = kwargs.get('outer_diameter_tooljoint')
        self.tool_joint_length_per_joint = kwargs.get('length_tooljoint') or kwargs.get('tool_joint_length_per_joint')
        self.linear_mass_in_air = kwargs.get('linear_weight', kwargs.get('linear_mass_in_air'))
        self.order = kwargs.get('order')

        self.pipe_material = kwargs.get('material')
        self.grade = kwargs.get('grade')

        self.set_tool_joint_length_ratio()

        family = kwargs.get('family') or ""
        self.pipe_type = PipeType.determine_type(family)

    def get_max_outer_diameter(self):
        return self.max_outer_diameter or self.outer_diameter_tooljoint or self.outer_diameter

    def set_tool_joint_length_ratio(self):
        if self.tool_joint_length_per_joint is None or not self.joint_length:
            self.tool_joint_length_ratio = 0
        else:
            self.tool_joint_length_ratio = self.tool_joint_length_per_joint / self.joint_length

    def is_valid_tool_joint(self):
        """
        If there is a valid tool joint or not
        :return:
        """
        if self.outer_diameter_tooljoint is None:
            return False
        if self.inner_diameter_tooljoint is None:
            return False
        if not self.tool_joint_length_ratio:
            return False

        return True

    def get_pipe_id_area(self):
        """
        Compute the total inner area of the pipe body
        :return: inner area of the pipe body in INCH^2
        """
        return np.pi / 4 * (self.inner_diameter ** 2)

    def get_pipe_od_area(self):
        """
        Compute the total outer area of the pipe body
        :return: outer area of the pipe body in INCH^2
        """
        return np.pi / 4 * (self.outer_diameter ** 2)

    def get_pipe_tool_joint(self):
        """
        Create a pipe with its id and od equal to the tool joint values (if available)
        :return:
        """
        p = deepcopy(self)
        p.inner_diameter = p.inner_diameter_tooljoint or p.inner_diameter
        p.outer_diameter = p.outer_diameter_tooljoint or p.outer_diameter
        return p

    def compute_inner_area_tool_joint_adjusted(self):
        """
        Compute the inner area of the pipe adjusted for the tool joint
        :return: the area in INCH^2
        """
        area_body = self.get_pipe_id_area()  # in INCH^2
        if not self.is_valid_tool_joint():
            return area_body

        area_tj = np.pi / 4 * (self.inner_diameter_tooljoint ** 2)  # in INCH^2
        return (
            area_body * (1 - self.tool_joint_length_ratio)
            + area_tj * self.tool_joint_length_ratio
        )

    def compute_outer_area_tool_joint_adjusted(self):
        """
        Compute the outer area of the pipe adjusted for the tool joint
        :return: the area in INCH^2
        """
        area_body = self.get_pipe_od_area()  # in INCH^2
        if not self.is_valid_tool_joint():
            return area_body

        area_tj = np.pi / 4 * (self.outer_diameter_tooljoint ** 2)  # in INCH^2
        r = self.tool_joint_length_ratio
        return area_body * (1 - r) + area_tj * r

    def compute_inner_diameter_tool_joint_adjusted(self):
        """
        Compute the inner diameter of the pipe adjusting for the tool joint
        :return: the adjusted inner diameter of the pipe in INCH
        """
        di_body = self.inner_diameter
        if not self.is_valid_tool_joint():
            return di_body

        di_tj = self.inner_diameter_tooljoint
        r = self.tool_joint_length_ratio
        return di_body * (1 - r) + di_tj * r

    def compute_outer_diameter_tool_joint_adjusted(self):
        """
        Compute the outer diameter of the pipe adjusting for the tool joint
        :return: the adjusted outer diameter of the pipe in INCH
        """
        do_body = self.outer_diameter
        if not self.is_valid_tool_joint():
            return do_body

        do_tj = self.outer_diameter_tooljoint
        r = self.tool_joint_length_ratio
        return do_body * (1 - r) + do_tj * r

    def compute_body_cross_sectional_area_tj_adjusted(self):
        """
        Compute body cross sectional area adjusted for the tool joint
        :return: area in INCH^2
        """
        return self.compute_outer_area_tool_joint_adjusted() - self.compute_inner_area_tool_joint_adjusted()

    # override
    def compute_get_area(self):
        return self.compute_inner_area_tool_joint_adjusted()

    def compute_body_volume_tj_adjusted(self):
        """
        Compute body volume adjusted for the tool joint
        :return: volume in FOOT^3
        """
        return self.compute_body_cross_sectional_area_tj_adjusted() / 144 * self.length

    def compute_outer_volume_tj_adjusted(self):
        """
        Compute outer volume adjusted for the tool joint
        :return: volume in FOOT^3
        """
        return self.compute_outer_area_tool_joint_adjusted() / 144 * self.length

    def compute_inner_volume_tj_adjusted(self):
        """
        Compute inner volume adjusted for the tool joint
        :return: volume in FOOT^3
        """
        return self.compute_inner_area_tool_joint_adjusted() / 144 * self.length

    # override
    def compute_get_volume(self):
        return self.compute_inner_volume_tj_adjusted()

    def calculate_linear_mass(self):
        """
        Compute the pipe linear mass in air from pipe materials
        :return: pipe linear mass in LB/FOOT
        """
        density = self.pipe_material.get_density()  # PPG
        pipe_body_area = self.get_pipe_body_area()  # INCH^2
        linear_mass = density * pipe_body_area * (US_LIQUID_GAL_to_INCH3 * 12)  # lb/ft
        return linear_mass

    def __eq__(self, other):
        if not isinstance(other, (Pipe, Bit)):
            return False

        if self.eq_without_length(other) is False:
            return False

        return self.length == other.length

    def eq_without_length(self, other):
        params = [
            'pipe_type',
            'inner_diameter',
            'outer_diameter',
            'inner_diameter_tooljoint',
            'outer_diameter_tooljoint',
            'linear_mass_in_air'
        ]
        return equal(self, other, params)

    def eq_id_and_od(self, other):
        params = [
            'inner_diameter',
            'outer_diameter'
        ]
        return equal(self, other, params)

    def __repr__(self):
        return (
            f"{self.pipe_type.name:13}"
            f"{nanround(self.inner_diameter, 2):>6} in / "
            f"{nanround(self.outer_diameter, 2):>6} in, "
            f"{nanround(self.linear_mass_in_air, 2):>6} lb/ft, "
            f"{super().__repr__()}"
        )


@serialization
class MWD(Pipe):
    # TODO extra items to be implemented later
    pass


@serialization
class PDM(Pipe):
    # TODO extra items to be implemented later
    pass


@serialization
class RSS(Pipe):
    # TODO extra items to be implemented later
    pass


@serialization
class Agitator(Pipe):
    pass


@serialization
class Bit(Element):
    SERIALIZED_VARIABLES = {
        'top_depth': float,
        'bottom_depth': float,
        'length': float,

        'size': float,
        'tfa': float,
        'pipe_type': PipeType
    }

    # TODO extra items to be implemented later
    def __init__(self, **kwargs):
        super(Bit, self).__init__(**kwargs)

        self.size = float(kwargs['size'])
        self.tfa = float(kwargs['tfa'])
        self.pipe_type = PipeType.BIT

    # override
    def compute_get_area(self):
        return 0

    # override
    def compute_get_volume(self):
        return 0

    def __repr__(self):
        return (
            f"{self.pipe_type.name:13}"
            f"{nanround(self.size, 2)} in - "
            f"tfa={nanround(self.tfa, 2)} in^2, "
            f"{super().__repr__()}"
        )
