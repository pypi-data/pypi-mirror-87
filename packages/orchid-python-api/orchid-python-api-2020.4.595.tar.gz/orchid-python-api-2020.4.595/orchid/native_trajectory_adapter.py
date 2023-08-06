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

import deal
import numpy as np

import orchid.validation
import orchid.dot_net_dom_access as dna

# noinspection PyUnresolvedReferences
from Orchid.FractureDiagnostics import (IWellTrajectory, WellReferenceFrameXy, DepthDatum, IWell)

# noinspection PyUnresolvedReferences
import UnitsNet


class NativeTrajectoryAdapter(dna.DotNetAdapter):
    def __init__(self, net_trajectory: IWellTrajectory):
        """
        Constructs an instance adapting a .NET IWellTrajectory.
        :param net_trajectory: The .NET stage time series to be adapted.
        """
        super().__init__(net_trajectory)
        self._reference_frame_text_net_map = {'absolute': WellReferenceFrameXy.AbsoluteStatePlane,
                                              'project': WellReferenceFrameXy.Project,
                                              'well_head': WellReferenceFrameXy.WellHead}

    @deal.pre(orchid.validation.arg_not_none)
    @deal.pre(orchid.validation.arg_neither_empty_nor_all_whitespace)
    @deal.pre(lambda _, reference_frame: reference_frame in ['absolute', 'project', 'well_head'])
    def get_easting_array(self, reference_frame: str) -> np.array:
        """
        Calculates the eastings of this trajectory in the specified `reference_frame` measured in `length_units`
        :param reference_frame: The reference from for the easting coordinates. Valid values are 'absolute' (
        absolute state plane), 'project', and 'well_head'.
        """
        net_reference_frame = self._reference_frame_text_net_map[reference_frame]
        project_length_unit = self._adaptee.Well.Project.ProjectUnits.LengthUnit
        raw_eastings = self._adaptee.GetEastingArray(net_reference_frame)
        return np.array([e.As(project_length_unit) for e in raw_eastings])

    @deal.pre(orchid.validation.arg_not_none)
    @deal.pre(orchid.validation.arg_neither_empty_nor_all_whitespace)
    @deal.pre(lambda _, reference_frame: reference_frame in ['absolute', 'project', 'well_head'])
    def get_northing_array(self, reference_frame: str) -> np.array:
        """
        Calculates the northings of this trajectory in the specified `reference_frame` measured in `length_units`
        :param reference_frame: The reference from for the easting coordinates. Valid values are 'absolute' (
        absolute state plane), 'project', and 'well_head'.
        """
        net_reference_frame = self._reference_frame_text_net_map[reference_frame]
        project_length_unit = self._adaptee.Well.Project.ProjectUnits.LengthUnit
        raw_northings = self._adaptee.GetNorthingArray(net_reference_frame)
        return np.array([e.As(project_length_unit) for e in raw_northings])
