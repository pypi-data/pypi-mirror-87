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

import sys

import deal

import orchid.validation

# noinspection PyUnresolvedReferences
from System import InvalidOperationException
# noinspection PyUnresolvedReferences
from System.IO import (FileStream, FileMode, FileAccess, FileShare)
# noinspection PyUnresolvedReferences
from Orchid.FractureDiagnostics.SDKFacade import ScriptAdapter


class OrchidError(Exception):
    pass


class ProjectLoader:
    """Provides an .NET IProject to be adapted."""

    @deal.pre(orchid.validation.arg_not_none)
    @deal.pre(orchid.validation.arg_neither_empty_nor_all_whitespace)
    def __init__(self, project_pathname: str):
        """
        Construct an instance that loads project data from project_pathname

        :param project_pathname: Identifies the data file for the project of interest.
        """
        self._project_pathname = project_pathname
        self._project = None
        self._in_context = False

    def native_project(self):
        """
        Return the native (.NET) Orchid project.

        :return: The loaded `IProject`.
        """
        if not self._project:
            with ScriptAdapterContext():
                reader = ScriptAdapter.CreateProjectFileReader(orchid.dot_net.app_settings_path())
                # TODO: These arguments are *copied* from `ProjectFileReaderWriterV2`
                stream_reader = FileStream(self._project_pathname, FileMode.Open, FileAccess.Read, FileShare.Read)
                try:
                    self._project = reader.Read(stream_reader)
                finally:
                    stream_reader.Close()
        return self._project


class ScriptAdapterContext:
    """
    A "private" class with the responsibility to initialize and shutdown the .NET ScriptAdapter class.

    I considered making `ProjectLoader` a context manager; however, the API then becomes somewhat unclear.
    - Does the constructor enter the context? Must a caller initialize the instance and then enter the
      context?
    - What results if a caller *does not* enter the context?
    - Enters the context twice?

    Because I was uncertain I created this private class to model the `ScriptAdapter` context. The property,
    `ProjectLoader.native_project`, enters the context if it will actually read the project and exits the
    context when the read operation is finished.

    For information on Python context managers, see
    [the Python docs](https://docs.python.org/3.8/library/stdtypes.html#context-manager-types)
    """

    def __enter__(self):
        try:
            ScriptAdapter.Init()
            return self
        except InvalidOperationException as ioe:
            if 'REVEAL-CORE-0xDEADFA11' in ioe.Message:
                print('Orchid licensing error. Please contact Orchid technical support.')
                sys.exit(-1)
            else:
                raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        ScriptAdapter.Shutdown()
        # Returning no value will propagate the exception to the caller in the normal way
        return


if __name__ == '__main__':
    import doctest
    doctest.testmod()
