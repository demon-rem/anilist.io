# Contains methods/variables shared between test cases.

from typing import Any, List, Type, Union

from collections import deque

from pytest import raises as _raises


def bruteforce_exception(
    exception: Union[Type[Any], Any], method: Any, *, param: List[Any]
) -> None:
    """
    Type-check a single method against variable input from a list of (in)valid inputs.

    Notes:
        This method will accept a list of **wrong** inputs, rotate them one by one, and
        feed them to the method - expecting to raise an error with every iteration.

        This ensures that each method will work only with a particular type of input -
        if the input is incorrect, the method will raise an error.

    Args:
        exception: The exception that will be raised.
        method: The method to be tested against.
        param: A tuple of data
    """

    # Convert the data into a deque - using this because it can be directly rotated.
    param = deque(param)

    for i in range(len(param)):
        with _raises(exception):
            method(param)

        param.rotate(-1)


def catch(exception: Any, method: Any, *args: Any):
    """
    Type-check one or more methods against a common exception.

    Notes:
        This method type-checks one or more methods against a common input (while
        with the same exception being raised).

    See Also:
        bruteforce_exceptions

    Args:
        exception: Expected exception that will be raised.
        method: An individual method, or a list of methods that are to be tested.
        args: Parameters (incorrect) used to type-check the method(s).
    """

    if not isinstance(method, list):
        method = [method]

    for current_method in method:
        with _raises(exception):
            # Executing every method with the argument, and expecting each of them to
            # raise an error
            current_method(*args) if args else current_method()
