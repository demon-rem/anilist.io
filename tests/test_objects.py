# Tests all the base objects.

from typing import Any, Dict

from json import loads

from pytest import raises
from tests.commons import bruteforce_exception, catch


def test_base_object():
    from dataclasses import dataclass

    from anilist.client.base_object import BaseObject

    # Ensure that an abstract class can't be instantiated.
    catch(TypeError, BaseObject)

    # Making the class *forget* it has abstract methods - testing an abstract method.
    # Used to check the remaining methods of base class.
    BaseObject.__abstractmethods__ = set()

    @dataclass
    class dummy(BaseObject):
        pass

    # The method return a JSON string with all the values stored in the class - since
    # this object does not contain any, the string will be an empty dictionary
    result = dummy()
    assert result.stringify() == "{}"
    assert result.stringify(None) == "{}"

    catch(NotImplementedError, dummy.initialize, "")

    with raises(TypeError):
        # noinspection PyTypeChecker
        result.stringify("")


def test_base_enum():
    from enum import auto

    from anilist.client.base_object import BaseEnum

    # Making the abstract class forget it has any abstract methods.
    BaseEnum.__abstractmethods__ = set()

    # Creating a temporary enum with a single value
    class Child(BaseEnum):
        test_val = auto()

    child = Child(1)  # Will map to the only value in the enum - `test_val`
    catch(NotImplementedError, child.stringify)


# noinspection PyTypeChecker
def test_user_avatar():
    from anilist.types.user_data import UserAvatar

    # Links should always be stored as strings.
    with raises(TypeError):
        UserAvatar(None, None)

    # Link to user avatar should not be a blank string.
    with raises(ValueError):
        UserAvatar("", "")

    # Instantiating to use this for tests
    avatar = UserAvatar(
        large_avatar="large avatar link", medium_avatar="medium avatar link"
    )

    # Validating the result of stringify
    result = avatar.stringify()
    assert isinstance(result, str)

    # Using this result to create an instance of the class, and comparing them
    new_val = avatar.initialize(result)
    assert isinstance(new_val, UserAvatar)
    assert new_val.large == avatar.large
    assert new_val.medium == avatar.medium

    with raises(TypeError):
        UserAvatar.initialize(None)

    # Testing the same using a dictionary - for this using `result` from above, and
    # mapping it to be a dictionary.
    del new_val
    new_val: Dict[str, Any] = loads(result)

    # Type checking the result - as the `initialize` method internally delegates
    # both string and dict to dict, and then uses them, checking variables individually
    # will be a waste
    assert isinstance(UserAvatar.initialize(new_val), UserAvatar)


def test_fuzzy_date():
    from anilist.types import FuzzyDate

    # Type-check
    bruteforce_exception(TypeError, FuzzyDate, param=["", None, 2.0])
    catch(TypeError, FuzzyDate.initialize, None)

    date = FuzzyDate(13, year=1990)
    assert date.day == 13
    assert date.month == 0
    assert date.year == 1990

    # Ensuring the date can be mapped to API-friendly value - will be YYYYMMDD format
    assert date.fuzz == "19900013"

    # Attempting to create another fuzzy-date object by fetching JSON from the first.
    new_date = FuzzyDate.initialize(date.stringify())
    assert new_date.day == date.day
    assert new_date.month == date.month
    assert new_date.year == date.year

    dict_data = loads(date.stringify())
    new_date = FuzzyDate.initialize(dict_data)
    assert new_date.day == date.day
    assert new_date.month == date.month
    assert new_date.year == date.year

    # Ensuring that two digit numbers are auto-mapped.
    temp = FuzzyDate(year=13)
    assert temp.year == 2013


def test_media_enums():
    from anilist.types import (
        MediaFormat,
        MediaSeason,
        MediaSort,
        MediaSource,
        MediaStatus,
    )

    # Iterating through all entries present in the enum, asserting that stringify
    # method works for them, `__members__` returns a dictionary of name - in string
    # and the value, for every value present in the enum.
    for x in (MediaSeason, MediaFormat, MediaStatus, MediaSource, MediaSort):
        for enum_str, enum in x.__members__.items():
            if isinstance(enum, MediaSeason):
                key = "season"
            elif isinstance(enum, MediaFormat):
                key = "format"
            elif isinstance(enum, MediaStatus):
                key = "status"
            elif isinstance(enum, MediaSource):
                key = "source"
            elif isinstance(enum, MediaSeason):
                key = "season"
            elif isinstance(enum, MediaSort):
                catch(NotImplementedError, enum.stringify)
                continue  # Jump to the next iteration.
            else:
                raise ValueError(f"Unexpected key-type in test cases: {type(enum)}")

            assert isinstance(enum.stringify(), str)
            assert enum.stringify() == f'"{key}": "{enum.translate}"'
