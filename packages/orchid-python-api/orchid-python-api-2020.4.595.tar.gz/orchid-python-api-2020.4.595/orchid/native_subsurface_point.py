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


import abc


import orchid.dot_net_dom_access as dna
import orchid.net_quantity as onq

import toolz.curried as toolz


class BaseSubsurfacePoint(dna.DotNetAdapter):
    depth_origin = dna.dom_property('depth_datum',
                                    'The datum or origin for the z-coordinate of this point.')
    xy_origin = dna.dom_property('well_reference_frame_xy',
                                 'The reference frame or origin for the x-y coordinates of this point.')

    @property
    @abc.abstractmethod
    def x(self):
        """The x-coordinate of this point."""
        pass

    @property
    @abc.abstractmethod
    def y(self):
        """The y-coordinate of this point."""
        pass

    @property
    @abc.abstractmethod
    def depth(self):
        """The depth of this point."""
        pass


class SubsurfacePoint(BaseSubsurfacePoint):
    """Adapts a .NET ISubsurfacePoint to be more Pythonic."""

    x = dna.transformed_dom_property('x', 'The x-coordinate of this point.', onq.as_measurement)
    y = dna.transformed_dom_property('y', 'The y-coordinate of this point.', onq.as_measurement)
    depth = dna.transformed_dom_property('depth', 'The z-coordinate (depth) of this point.', onq.as_measurement)

    def as_length_unit(self, as_length_unit):
        return SubsurfacePointUsingLengthUnit(self._adaptee, as_length_unit)


class SubsurfacePointUsingLengthUnit(BaseSubsurfacePoint):
    """Adapts a .NET ISubsurfacePoint to be more Pythonic. Always returns lengths in the specified units."""

    def __init__(self, adaptee, in_length_unit):
        super().__init__(adaptee)
        self._length_converter_func = toolz.flip(onq.convert_net_quantity_to_different_unit,
                                                 in_length_unit.abbreviation)

    @property
    def x(self):
        """The x-coordinate of this point."""
        return onq.as_measurement(self._length_converter_func(self._adaptee.X))

    @property
    def y(self):
        """The y-coordinate of this point."""
        return onq.as_measurement(self._length_converter_func(self._adaptee.Y))

    @property
    def depth(self):
        """The depth of this point."""
        return onq.as_measurement(self._length_converter_func(self._adaptee.Depth))
