# Defines classes used to perform media queries.

from typing import Optional, List

from anilist.types import (
    FuzzyDate,
    MediaSeason,
    MediaType,
    MediaStatus,
    MediaFormat,
    MediaSource,
    MediaSort,
)


class MediaQuery:
    def __init__(
        self,
        title: Optional[str] = None,
        media_id: Optional[int] = None,
        id_not: Optional[int] = None,
        id_in: Optional[List[int]] = None,
        id_not_in: Optional[List[int]] = None,
        idMal: Optional[int] = None,
        idMal_not: Optional[int] = None,
        idMal_in: Optional[List[int]] = None,
        idMal_not_in: Optional[List[int]] = None,
        startDate: Optional[FuzzyDate] = None,
        startDate_like: Optional[str] = None,
        startDate_greater: Optional[FuzzyDate] = None,
        startDate_lesser: Optional[FuzzyDate] = None,
        endDate: Optional[FuzzyDate] = None,
        endDate_like: Optional[str] = None,
        endDate_greater: Optional[FuzzyDate] = None,
        endDate_lesser: Optional[FuzzyDate] = None,
        season: Optional[MediaSeason] = None,
        seasonYear: Optional[int] = None,
        media_type: Optional[MediaType] = None,
        status: Optional[MediaStatus] = None,
        status_not: Optional[MediaStatus] = None,
        status_in: Optional[List[MediaStatus]] = None,
        status_not_in: Optional[List[MediaStatus]] = None,
        episodes: Optional[int] = None,
        episodes_greater: Optional[int] = None,
        episodes_lesser: Optional[int] = None,
        duration: Optional[int] = None,
        duration_greater: Optional[int] = None,
        duration_lesser: Optional[int] = None,
        chapters: Optional[int] = None,
        chapters_greater: Optional[int] = None,
        chapters_lesser: Optional[int] = None,
        volumes: Optional[int] = None,
        volumes_greater: Optional[int] = None,
        volumes_lesser: Optional[int] = None,
        isAdult: Optional[bool] = None,
        genre: Optional[str] = None,
        genre_in: Optional[List[str]] = None,
        genre_not_in: Optional[List[str]] = None,
        tag: Optional[str] = None,
        tag_in: Optional[List[str]] = None,
        tag_not_in: Optional[List[str]] = None,
        minimumTagRank: Optional[str] = None,
        tagCategory: Optional[str] = None,
        tagCategory_in: Optional[List[str]] = None,
        tagCategory_not_in: Optional[List[str]] = None,
        onList: Optional[bool] = None,
        averageScore: Optional[int] = None,
        averageScore_not: Optional[int] = None,
        averageScore_greater: Optional[int] = None,
        averageScore_lesser: Optional[int] = None,
        popularity: Optional[int] = None,
        popularity_not: Optional[int] = None,
        popularity_greater: Optional[int] = None,
        popularity_lesser: Optional[int] = None,
        source: Optional[MediaSource] = None,
        source_in: Optional[List[MediaSource]] = None,
        country_origin: Optional[str] = None,
        media_format: Optional[MediaFormat] = None,
        format_in: Optional[List[MediaFormat]] = None,
        format_not: Optional[MediaFormat] = None,
        format_not_in: Optional[List[MediaFormat]] = None,
        licensedBy: Optional[str] = None,
        licensedBy_in: Optional[List[str]] = None,
        sort: Optional[List[MediaSort]] = None,
    ):
        """
        Instance of a media-query. Used to perform a search for media.

        Media includes Anime, Manga, Light Novel, and everything else. This is one of
        the most basic types of searches that can be performed.

        In order to perform a search, individual parameters in this class can be filled
        with the required values. Searches can also be limited to get narrowed, and
        more specific results.

        For example, if you already have the ID of a media from MyAnimeList (referred
        to as `mal`), you can form a query using the same by filling the `idMal`
        parameter with the required values

        Notes:
            - All arguments are optional.
            - Atleast one argument must be filled to perform a search.


        Args:
            title: String containing the title to search for. Can be the name of an
                anime/manga/special, etc. Results can be narrowed down using other
                parameters.

            media_id: Filter media using its ID on Anilist.
            id_not: Filter media using its ID on Anilist.
            id_in: Filter media using its ID on Anilist.
            id_not_in: Filter media using its ID on Anilist.

            idMal: Filter media using its ID on MyAnimeList
            idMal_not: Filter media using its ID on MyAnimeList
            idMal_in: Filter media using its ID on MyAnimeList
            idMal_not_in: Filter media using its ID on MyAnimeList

            startDate: Filter media using its start date.
            startDate_like: Filter media using its start date.
            startDate_greater: Filter media using its start date.
            startDate_lesser: Filter media using its start date.

            endDate: Filter media using its end date.
            endDate_like: Filter media using its end date.
            endDate_greater: Filter media using its end date.
            endDate_lesser: Filter media using its end date.

            season: Filter media using the season it was released in.
            seasonYear: The year in which the media was released. Note: The parameter
                `season` should be filled in order to use this parameter.

            media_type: Filter media by its type.

            status: Filter media by its current release status.
            status_not: Filter media by its current release status.
            status_in: Filter media by its current release status.
            status_not_in: Filter media by its current release status.

            episodes: Filter media by the amount of episodes it has.
            episodes_greater: Filter media by the amount of episodes it has.
            episodes_lesser: Filter media by the amount of episodes it has.

            duration: Filter media by the length of an episode
            duration_greater: Filter media by the length of an episode
            duration_lesser: Filter media by the length of an episode

            chapters: Filter media by the number of chapters present.
            chapters_greater: Filter media by the number of chapters present.
            chapters_lesser: Filter media by the number of chapters present.

            volumes: Filter media by the number of volumes present.
            volumes_greater: Filter media by the number of volumes present.
            volumes_lesser: Filter media by the number of volumes present.

            isAdult: Filter media on the based on if it is adult or not.

            genre: Filter media by the genre it belongs to.
            genre_in: Filter media by the genre it belongs to.
            genre_not_in: Filter media by the genre it belongs to.

            tag: Filter media using its tag.
            tag_in: Filter media using its tag.
            tag_not_in: Filter media using its tag.

            minimumTagRank: Apply tags filter argument to tags above this rank.
            onList: Filter by the media on an authenticated user's list. Works with
            authentication. Not implemented yet.

            tagCategory: Filter by the media's tags in the tag category.
            tagCategory_in: Filter by the media's tags in the tag category.
            tagCategory_not_in: Filter by the media's tags in the tag category.

            averageScore: Filter by the media's average score.
            averageScore_not: Filter by the media's average score.
            averageScore_greater: Filter by the media's average score.
            averageScore_lesser: Filter by the media's average score.

            popularity: Filter by amount of users having this media on their list.
            popularity_not: Filter by amount of users having this media on their list.
            popularity_greater: Filter by amount of users having this media on their
                list.
            popularity_lesser: Filter by amount of users having this media on their list

            source: Filter by the source type of the media.
            source_in: Filter by the source type of the media.
            country_origin: Filter by the media's country of origin.

            media_format: Filter by the media's format.
            format_in: Filter by the media's format.
            format_not: Filter by the media's format.
            format_not_in: Filter by the media's format.

            licensedBy: Filter media by sites with online streaming/reading license
            licensedBy_in: Filter media by sites with online streaming/reading license
            sort: The order in which the results are to be returned.
        """
        pass
