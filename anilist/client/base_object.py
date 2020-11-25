"""
Defines the base object, an abstract class that will define the basic behaviour of all
classes that derive from it.

Used to define the common behaviour among all objects.
"""

from abc import ABC, abstractmethod
from ast import literal_eval
from json import JSONEncoder
from json import dumps as prettify_json
from typing import Any, Union, Dict

from . import BaseEnum


class _CustomEncoder(JSONEncoder):
    """
    Implementing a custom encoder to encode a classes into a a printable string.

    Depending on the type of variable encountered, behaviour of the encoder will vary
    to ensure that the final JSON structure maps all the variables present in each
    object.
    """

    def default(self, o: Any) -> Any:
        if isinstance(o, (int, str, list, dict, tuple, float)):
            # In case of primitive data types, using the built-in encoder.
            #
            # In case of complex datatype, i.e. list/dictionary/tuple, the
            # encoder will iterate over each element present in the structure, calling
            # this method for every object encountered - ensuring that the
            # custom implementation works with iterable data types as well.
            return JSONEncoder.default(self=self, o=o)
        if isinstance(o, BaseEnum):
            # If the object is derived from an enum, calling the `stringify()`
            # method on this - not using `literal_eval` as the result will simply
            # be a string.
            return o.stringify()
        elif isinstance(o, BaseObject):
            # If the object is derived from `BaseObject`, calling the `stringify()`
            # method on the object to get its string representation - the response
            # will contain escape sequences (such as "\n"), using `literal_eval` to
            # convert them into a printable string.
            return literal_eval(o.stringify())
        else:
            Warning(
                f"Error; Unexpected object of type `{type(o)}` encountered. Unable "
                f"to encode it into a string"
            )

            return f"<error>"


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
                # Allowing the JSON library to automatically map primitive types
                f"{key}": value
                for key, value in self.__dict__.items()
                # Appending any instance variable if it does not start with an
                # underscore - private and protected variables are not exposed.
                if key[0] != "_" and not callable(key)
            },
            indent=indent,
            sort_keys=True,
            cls=_CustomEncoder,  # Using custom-encoder to handle complex data types
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
