# -*- coding: utf-8 -*-

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

from orchid.project import Project
from orchid.project_loader import ProjectLoader


@deal.pre(lambda ifrac_pathname: ifrac_pathname is not None)
@deal.pre(lambda ifrac_pathname: len(ifrac_pathname) != 0)
@deal.pre(lambda ifrac_pathname: len(ifrac_pathname.strip()) != 0)
def load_project(ifrac_pathname: str) -> Project:
    """
    Return the project for the specified `.ifrac` file.

    :param ifrac_pathname: The path identifying the data file of the project of interest.
    :return: The project of interest.
    """

    loader = ProjectLoader(ifrac_pathname.strip())
    result = Project(loader)
    return result
