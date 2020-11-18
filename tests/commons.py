# Contains methods/variables shared between test cases.

from typing import Any, List, Type, Union

from random import shuffle as _random_shuffle

from pytest import raises as _raises


def bruteforce_exceptions(
    method: Any,
    data: List[Any],
    exception: Union[Type[Any], Any] = TypeError,
) -> None:
    """
    Test a method to throw exceptions by running it against randomized list of inputs - normally
    used to type-check a method.

    Notes:
        This method will accept a list of **wrong** inputs, randomize and feed them to the method -
        expecting to raise an error with every iteration.

        This ensures that each method will work only with a particular type of input - if the input
        is incorrect, the method will raise an error.

    Args:
        method: The method to be tested against.
        data: A tuple of data
        exception: The exception that will be raised. Defaults to `TypeError`
    """

    for i in range(len(data)):
        _random_shuffle(data)
        with _raises(exception):
            method(data)
