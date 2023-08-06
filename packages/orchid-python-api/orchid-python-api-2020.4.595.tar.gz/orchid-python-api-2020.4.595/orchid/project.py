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

from typing import List, Tuple, Iterable

import deal
import toolz.curried as toolz

import orchid.dot_net_dom_access as dna
from orchid.native_well_adapter import NativeWellAdapter
from orchid.native_monitor_curve_facade import NativeMonitorCurveFacade
from orchid.project_loader import ProjectLoader
import orchid.project_units as project_units
import orchid.unit_system as units

# noinspection PyUnresolvedReferences
from Orchid.FractureDiagnostics import IWell, UnitSystem
# noinspection PyUnresolvedReferences
import UnitsNet


def as_unit_system(net_unit_system: UnitSystem):
    if net_unit_system == UnitSystem.USOilfield():
        return units.UsOilfield
    elif net_unit_system == UnitSystem.Metric():
        return units.Metric
    else:
        raise ValueError(f'Unrecognized unit system: {net_unit_system}')


class Project(dna.DotNetAdapter):
    """Adapts a .NET `IProject` to a Pythonic interface."""

    @deal.pre(lambda self, project_loader: project_loader is not None)
    def __init__(self, project_loader: ProjectLoader):
        """
        Construct an instance adapting he project available from net_project.

        :param project_loader: Loads an IProject to be adapted.
        """
        super().__init__(project_loader.native_project())
        self._project_loader = project_loader
        self._are_well_loaded = False
        self._wells = []

    name = dna.dom_property('name', 'The name of this project.')
    project_units = dna.transformed_dom_property('project_units', 'The project unit system.', as_unit_system)
    wells = dna.transformed_dom_property_iterator('wells', 'An iterator of all the wells in this project.',
                                                  NativeWellAdapter)

    def default_well_colors(self) -> List[Tuple[float, float, float]]:
        """
        Calculate the default well colors for this project.
        :return: A list of RGB tuples.
        """
        result = list(map(tuple, self._project_loader.native_project().PlottingSettings.GetDefaultWellColors()))
        return result

    def monitor_curves(self) -> Iterable[NativeMonitorCurveFacade]:
        """
            Return a sequence of well time series for this project.
        Returns:
            An iterable of well time series.
        """
        native_time_series_list_items = self._project_loader.native_project().WellTimeSeriesList.Items
        if len(native_time_series_list_items) > 0:
            return toolz.map(NativeMonitorCurveFacade,
                             self._project_loader.native_project().WellTimeSeriesList.Items)
        else:
            return []

    def unit_abbreviation(self, physical_quantity):
        """
        Return the abbreviation for the specified `physical_quantity` of this project.
        :param physical_quantity: The name of the physical quantity.
        :return: The abbreviation of the specified physical quantity.
        """
        return project_units.unit_abbreviation(self._project_loader.native_project(), physical_quantity)

    def wells_by_name(self, name) -> Iterable[IWell]:
        """
        Return all the wells in this project with the specified name.
        :param name: The name of the well(s) of interest.
        :return: A list of all the wells in this project.
        """
        return toolz.filter(lambda w: name == w.name, self.wells)
