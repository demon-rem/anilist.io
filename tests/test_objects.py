# Tests all the base objects.

from inspect import getmembers, isabstract, isclass
from json import loads

from pytest import raises
from tests.commons import bruteforce_exception, catch, check_initialize

from . import LOGGER


def test_base_object():
    from dataclasses import dataclass

    from anilist.client.base_object import BaseObject

    # Ensure that an abstract class can't be instantiated.
    catch(TypeError, BaseObject)

    # Making the class *forget* it has abstract methods - testing an abstract method.
    # Used to check the remaining methods of base class.
    BaseObject.__abstractmethods__ = set()

    @dataclass
    class dummy(BaseObject):
        pass

    # The method return a JSON string with all the values stored in the class - since
    # this object does not contain any, the string will be an empty dictionary
    result = dummy()
    assert result.stringify() == "{}"
    assert result.stringify(None) == "{}"

    catch(NotImplementedError, dummy.initialize, "")

    with raises(TypeError):
        # noinspection PyTypeChecker
        result.stringify("")


def test_base_enum():
    from enum import auto

    from anilist.client import BaseEnum

    # Making the abstract class forget it has any abstract methods.
    BaseEnum.__abstractmethods__ = set()

    # Creating a temporary enum with a single value
    class Child(BaseEnum):
        test_val = auto()

    child = Child(1)  # Will map to the only value in the enum - `test_val`

    # Type-checking the map function
    for var in [(None, None), (2, 2.0), ("", {}), ("a", "a")]:
        catch(TypeError, child.map, *var)

    # Ensuring that a key that doesn't map raises an error.
    catch(ValueError, child.map, Child, "this-key-won't-map")

    # A valid key can be mapped
    assert child.test_val == child.map(Child, Child.test_val.translate)


# noinspection PyTypeChecker
def test_user_avatar():
    from anilist.types.user_data import UserAvatar

    # Links should always be stored as strings.
    with raises(TypeError):
        UserAvatar(None, None)

    # Link to user avatar should not be a blank string.
    with raises(ValueError):
        UserAvatar("", "")

    # Instantiating to use this for tests
    avatar = UserAvatar(
        large_avatar="large avatar link", medium_avatar="medium avatar link"
    )

    # Validating the result of stringify with the result of initialize
    assert (
        avatar.stringify()
        == UserAvatar.initialize(avatar.stringify()).stringify()
        == UserAvatar.initialize(loads(avatar.stringify())).stringify()
    )


def test_fuzzy_date():
    from anilist.types import FuzzyDate

    # Type-check
    bruteforce_exception(TypeError, FuzzyDate, param=["", None, 2.0])
    catch(TypeError, FuzzyDate.initialize, None)

    date = FuzzyDate(13, year=1990)
    assert date.day == 13
    assert date.month == 0
    assert date.year == 1990

    # Ensuring the date can be mapped to API-friendly value - will be YYYYMMDD format
    assert date.fuzz == "19900013"

    # Attempting to create another fuzzy-date object by fetching JSON from the first.
    assert (
        date.stringify()
        == FuzzyDate.initialize(date.stringify()).stringify()
        == FuzzyDate.initialize(loads(date.stringify())).stringify()
    )

    # Ensuring that two digit numbers are auto-mapped.
    temp = FuzzyDate(year=13)
    assert temp.year == 2013


def test_airing():
    from anilist.types import AiringSchedule, MediaData

    # Type-check
    bruteforce_exception(TypeError, AiringSchedule, param=[None, 2, 3, 4, 5, None])

    schedule = AiringSchedule(
        airing_id=10,
        airing_at=10,
        time_left=10,
        episode=10,
        media_id=19,
        media=MediaData(10),
    )

    # Verifying `initialize` works with dictionary as well as string.
    assert (
        schedule.stringify()
        == AiringSchedule.initialize(schedule.stringify()).stringify()
        == AiringSchedule.initialize(loads(schedule.stringify())).stringify()
    )


