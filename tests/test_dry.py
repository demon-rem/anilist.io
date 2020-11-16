from .context import Anilist


def test_dry():
    result = Anilist().test()
    assert result == "Test run complete"
