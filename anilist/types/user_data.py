# Definition of a user.

from __future__ import annotations

from json import loads as json_load
from typing import Any
from typing import Dict, Union

from ..client import BaseObject


class UserAvatar(BaseObject):
    def __init__(self, large_avatar: str, medium_avatar: str):
        """
        Container to hold url to a users profile picture.

        Has URL for the large and medium version of the avatar.

        Args:
            large_avatar: String containing URL to large version of the avatar.
            medium_avatar: String containing URL to medium version of the avatar.
        """

        if not isinstance(large_avatar, str) or not isinstance(medium_avatar, str):
            raise TypeError

        if len(large_avatar) == 0 or len(medium_avatar) == 0:
            raise ValueError

        self.large = large_avatar
        self.medium = medium_avatar

    @staticmethod
    def initialize(data: Union[str, Dict[Any, Any]]) -> UserAvatar:
        if not isinstance(data, (dict, str)):
            raise TypeError

        if isinstance(data, str):
            # Can result in JSONDecode error if the string does not contain valid JSON
            final_data: Dict[Any, Any] = json_load(data)
        else:
            final_data = data

        return UserAvatar(
            large_avatar=final_data["large"], medium_avatar=final_data["medium"]
        )
