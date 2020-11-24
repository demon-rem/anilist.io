from __future__ import annotations

from json import loads as json_load
from typing import Union, Dict, Any, Optional

from . import MediaFormat, MediaRankType, MediaSeason
from ..client import BaseObject


class MediaTitle(BaseObject):
    def __init__(self, romanji: str, english: str, native: str, user_preferred: str):
        """
        The official titles of the media in various languages.

        Args:
            romanji: Romanization of the native language title.
            english: The official english title.
            native: Official title in its native language.
            user_preferred: Title in the users preferred language. Authenticated users
            only, will default to romanji for non-authenticated users.
        """

        # Type-check
        if not all(
            isinstance(x, str) for x in (romanji, english, native, user_preferred)
        ):
            raise TypeError

        # Assigning the values to object - the instance-variables are named such that
        # they can be mapped back using `stringify` method.
        self.romaji = romanji
        self.english = english
        self.native = native
        self.userPreferred = user_preferred

    @staticmethod
    def initialize(data: Union[str, Dict[Any, Any]]) -> MediaTitle:
        if not isinstance(data, (str, dict)):
            # Type-check
            raise TypeError

        if isinstance(data, str):
            final_data = json_load(data)
        else:
            final_data = data

        return MediaTitle(
            romanji=final_data["romaji"],
            english=final_data["english"],
            native=final_data["native"],
            user_preferred=final_data["userPreferred"],
        )


class MediaTrailer(BaseObject):
    def __init__(self, trailer_id: str, site: str, thumbnail: str):
        """
        Media trailer, or advertisement

        Args:
            trailer_id: Video id for the trailer video.
            site: Name of the site where the video is hosted at.
            thumbnail: Direct url to fetch thumbnail for the trailer.
        """

        if not all(isinstance(x, str) for x in (trailer_id, site, thumbnail)):
            raise TypeError

        self.id = trailer_id
        self.site = site
        self.thumbnail = thumbnail

    @staticmethod
    def initialize(data: Union[str, Dict[Any, Any]]) -> MediaTrailer:
        if not isinstance(data, (str, dict)):
            raise TypeError

        if isinstance(data, str):
            final_data = json_load(data)
        else:
            final_data = data

        return MediaTrailer(
            trailer_id=final_data["id"],
            site=final_data["site"],
            thumbnail=final_data["thumbnail"],
        )


class MediaPoster(BaseObject):
    def __init__(
        self, large: str, medium: str, color: str, extra_large: Optional[str] = None
    ):
        """
        Poster for the media.

        Args:
            extra_large: Url to extra large cover image. Not all media may have this
            large: Url to the large version of the media cover image
            medium: Url to the medium version of the media cover image
            color: Average hex color value for the media cover image
        """

        # Type check
        if not all(isinstance(x, str) for x in (large, medium, color)):
            raise TypeError

        # Separate type-check for extra large - it can be empty.
        if extra_large is not None and not isinstance(extra_large, str):
            raise TypeError

        self.extraLarge = extra_large
        self.large = large
        self.medium = medium
        self.color = color

    @staticmethod
    def initialize(data: Union[str, Dict[Any, Any]]) -> Any:
        if not isinstance(data, (str, dict)):
            raise TypeError

        if isinstance(data, str):
            final_data = json_load(data)
        else:
            final_data = data

        return MediaPoster(
            extra_large=final_data.get("extraLarge", None),
            large=final_data["large"],
            medium=final_data["medium"],
            color=final_data["color"],
        )


class MediaTag(BaseObject):
    def __init__(
        self,
        media_id: int,
        name: str,
        description: str,
        category: str,
        rank: int,
        general_spoiler: bool,
        media_spoiler: bool,
        adult: bool,
    ):
        """
        Tag describing the theme or element of media.

        Args:
            media_id: Tag id.
            name: Name of the tag.
            description: String containing a general description of the tag.
            category: The category of tags of which this tag is a part.
            rank: Relevance ranking tag out of 100 for this media.
            general_spoiler: Boolean denoting if the tag could be spoiler for any media
            media_spoiler: Boolean denoting if the tag could be a spoiler for this media
            adult: Boolean indicating if this tag is only for adult media.
        """

        # Type-check
        if (
            not all(isinstance(x, str) for x in (name, description, category))
            or not all(isinstance(x, int) for x in (media_id, rank))
            or not all(
                isinstance(x, bool) for x in (general_spoiler, media_spoiler, adult)
            )
        ):
            raise TypeError

        self.id = media_id
        self.name = name
        self.description = description
        self.category = category
        self.rank = rank
        self.isGeneralSpoiler = general_spoiler
        self.isMediaSpoiler = media_spoiler
        self.isAdult = adult

    @staticmethod
    def initialize(data: Union[str, Dict[Any, Any]]) -> MediaTag:
        if not isinstance(data, (str, dict)):
            raise TypeError

        if isinstance(data, str):
            final_data = json_load(data)
        else:
            final_data = data

        return MediaTag(
            media_id=final_data["id"],
            name=final_data["name"],
            description=final_data["description"],
            category=final_data["category"],
            rank=final_data["rank"],
            general_spoiler=final_data["isGeneralSpoiler"],
            media_spoiler=final_data["isMediaSpoiler"],
            adult=final_data["isAdult"],
        )


