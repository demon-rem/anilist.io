# Defines objects pertaining to data regarding media type

from __future__ import annotations

from enum import auto
from typing import Union

from ..client import BaseEnum


class MediaSeason(BaseEnum):
    """
    Enum representing available media seasons.
    """

    # Note, the names of these variables should the same as the ones
    WINTER = auto()
    SPRING = auto()
    SUMMER = auto()
    FALL = auto()

    def stringify(self: MediaSeason, indent: Union[int, None] = 4) -> str:
        return f'"season": "{self.translate}"'


class MediaFormat(BaseEnum):
    """
    Enum representing available media formats.
    """

    TV = auto()
    TV_SHORT = auto()
    MOVIE = auto()
    SPECIAL = auto()
    OVA = auto()
    ONA = auto()
    MUSIC = auto()
    MANGA = auto()
    NOVEL = auto()
    ONE_SHOT = auto()

    def stringify(self, indent: Union[int, None] = 4) -> str:
        return f'"format": "{self.translate}"'


class MediaStatus(BaseEnum):
    """
    Enum representing available media status.
    """

    FINISHED = auto()
    RELEASING = auto()
    NOT_RELEASED = auto()  # Mapping this one internally
    CANCELLED = auto()
    HIATUS = auto()

    def stringify(self, indent: Union[int, None] = 4) -> str:
        return f'"status": "{self.translate}"'

    @property
    def translate(self):
        """
        Maps an enum key to an appropriate value. Used to convert an enum entry into a
        string - used while making the final API call.

        Notes:
            Overridden method. The variable 'NOT_RELEASED' should actually have been
            'NOT_YET_RELEASED' - but the name looked pretty ugly.

            As a result, the variable name is slightly modified, and the mapping is
            changed by overriding this method to ensure that correct value is being
            sent while making API calls.

        Returns:
            String containing the name of the enum entry in upper case.
        """

        if self != MediaStatus.NOT_RELEASED:
            # Passing the flow-of-control to the parent method.
            return super(MediaStatus, self).translate
        else:
            # An exception, a variable with this named looks ugly - mapping it
            # internally.
            return "NOT_YET_RELEASED"


class MediaSource(BaseEnum):
    """
    Enum representing available media sources.
    """

    ORIGINAL = auto()
    MANGA = auto()
    LIGHT_NOVEL = auto()
    VISUAL_NOVEL = auto()
    VIDEO_GAME = auto()
    NOVEL = auto()
    DOUJINSHI = auto()
    ANIME = auto()

    def stringify(self, indent: Union[int, None] = 4) -> str:
        return f'"source": "{self.translate}"'


class MediaSort(BaseEnum):
    """
    Enum representing available media sorts.

    Notes:
        Does not implement `stringify` method - this object is not a part of the API
        Response, and so does not implement the `stringify` method.
    """

    ID = auto()
    ID_DESC = auto()
    TITLE_ROMANJI = auto()
    TITLE_ROMANJI_DESC = auto()
    TITLE_ENGLISH = auto()
    TITLE_ENGLISH_DESC = auto()
    TITLE_NATIVE = auto()
    TITLE_NATIVE_DESC = auto()
    TYPE = auto()
    TYPE_DESC = auto()
    FORMAT = auto()
    FORMAT_DESC = auto()
    START_DATE = auto()
    START_DATE_DESC = auto()
    END_DATE = auto()
    END_DATE_DESC = auto()
    SCORE = auto()
    SCORE_DESC = auto()
    POPULARITY = auto()
    POPULARITY_DESC = auto()
    TRENDING = auto()
    TRENDING_DESC = auto()
    EPISODES = auto()
    EPISODES_DESC = auto()
    DURATION = auto()
    DURATION_DESC = auto()
    STATUS = auto()
    STATUS_DESC = auto()
    CHAPTERS = auto()
    CHAPTERS_DESC = auto()
    VOLUMES = auto()
    VOLUMES_DESC = auto()
    UPDATED_AT = auto()
    UPDATED_AT_DESC = auto()
    FAVOURITES = auto()
    FAVOURITES_DESC = auto()
    SEARCH_MATCH = auto()

    def stringify(self, indent: Union[int, None] = 4) -> None:
        raise NotImplementedError("Attempt to stringify an API parameter")
