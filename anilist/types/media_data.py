from __future__ import annotations

from json import loads as json_load
from typing import Union, Dict, Any, Optional

from . import MediaType, MediaTitle, MediaFormat
from ..client import BaseObject


class MediaData(BaseObject):
    def __init__(
        self,
        media_id: int,
        mal_id: Optional[int] = None,
        title: Optional[MediaTitle] = None,
        media_type: Optional[MediaType] = None,
        media_format: Optional[MediaFormat] = None,
    ):

        pass

    @staticmethod
    def initialize(data: Union[str, Dict[Any, Any]]) -> Any:
        if not isinstance(data, (str, dict)):
            raise TypeError

        if isinstance(data, str):
            final_data = json_load(data)
        else:
            final_data = data

        return MediaData(final_data.get("param", None))
