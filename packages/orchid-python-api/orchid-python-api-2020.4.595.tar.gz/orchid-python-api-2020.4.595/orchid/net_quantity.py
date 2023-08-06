#  Copyright 2017-2020 Reveal Energy Services, Inc 
#
#  Licensed under the Apache License, Version 2.0 (the "License"); 
#  you may not use this file except in compliance with the License. 
#  You may obtain a copy of the License at 
#
#      http://www.apache.org/licenses/LICENSE-2.0 
#
#  Unless required by applicable law or agreed to in writing, software 
#  distributed under the License is distributed on an "AS IS" BASIS, 
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
#  See the License for the specific language governing permissions and 
#  limitations under the License. 
#
# This file is part of Orchid and related technologies.
#

"""This module contains functions for converting between instances of the (Python) `Measurement` class and
instances of .NET classes like `UnitsNet.Quantity` and `DateTime`."""

from datetime import datetime

import toolz.curried as toolz

from orchid.measurement import make_measurement
import orchid.unit_system as units

# noinspection PyUnresolvedReferences,PyPackageRequirements
from System import DateTime
# noinspection PyUnresolvedReferences
import UnitsNet

ABBREVIATION_NET_UNIT_MAP = {units.UsOilfield.LENGTH.abbreviation: UnitsNet.Units.LengthUnit.Foot,
                             units.Metric.LENGTH.abbreviation: UnitsNet.Units.LengthUnit.Meter,
                             units.UsOilfield.MASS.abbreviation: UnitsNet.Units.MassUnit.Pound,
                             units.Metric.MASS.abbreviation: UnitsNet.Units.MassUnit.Kilogram,
                             units.UsOilfield.PRESSURE.abbreviation:
                                 UnitsNet.Units.PressureUnit.PoundForcePerSquareInch,
                             units.Metric.PRESSURE.abbreviation: UnitsNet.Units.PressureUnit.Kilopascal,
                             'MPa': UnitsNet.Units.PressureUnit.Megapascal,
                             units.UsOilfield.VOLUME.abbreviation: UnitsNet.Units.VolumeUnit.OilBarrel,
                             units.Metric.VOLUME.abbreviation: UnitsNet.Units.VolumeUnit.CubicMeter}


def as_datetime(net_time_point):
    return datetime(net_time_point.Year, net_time_point.Month, net_time_point.Day,
                    net_time_point.Hour, net_time_point.Minute, net_time_point.Second,
                    net_time_point.Millisecond * 1000)


def as_measurement(net_quantity):
    """
    Convert a .NET UnitsNet.Quantity to a Python Measurement.
    :param net_quantity: The Python Measurement to convert.
    :return: The Python Measurement corresponding to net_quantity.
    """
    net_quantity_text = str(net_quantity)
    _, raw_net_unit_abbreviation = net_quantity_text.split(maxsplit=1)
    net_unit_abbreviation = raw_net_unit_abbreviation if raw_net_unit_abbreviation != 'm\u00b3' else 'm^3'
    result = make_measurement(net_quantity.Value, net_unit_abbreviation)
    return result


def as_net_date_time(time_point):
    """
    Convert a Python `datetime.datetime` instance to a .NET `DateTime` instance.
    :param time_point: The Python `datetime.datetime` to convert.
    :return: The corresponding .NET `DateTime`
    """
    return DateTime(time_point.year, time_point.month, time_point.day, time_point.hour, time_point.minute,
                    time_point.second, round(time_point.microsecond / 1e3))


def as_net_quantity(measurement):
    """
    Convert a Measurement to a .NET UnitsNet.Quantity in the same unit as the Measurement.
    :param measurement: The Python Measurement to convert.
    :return: The .NET UnitsNet.Quantity corresponding to measurement.
    """
    if measurement.unit == 'ft' or measurement.unit == 'm':
        return UnitsNet.Length.From(UnitsNet.QuantityValue.op_Implicit(measurement.magnitude),
                                    ABBREVIATION_NET_UNIT_MAP[measurement.unit])
    elif measurement.unit == 'lb' or measurement.unit == 'kg':
        return UnitsNet.Mass.From(UnitsNet.QuantityValue.op_Implicit(measurement.magnitude),
                                  ABBREVIATION_NET_UNIT_MAP[measurement.unit])
    elif measurement.unit == 'psi' or measurement.unit == 'kPa' or measurement.unit == 'MPa':
        return UnitsNet.Pressure.From(UnitsNet.QuantityValue.op_Implicit(measurement.magnitude),
                                      ABBREVIATION_NET_UNIT_MAP[measurement.unit])
    elif measurement.unit == 'bbl' or measurement.unit == 'm^3':
        return UnitsNet.Volume.From(UnitsNet.QuantityValue.op_Implicit(measurement.magnitude),
                                    ABBREVIATION_NET_UNIT_MAP[measurement.unit])


def as_net_quantity_in_different_unit(measurement, in_unit):
    """
    Convert a Measurement to a .NET UnitsNet measurement in a specific unit.
    :param measurement: The Python Measurement to convert.
    :param in_unit: An unit abbreviation that can be converted to a .NET UnitsNet.Unit
    :return:
    """
    net_to_convert = as_net_quantity(measurement)
    return net_to_convert.ToUnit(ABBREVIATION_NET_UNIT_MAP[in_unit])


@toolz.curry
def convert_net_quantity_to_different_unit(net_quantity, to_unit):
    """
    Convert one .NET UnitsNet.Quantity to a .NET UnitsNet.Quantity in a specific unit.
    :param net_quantity: The .NET UnitsNet.Quantity to convert.
    :param to_unit: An unit abbreviation that can be converted to a .NET UnitsNet.Unit
    :return: The corresponding .NET UnitsNet.Quantity in the specified unit.
    """

    result = net_quantity.ToUnit(unit_abbreviation_to_unit(to_unit))
    return result


def unit_abbreviation_to_unit(unit_abbreviation: str):
    """
    Convert a unit abbreviation to a .NET UnitsNet.Unit
    :param unit_abbreviation: The abbreviation identifying the target .NET UnitsNet.Unit.
    :return: The corresponding .NET UnitsNet.Unit
    """
    return ABBREVIATION_NET_UNIT_MAP[unit_abbreviation]
