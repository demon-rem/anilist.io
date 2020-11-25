from __future__ import annotations

from abc import ABC
from enum import EnumMeta, Flag
from typing import Optional, TypeVar


class MetaEnum(ABC, EnumMeta):
    """
    Metaclass just to be able to create an enum with abstract methods - pretty sure
    that there is a way to directly create an enum with abstract methods, but too tired
    to look for that now :(
    """

    pass


this = TypeVar("this")


class BaseEnum(Flag, metaclass=EnumMeta):
    """
    Custom implementation of enum similar to `BaseObject` - is the base over which
    all enums being used are created.

    Includes a `stringify` method to be able to print the contents of the enum.

    Notes:
        By default, while making the API call, the name of the enum entry will be
        converted into an upper-case string and used in the API call.

        As such, child classes need to name their entries such that they can be
        directly used while making the API call.

        Alternatively, if any child-class wishes to defer this default behaviour, it
        can alternatively override the `translate` property with a custom implementation
        to map an enum entry to a string that will be used with API calls.
    """

    def stringify(self) -> Optional[str]:
        return self.translate

    @property
    def translate(self) -> str:
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

    @staticmethod
    def map(enum_type: EnumMeta, key: str) -> this:
        """
        Maps a string to the current enum.

        Will iterate over all elements present in the given enum, translating them
        one by one, if the string matches with any value, will return the value.

        Raises:
            ValueError: Raised if the string cannot be mapped to an existing enum value.

        Args:
            enum_type: The enum in which the value is to be mapped. Entries in this enum
                will be scanned against by running the `translate` method.
            key: String containing the value that is to be mapped to the enum.

        Returns:
            The enum in which the value can be successfully mapped, or none if no
            match occurs
        """

        if (
            not isinstance(enum_type, type)
            or not issubclass(enum_type, BaseEnum)
            or not isinstance(key, str)
        ):
            raise TypeError

        # Type hint just to stop mypy from displaying this as an error
        enum: Optional[this] = None  # Initializing to none to for python 3.5 and below
        for enum in enum_type.__members__.values():
            # MyPy throws an error for the statement without any reason, making it skip
            # the line for now.
            if enum.translate == key:  # type: ignore
                return enum

        raise ValueError(
            f"Attempt to map value `{key}` to the enum `{enum_type.__name__}`"
        )
