# Defines the base error class(es).

from typing import Optional, Dict


class BaseError(Exception):
    def __init__(
        self, status: int, message: str, locations: Optional[Dict[str, int]] = None
    ):
        """
        Base class for exceptions, defines the common behaviour.

        Args:
            status: Integer containing the error-code.
            message: String containing error message.
            locations: Dictionary of values/pairs specifying the line/column of where the error
            occurred.
        """

        if (
            not isinstance(status, int)
            or not isinstance(message, str)
            or (locations is not None and not isinstance(locations, Dict))
        ):
            raise TypeError("Incorrect data type")

        self.status = status
        self.message = message
        self.locations = locations

        super().__init__(
            f"RequestException {status}: {message} caused by {self.__class__.__name__}"
        )

    def __reduce__(self):
        return type(self), (self.status, self.message, self.locations)


class APIError(BaseError):
    """
    Enacts the base error, will be thrown if an API call is made with incorrect parameters.
    """

    def __init__(self, status: int, message: str, locations: Optional[Dict[str, int]]):
        super(APIError, self).__init__(
            status=status, message=message, locations=locations
        )