class MediaExternalLink(BaseObject):
    def __init__(self, link_id: int, url: str, site: str):
        """
        External link to another site related to the media.

        Args:
            link_id: Id for the external link
            url: String containing url of the external link
            site: Text containing title of the site - can be used to make a hyperlink
        """

        # Type-check
        if not all(isinstance(x, str) for x in (url, site)) or not isinstance(
            link_id, int
        ):
            raise TypeError

        self.id = link_id
        self.url = url
        self.site = site

    @staticmethod
    def initialize(data: Union[str, Dict[Any, Any]]) -> MediaExternalLink:
        if not isinstance(data, (str, dict)):
            raise TypeError

        if isinstance(data, str):
            final_data = json_load(data)
        else:
            final_data = data

        return MediaExternalLink(
            link_id=final_data["id"], url=final_data["url"], site=final_data["site"]
        )


class MediaStreamingEpisode(BaseObject):
    def __init__(self, title: str, thumbnail: str, url: str, site: str):
        """
        Data and links to legal streaming episodes on external sites.s

        Args:
            title: Title of the episode.
            thumbnail: Url for the episode image thumbnail.
            url: Url to the external site.
            site: Site location of the streaming episodes.
        """

        if not all(isinstance(x, str) for x in (title, thumbnail, url, site)):
            raise TypeError

        self.title = title
        self.thumbnail = thumbnail
        self.url = url
        self.site = site

    @staticmethod
    def initialize(data: Union[str, Dict[Any, Any]]) -> MediaStreamingEpisode:
        if not isinstance(data, (str, dict)):
            raise TypeError

        if isinstance(data, str):
            final_data = json_load(data)
        else:
            final_data = data

        return MediaStreamingEpisode(
            title=final_data["title"],
            thumbnail=final_data["thumbnail"],
            url=final_data["url"],
            site=final_data["site"],
        )


class MediaRank(BaseObject):
    def __init__(
        self,
        rank_id: int,
        rank: int,
        rank_type: MediaRankType,
        media_format: MediaFormat,
        year: int,
        season: MediaSeason,
        all_time: bool,
        context: str,
    ):
        """
        The ranking of a media in a particular time-span and format, compared to other
        media

        Args:
            rank_id: Rank id.
            rank: Rank of the media.
            rank_type: The type of ranking
            media_format: The format within which the media is ranked
            year: The year the media is ranked within
            season: The season the media is ranked within
            all_time: Boolean indicating if the ranking is based on all time instead.
            context: String supplying context to ranking type and span.
        """

        if (
            not all(isinstance(x, int) for x in (rank, rank_id, year))
            or not isinstance(rank_type, MediaRankType)
            or not isinstance(media_format, MediaFormat)
            or not isinstance(season, MediaSeason)
            or not isinstance(all_time, bool)
            or not isinstance(context, str)
        ):
            raise TypeError

        self.id = rank_id
        self.rank = rank
        self.type = rank_type
        self.format = media_format
        self.year = year
        self.season = season
        self.allTime = all_time
        self.context = context

    @staticmethod
    def initialize(data: Union[str, Dict[Any, Any]]) -> MediaRank:
        if not isinstance(data, (str, dict)):
            raise TypeError

        if isinstance(data, str):
            final_data = json_load(data)
        else:
            final_data = data

        return MediaRank(
            rank_id=final_data["id"],
            rank=final_data["rank"],
            rank_type=MediaRankType.map(MediaRankType, final_data["type"]),
            media_format=MediaFormat.map(MediaFormat, final_data["format"]),
            year=final_data["year"],
            season=MediaSeason.map(MediaSeason, final_data["season"]),
            all_time=final_data["allTime"],
            context=final_data["context"],
        )


class MediaData(BaseObject):
    def __init__(self, param: int):
        self.param = param

    @staticmethod
    def initialize(data: Union[str, Dict[Any, Any]]) -> Any:
        if not isinstance(data, (str, dict)):
            raise TypeError

        if isinstance(data, str):
            final_data = json_load(data)
        else:
            final_data = data

        return MediaData(param=final_data["param"])
