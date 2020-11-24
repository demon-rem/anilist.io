import logging as __logging
from logging import Logger as __Logger
from logging import getLogger

from anilist.client.anilist_client import Anilist

from . import errors

Logger: __Logger = getLogger()

# Modifying log configuration. configuration.
__logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filemode='a',
    filename='logs.txt'
)
