#
# This file is part of Orchid and related technologies.
#
# Copyright (c) 2017-2020 Reveal Energy Services.  All Rights Reserved.
#
# LEGAL NOTICE:
# Orchid contains trade secrets and otherwise confidential information
# owned by Reveal Energy Services. Access to and use of this information is 
# strictly limited and controlled by the Company. This file may not be copied,
# distributed, or otherwise disclosed outside of the Company's facilities 
# except under appropriate precautions to maintain the confidentiality hereof, 
# and may not be used in any way not expressly authorized by the Company.
#


from abc import abstractmethod
from collections import namedtuple
from enum import Enum

# noinspection PyUnresolvedReferences
import UnitsNet


About = namedtuple('About', ['abbreviation', 'net_unit'])


class UnitSystem(Enum):
    net_unit = property(lambda self: self.value.net_unit)

    def __repr__(self):
        return f'<{self.system_name()}: {str(self.value)}>'

    abbreviation = property(lambda self: str(self))

    def __str__(self):
        return self.value.abbreviation

    @abstractmethod
    def system_name(self):
        raise NotImplementedError()


# TODO: expand both unit systems to all units in the .NET `UnitSystem` class:
# - Length
# - Angle
# - Pressure
# - Force
# - Volume
# - Mass
# - Power
# - Density
# - Temperature
# - ProppantConcentration
# - SlurryRate
# - Energy

# TODO: Replace usage of unit abbreviations (strings) with UnitSystem concrete child classes.


class UsOilfield(UnitSystem):
    """The enumeration of U. S. oilfield units available via the Orchid Python API."""

    LENGTH = About('ft', UnitsNet.Units.LengthUnit.Foot)
    MASS = About('lb', UnitsNet.Units.MassUnit.Pound)
    PRESSURE = About('psi', UnitsNet.Units.PressureUnit.PoundForcePerSquareInch)
    VOLUME = About('bbl', UnitsNet.Units.VolumeUnit.OilBarrel)

    def system_name(self):
        return 'USOilfield'


class Metric(UnitSystem):
    """The enumeration of metric units available via the Orchid Python API."""

    LENGTH = About('m', UnitsNet.Units.LengthUnit.Meter)
    MASS = About('kg', UnitsNet.Units.MassUnit.Kilogram)
    PRESSURE = About('kPa', UnitsNet.Units.PressureUnit.Kilopascal)
    VOLUME = About('m^3', UnitsNet.Units.VolumeUnit.CubicMeter)

    def system_name(self):
        return 'Metric'


def abbreviation_to_unit(unit_abbreviation: str) -> UnitSystem:
    """
    Determines the `UnitSystem` member corresponding to `unit_abbreviation`.

    Args:
        unit_abbreviation: The abbreviation to convert.

    Returns:
        The corresponding `UnitSystem` member.
    """
    if unit_abbreviation == 'ft':
        return UsOilfield.LENGTH
    elif unit_abbreviation == 'm':
        return Metric.LENGTH
    else:
        raise ValueError(f'Unrecognized unit abbreviation, "{unit_abbreviation}".')
