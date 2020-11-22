# Defines objects that can't really be grouped on the basis of similarities.
from __future__ import annotations

from json import loads as json_load
from typing import Union, Dict, Any

from ..client.base_object import BaseObject


class FuzzyDate(BaseObject):
    def __init__(
        self,
        day: int = 0,
        month: int = 0,
        year: int = 0,
    ):
        """
        Defines a date.

        Notes:
            Any value not specified will default to zero.

        Args:
            day: Integer containing the date.
            month: Integer containing the month.
            year: Integer containing the year. Two digit numbers will be auto-mapped
            between 2000 - 2100.
        """

        if not all(isinstance(x, int) for x in [day, month, year]):
            # Throw type error if any variable is not integer.
            raise TypeError

        self.day = day
        self.month = month
        self.year = year if year > 100 or year == 0 else 2000 + year

    @staticmethod
    def initialize(data: Union[str, Dict[Any, Any]]) -> FuzzyDate:
        if not isinstance(data, (dict, str)):
            raise TypeError

        # Convert string into JSON-parsable dictionary.
        if isinstance(data, str):
            final_data = json_load(data)
        else:
            final_data = data

        return FuzzyDate(
            day=final_data["day"], month=final_data["month"], year=final_data["year"]
        )

    @property
    def fuzz(self) -> str:
        """
        Converts instance of this class into an API-friendly string. Designed to be
        used internally while making API calls.

        Returns:
            String containing the date represented by this object in `YYYYMMDD` format.
        """

        return (
            f"{str(self.year).zfill(4)}{str(self.month).zfill(2)}"
            f"{str(self.day).zfill(2)}"
        )
