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

import datetime

import deal
import numpy as np
import pandas as pd

# noinspection PyUnresolvedReferences
from System import DateTime

# noinspection PyUnresolvedReferences
import UnitsNet


def _as_datetime(net_time_point: DateTime) -> datetime.datetime:
    """
    Convert a .NET `DateTime` struct to a Python `datetime.datetime` object.
    :param net_time_point:  The .NET `DateTime` instance to convert.
    :return: The Python `datetime.datetime` instance equivalent to `net_time_point`.
    """
    result = datetime.datetime(net_time_point.Year, net_time_point.Month, net_time_point.Day,
                               net_time_point.Hour, net_time_point.Minute, net_time_point.Second)
    return result


@deal.pre(lambda net_time_series, **kwargs: net_time_series is not None)
def transform_net_time_series(net_time_series, name=None) -> pd.Series:
    """
    Transform a sequence of .NET samples (ticks) to a pandas (Time) Series
    :param net_time_series: The sequence of .NET samples (each an implementation of `ITick<double>`).
    :param name: The name used to identify this time series (used to identify columns in pandas `DataFrame`s.
    :return: The pandas (Time) `Series` for the values.
    """
    result = pd.Series(data=[s.Value for s in net_time_series],
                       index=[_as_datetime(s.Timestamp) for s in net_time_series],
                       dtype=np.float64, name=name)
    return result
