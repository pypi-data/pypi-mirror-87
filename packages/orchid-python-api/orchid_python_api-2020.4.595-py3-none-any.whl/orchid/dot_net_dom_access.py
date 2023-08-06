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

import uuid

import deal
import toolz.curried as toolz

import orchid.validation

# noinspection PyUnresolvedReferences
from System import Guid


# These methods in this module are based on the StackOverflow post:
# https://stackoverflow.com/questions/36580931/python-property-factory-or-descriptor-class-for-wrapping-an-external-library
#
# Additionally, it resolves an issue I was experiencing with PyCharm: when I used `property` directly
# in the class definition, PyCharm reported "Property 'xyz' could not be read. I think it might have been
# than I needed to apply `curry` to the "getter method" I also defined in the class in order to pass he
# attribute name at definition time (because `self` was only available at run-time).


def get_dot_net_property_value(attribute_name, dom_object):
    """
    Return the value of the DOM property whose name corresponds to `attribute_name`.
    :param attribute_name: The Python `attribute_name`.
    :param dom_object: The DOM object whose property is sought.
    :return: The value of the DOM property.
    """
    @toolz.curry
    def python_name_to_words(python_name):
        return python_name.split('_')

    def capitalize_words(words):
        return toolz.map(str.capitalize, words)

    def words_to_dot_net_property_name(words):
        return ''.join(words)

    @toolz.curry
    def get_value_from_dom(dom, property_name):
        return getattr(dom, property_name)

    # The function, `thread_last`, from `toolz.curried`, "splices" threads a value (the first argument)
    # through each of the remaining functions as the *last* argument to each of these functions.
    result = toolz.thread_last(attribute_name,
                               python_name_to_words,
                               capitalize_words,
                               words_to_dot_net_property_name,
                               get_value_from_dom(dom_object))
    return result


def dom_property(attribute_name, docstring):
    """
    Return the property of the DOM corresponding to `attribute_name` with doc string.
    :param attribute_name: The name of the Python attribute.
    :param docstring: The doc string to be attached to the resulting property.
    :return: The Python property wrapping the value of the DOM property.
    """
    def getter(self):
        result = get_dot_net_property_value(attribute_name, self._adaptee)
        return result

    # Ensure no setter for the DOM properties
    return property(fget=getter, doc=docstring, fset=None)


def transformed_dom_property(attribute_name, docstring, transformer):
    """
    Return the transformed property of the DOM corresponding to `attribute_name`.
    :param attribute_name: The name of the Python attribute.
    :param docstring: The doc string to be attached to the resulting property.
    :param transformer: A callable to transform the value returned by the .NET DOM property.
    :return: The Python property wrapping the transformed value of the DOM property.
    """
    def getter(self):
        raw_result = get_dot_net_property_value(attribute_name, self._adaptee)
        result = transformer(raw_result)
        return result

    # Ensure no setter for the DOM properties
    return property(fget=getter, doc=docstring, fset=None)


def transformed_dom_property_iterator(attribute_name, docstring, transformer):
    """
    Return transformed collection property of the DOM corresponding to `attribute_name` with doc string, `docstring`.
    :param attribute_name: The name of the original attribute.
    :param docstring: The doc string to be attached to the resultant property.
    :param transformer: A callable invoked on each value in the list returned by the .NET DOM property.
    :return: The Python property wrapping a Python iterator mapping values from the DOM property (collection) items.
    """
    def getter(self):
        container = get_dot_net_property_value(attribute_name, self._adaptee)
        result = toolz.map(transformer, container.Items)
        return result

    # Ensure no setter for the DOM properties
    return property(fget=getter, doc=docstring, fset=None)


def as_uuid(guid: Guid):
    return uuid.UUID(str(guid))


class DotNetAdapter:
    @deal.pre(orchid.validation.arg_not_none)
    def __init__(self, adaptee):
        """
        Construct an instance adapting a .NET IStage.
        :param adaptee: The .NET DOM object to adapt.
        """
        self._adaptee = adaptee

    object_id = transformed_dom_property('object_id', 'The object ID of the adapted .NET DOM object.', as_uuid)

    def dom_object(self):
        """
        (PRIVATE) Determine the DOM object being adapted.

        This method is only intended to be used **INSIDE** the orchid package. It is **NOT** intended for
        external use.

        Returns:
            The .NET DOM object being adapted.
        """
        return self._adaptee
