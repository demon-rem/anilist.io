# Test the errors - just the basics for now - type check for one. Converting python to a
# strong-typed language, one module at a time :p

from random import randint

from anilist import Anilist
from anilist.errors import APIError
from pytest import raises
from tests import LOGGER
from tests.commons import bruteforce_exceptions


def test_base_error():
    LOGGER.info(f"Checking errors - `{APIError.__name__}`")

    # Bruteforcing type-check exception(s)
    bruteforce_exceptions(APIError, data=["message", None, int(2)])

    # Adding (another) test because without this code coverage drops (stupidly)
    with raises(TypeError):
        APIError("test", 3, 5)

    # Check if the class can be instantiated using randomized data.
    error_status = randint(1, 100)
    error_message = "test error message"
    error_locations = {"line": 3, "column": 2}

    error = APIError(
        status=error_status, message=error_message, locations=error_locations
    )

    assert error.status == error_status
    assert error.message == error_message
    assert error.locations == error_locations

    assert error.__reduce__() == (
        APIError,
        (error_status, error_message, error_locations),
    )

    # Todo: Another (stupid) test case, remove this later.
    assert type(Anilist()) == Anilist
