# Defines objects that can't really be grouped on the basis of similarities.
from __future__ import annotations

from json import loads as json_load
from typing import Union, Dict, Any

from . import MediaData
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


class AiringSchedule(BaseObject):
    def __init__(
        self,
        airing_id: int,
        airing_at: int,
        time_left: int,
        episode: int,
        media_id: int,
        media: MediaData,
    ):
        """
        Media airing schedule

        Args:
            airing_id: Id of the airing schedule item
            airing_at: The time at which the episode airs
            time_left: Seconds remaining till the airing of the episode starts
            episode: The episode number which is to be aired
            media_id: Associated media id of the airing episode
            media: The media associated with the airing episode
        """

        # Type-check
        if not all(
            isinstance(x, int)
            for x in (airing_id, airing_at, time_left, episode, media_id)
        ) or not isinstance(media, MediaData):
            raise TypeError

        self.id = airing_id
        self.airingAt = airing_at
        self.timeUntilAiring = time_left
        self.episode = episode
        self.mediaId = media_id
        self.media = media

    @staticmethod
    def initialize(data: Union[str, Dict[Any, Any]]) -> AiringSchedule:
        if not isinstance(data, (str, dict)):
            raise TypeError

        if isinstance(data, str):
            final_data = json_load(data)
        else:
            final_data = data

        return AiringSchedule(
            airing_id=final_data["id"],
            airing_at=final_data["airingAt"],
            time_left=final_data["timeUntilAiring"],
            episode=final_data["episode"],
            media_id=final_data["mediaId"],
            media=MediaData.initialize(final_data["media"]),
        )
