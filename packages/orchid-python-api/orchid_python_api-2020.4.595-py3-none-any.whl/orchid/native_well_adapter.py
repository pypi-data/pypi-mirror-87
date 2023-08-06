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

# noinspection PyUnresolvedReferences
import orchid
import orchid.dot_net_dom_access as dna
import orchid.native_stage_adapter as nsa
import orchid.native_trajectory_adapter as nta

# noinspection PyUnresolvedReferences
from Orchid.FractureDiagnostics import IWell


def replace_no_uwi_with_text(uwi):
    return uwi if uwi else 'No UWI'


class NativeWellAdapter(dna.DotNetAdapter):
    """Adapts a native IWell to python."""
    def __init__(self, net_well: IWell):
        """
        Constructs an instance adapting a .NET IWell.
        :param net_well: The .NET well to be adapted.
        """
        super().__init__(net_well)

    name = dna.dom_property('name', 'The name of the adapted .NET well.')
    display_name = dna.dom_property('display_name', 'The display name of the adapted .NET well.')
    stages = dna.transformed_dom_property_iterator('stages', 'An iterator over the NativeStageAdapters.',
                                                   nsa.NativeStageAdapter)
    trajectory = dna.transformed_dom_property('trajectory', 'The trajectory of the adapted .NET well.',
                                              nta.NativeTrajectoryAdapter)
    uwi = dna.transformed_dom_property('uwi', 'The UWI of the adapted .', replace_no_uwi_with_text)
