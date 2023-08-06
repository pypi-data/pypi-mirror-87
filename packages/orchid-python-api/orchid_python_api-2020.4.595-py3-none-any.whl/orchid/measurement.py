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

"""This module contains functions and classes supporting the (Python) Measurement 'class.'"""

import collections
import numbers

import deal


Measurement = collections.namedtuple('measurement', ['magnitude', 'unit'], module=__name__)


# TODO: Wrap UnitsNet and custom (ratio) types
# This solution, although initially usefully, is not very extensible. I believe, after a discussion with
# Scott, that a better solution would wrap .NET code: both the `UnitsNet` package and the custom types we
# wrote for slurry rate and proppant concentration. Because of the imminent, initial release, I have chosen
# not to make that change at this time. As part of this change, I will introduce symbolic constants so that
# user can use "Intellisense" if available.
CONVERSION_FACTORS = {('bbl/min', 'bbl/s'): 1.0 / 60.0,
                      ('m\u00b3/min', 'm^3/s'): 1.0 / 60.0,
                      ('m\u00b3/min', 'm\u00b3/s'): 1.0 / 60.0,
                      ('bbl/min', 'gal/s'): 42.0 / 60,
                      ('bbl/s', 'gal/s'): 42,
                      ('m\u00b3', 'bbl'): 6.28981,
                      ('kg', 'lb'): 2.20462,
                      ('kPa', 'psi'): 0.145038}


def argument_neither_none_empty_nor_all_whitespace(arg):
    return (arg is not None) and (len(arg.strip()) > 0)


@deal.pre(lambda source_unit, _target_unit: argument_neither_none_empty_nor_all_whitespace(source_unit))
@deal.pre(lambda _source_unit, target_unit: argument_neither_none_empty_nor_all_whitespace(target_unit))
def get_conversion_factor(source_unit, target_unit):
    return CONVERSION_FACTORS[(source_unit, target_unit)]


@deal.pre(lambda magnitude, _: isinstance(magnitude, numbers.Real))
@deal.pre(lambda _, unit: argument_neither_none_empty_nor_all_whitespace(unit))
def make_measurement(magnitude, unit):
    """
    Construct a measurement.
    :param magnitude: The magnitude of the measurement.
    :param unit: The abbreviation of the unit of measurement.
    :return: The constructed (Python) measurement.
    """
    return Measurement(magnitude, unit)


@deal.pre(lambda slurry_rate_unit: argument_neither_none_empty_nor_all_whitespace(slurry_rate_unit))
def slurry_rate_volume_unit(slurry_rate_unit):
    """
    Extract the volume unit from the compound `slurry_rate_unit`.
    :param slurry_rate_unit:  The abbreviation for the compound slurry rate unit.
    :return: The abbreviation for the volume unit of the slurry rate unit.
    """
    if slurry_rate_unit == 'bbl/min':
        return 'bbl'
    elif slurry_rate_unit == 'm^3/min':
        return 'm^3'
    elif slurry_rate_unit == 'm\u00b3/min':
        return 'm\u00b3'
    else:
        raise ValueError(f'Unit, "{slurry_rate_unit}", unrecognized.')


@deal.pre(lambda proppant_concentration_unit: argument_neither_none_empty_nor_all_whitespace(
    proppant_concentration_unit))
def proppant_concentration_mass_unit(proppant_concentration_unit):
    """
    Extract the mass unit from the compound `proppant_concentration_unit`.

    Args:
        proppant_concentration_unit: The abbreviation for the proppant concentration unit.

    Returns:
        The abbreviation for the mass unit of the proppant concentration unit.
    """
    if proppant_concentration_unit == 'lb/gal (U.S.)':
        return 'lb'
    elif proppant_concentration_unit == 'kg/m^3' or proppant_concentration_unit == 'kg/m\u00b3':
        return 'kg'
    else:
        raise ValueError(f'Unit, "{proppant_concentration_unit}", unrecognized.')