def test_media_enums():
    from anilist.types import (
        MediaFormat,
        MediaRankType,
        MediaSeason,
        MediaSort,
        MediaSource,
        MediaStatus,
        MediaType,
    )

    # Iterating through all entries present in the enum, asserting that stringify
    # method works for them, `__members__` returns a dictionary of name - in string
    # and the value, for every value present in the enum.
    for x in (
        MediaSeason,
        MediaFormat,
        MediaStatus,
        MediaSource,
        MediaSort,
        MediaType,
        MediaRankType,
    ):
        for enum_str, enum in x.__members__.items():
            if isinstance(enum, MediaSort):
                catch(NotImplementedError, enum.stringify)
                continue  # Jump to the next iteration.

            assert isinstance(enum.stringify(), str)
            assert enum.stringify() == enum.translate


def test_generic_objects():
    # Performs a test on all (public) classes that derive from `BaseObject`.
    # Tests for the common functionality.

    from anilist import types
    from anilist.client import BaseObject

    LOGGER.info(f"Running generic tests on children of base class")

    child_class: BaseObject
    class_name: str

    # Looping over all objects present in the `types` module, checking if the object
    # is a class, derives from BaseClass and ensuring that it isn't abstract, if all
    # these flags pass, moving on to running generic tests on the object.
    for class_name, child_class in getmembers(
        types, lambda o: isclass(o) and issubclass(o, BaseObject) and not isabstract(o)
    ):
        # Child class will be a tuple, with the first element in the tuple being a
        # string containing the name of the class, and the second element in the tuple
        # being the actual class object against which the tests are to be run.
        LOGGER.info(f"Generic testing; `{class_name}`")

        for var in (None, 3, 2.0, [], ()):
            # Ensuring that data type other than a dictionary and a string are rejected.
            catch(TypeError, child_class.initialize, var)


# noinspection PyTypeChecker
def test_media_data():
    from anilist.types import (
        MediaData,
        MediaExternalLink,
        MediaFormat,
        MediaListStatus,
        MediaPoster,
        MediaRank,
        MediaRankType,
        MediaSeason,
        MediaStats,
        MediaStatus,
        MediaStreamingEpisode,
        MediaTag,
        MediaTitle,
        MediaTrailer,
        ScoreDistribution,
        StatusDistribution,
    )

    bruteforce_exception(TypeError, MediaTitle, param=[None, "", "", ""])
    bruteforce_exception(TypeError, MediaTrailer, param=[None, "", ""])
    bruteforce_exception(TypeError, MediaPoster, param=("", "", 2, ""))
    bruteforce_exception(TypeError, MediaPoster, param=("", "", 2, None))
    bruteforce_exception(TypeError, MediaTag, param=(2, "", "", "", 3, "", None, None))
    bruteforce_exception(TypeError, MediaExternalLink, param=(None, "", ""))
    bruteforce_exception(TypeError, MediaStreamingEpisode, param=(None, "", "", ""))
    bruteforce_exception(TypeError, MediaData, param=(""))
    bruteforce_exception(TypeError, ScoreDistribution, param=[None, 10])
    bruteforce_exception(
        TypeError, MediaRank, param=(None, None, "", None, 2, "", False, "")
    )

    bruteforce_exception(
        TypeError,
        MediaStats,
        param=[
            ScoreDistribution(1, 2),
            StatusDistribution(MediaListStatus.CURRENT, 12),
        ],
    )

    bruteforce_exception(
        TypeError, StatusDistribution, param=[MediaStatus.FINISHED, None]
    )

    assert check_initialize(MediaTitle("romaji", "english", "native", "user_preferred"))
    assert check_initialize(MediaTrailer("trailer_id", "test_site", "thumbnail"))
    assert check_initialize(MediaPoster("large", "medium", "color", "extra_large"))
    assert check_initialize(MediaExternalLink(10, "link_url", "site_url"))
    assert check_initialize(MediaStreamingEpisode("title", "thumbnail", "url", "site"))
    assert check_initialize(ScoreDistribution(13, 25))
    assert check_initialize(StatusDistribution(MediaListStatus.CURRENT, 12))
    assert check_initialize(
        MediaRank(
            12,
            10,
            MediaRankType.POPULAR,
            MediaFormat.MOVIE,
            1992,
            MediaSeason.WINTER,
            False,
            "",
        )
    )

    assert check_initialize(
        MediaStats(
            [ScoreDistribution(15, 20)],
            [StatusDistribution(MediaListStatus.PAUSED, 20)],
        )
    )

    assert check_initialize(
        MediaTag(13, "name", "description", "category", 10, False, True, False)
    )
