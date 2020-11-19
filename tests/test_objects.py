# Tests all the base objects.

from typing import Any, Dict

from dataclasses import dataclass
from json import loads

from anilist.types.user_data import UserAvatar
from pytest import raises
from tests.commons import exception


def test_base_object():
    from anilist.client.base_object import BaseObject

    # Ensure that an abstract class can't be instantiated.
    exception(BaseObject, TypeError)

    # Making the class *forget* it has abstract methods - testing an abstract method.
    BaseObject.__abstractmethods__ = set()

    @dataclass
    class dummy(BaseObject):
        pass

    # The method return a JSON string with all the values stored in the class - since
    # this object does not contain any, the string will be an empty dictionary
    result = dummy()
    assert result.stringify() == "{}"
    assert result.stringify(None) == "{}"

    exception(dummy.initialize, NotImplementedError, "")

    with raises(TypeError):
        # noinspection PyTypeChecker
        result.stringify("")


# noinspection PyTypeChecker
def test_user_avatar():
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
