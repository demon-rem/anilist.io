"""
Defines a query object. This will be the base class used to define the behaviour of a
query.

The basic behaviour of all queries will be to receive input from the user, convert it
into a string that can then be used while making an API call.

Each sub-class deriving from this base class will internally handle the part of
enforcing defaults, taking user input, rejecting a blank query if needed and more.
"""

from abc import abstractmethod
from typing import Any


class BaseQuery:
    @abstractmethod
    def __init__(self):
        """
        BaseQuery, used to define the structure of any query being used, and the common
        properties.

        The basic functioning of a query should be to accept arguments from user to
        formulate the query internally, reject in case of false/wrong parameters.
        Finally, using these parameters, it should form a string containing the actual
        query that is to be used to perform the search.

        This string should consist of values for which the search is to be performed,
        as well as the parameters that are to be present in the response.
        """

        # Each child class will need to define its own query argument.
        self.__query = ""

    @property
    def query(self) -> str:
        return self.__query

    @query.setter
    def query(self, args: Any) -> None:
        # Query should not be modifiable externally.
        raise NotImplementedError
