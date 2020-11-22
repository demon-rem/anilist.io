# Defines the base object, an abstract class that will define the basic behaviour of all
# classes that derive from it.

from abc import ABC, abstractmethod
from enum import EnumMeta, Flag
from json import dumps as prettify_json
from typing import Any, Union, Dict, Optional


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
        # in the object- name of the variable being the key with its value being the
        # the value in the dictionary. Then, converting this into a JSON response
        return prettify_json(
            obj={
                f"{key}": value
                for key, value in self.__dict__.items()
                # Appending any instance variable if it does not start with an
                # underscore - private and protected variables are not exposed.
                if not key.startswith("_") and not callable(key)
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


class MetaEnum(ABC, EnumMeta):
    """
    Metaclass just to be able to create an enum with abstract methods - pretty sure
    that there is a way to directly create an enum with abstract methods, but too tired
    to look for that now :(
    """

    pass


class BaseEnum(Flag, metaclass=EnumMeta):
    """
    A custom implementation of an enum similar to `BaseObject`.

    Includes an abstract `stringify` method.

    Notes:
        By default, while making the API call, the name of the enum entry will be
        converted into an upper-case string and used in the API call.

        As such, child classes need to name their entries such that they can be
        directly used while making the API call.

        Alternatively, if any child-class wishes to defer this default behaviour, it
        can alternatively override the `translate` property with a custom implementation
        to map an enum entry to a string that will be used with API calls.
    """

    @abstractmethod
    def stringify(self, indent: Union[int, None] = 4) -> Optional[str]:
        raise NotImplementedError

    @property
    def translate(self):
        """
        Maps an enum key to an appropriate value. Used to convert an enum entry into a
        string - used while making the final API call.

        By default, will simply convert the name of the enum value into an upper-case
        string.

        Any child-class that wants to modify this behaviour can override this method.

        Returns:
            String containing the name of the enum entry in upper case.
        """

        return self.name.upper()
