"""
Defines the base object, an abstract class that will define the basic behaviour of all
classes that derive from it.

Used to define the common behaviour among all objects.
"""

from abc import ABC, abstractmethod
from ast import literal_eval
from enum import Enum
from . import BaseEnum
from json import dumps as prettify_json
from typing import Any, Union, Dict


class BaseObject(ABC):
    def stringify(self, indent: Union[int, None] = 4) -> str:
        """
        Convert the data held by this instance into a printable string.

        Args:
            indent: Integer containing amount of indent required. Defaults to 4.
            Can optionally be `None` if the entire JSON is to be returned in a
            single line.

        Returns:
            String containing prettified-version of the JSON data.
        """

        if indent is not None and not isinstance(indent, int):
            raise TypeError

        # Using built-in method(s), generate a dictionary of instance variables present
        # in the object-name of the variable being the key with its value being the
        # the value in the dictionary. Then, converting this into a JSON response
        return prettify_json(
            obj={
                f"{key}": value
                # Allowing the JSON library to automatically map primitive types
                if isinstance(value, (int, str, list, dict, tuple))
                # If the object is derived from `BaseObject`, calling the `stringify()`
                # method on the object to get its string representation - the response
                # will contain escape sequences (such as "\n"), using `literal_eval` to
                # convert them into a printable string.
                else literal_eval(value.stringify()) if isinstance(value, BaseObject)
                # If the object is derived from an enum, calling the `stringify()`
                # method on this - not using `literal_eval` as the result will simply
                # be a string.
                else value.stringify() if isinstance(value, BaseEnum)
                # If the flow-of-control reaches this part, adding this as an error
                else f"Error: `{type(value)}` has no method `stringify()`"
                for key, value in self.__dict__.items()
                # Appending any instance variable if it does not start with an
                # underscore - private and protected variables are not exposed.
                if key[0] != "_" and not callable(key)
            },
            indent=indent,
            sort_keys=True,
        )

    @staticmethod
    @abstractmethod
    def initialize(data: Union[str, Dict[Any, Any]]) -> Any:
        """
        Static method to instantiate an object of this class using a JSON string, or a
        dictionary containing the required key-value pairs.

        Args:
            data: Can be a string containing JSON data to populate an instance of the
            child class. Or, a dictionary containing key-value pairs with the
            appropriate data.

        Returns:
            An object of the child class, populated with the data passed in to this
            method.
        """

        raise NotImplementedError("Direct call to abstract method")
