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


import pandas as pd

import orchid.dot_net_dom_access as dna
from orchid.net_quantity import as_datetime
import orchid.physical_quantity as pq


class NativeMonitorCurveFacade(dna.DotNetAdapter):
    def __init__(self, native_well_time_series):
        super().__init__(native_well_time_series)

    display_name = dna.dom_property('display_name', 'The display name of the .NET well time series.')
    sampled_quantity_name = dna.dom_property('sampled_quantity_name',
                                             'The name describing the physical quantity of each sample of the .NET '
                                             'well time series.')
    sampled_quantity_type = dna.transformed_dom_property('sampled_quantity_type',
                                                         'The physical quantity of each sample.',
                                                         pq.to_physical_quantity)

    def time_series(self) -> pd.Series:
        """
        Return the time series for this treatment curve.

        Returns
            The time series of this treatment curve.
        """
        # Because I use `samples` twice in the subsequent expression, I must *actualize* the map by invoking `list`.
        samples = list(map(lambda s: (s.Timestamp, s.Value), self._adaptee.GetOrderedTimeSeriesHistory()))
        result = pd.Series(data=map(lambda s: s[1], samples), index=map(as_datetime, map(lambda s: s[0], samples)),
                           name=self.display_name)
        return result
