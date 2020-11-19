# Defines the base object, an abstract class that will define the basic behaviour of all
# classes that derive from it.

from abc import ABC, abstractmethod
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

        return prettify_json(
            obj={
                key: value
                for key, value in self.__dict__.items()
                if not key.startswith("__") and not callable(key)
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
