# Using this file to setup stuff - perform import(s) from the source directory to make
# classes/methods available to the remaining tests.
#
# Any other file in the test suite can just import stuff from this file.

from os import path as os_path
from sys import path as sys_path

sys_path.insert(0, os_path.abspath(os_path.join(os_path.dirname(__file__), "..")))

# noinspection PyUnresolvedReferences
from src import Anilist
