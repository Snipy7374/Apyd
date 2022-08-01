__title__ = 'apyd'
__author__ = 'Snipy'
__license__ = 'MIT'
__version__ = '0.0.1a'

from typing import NamedTuple, Literal
from .image import *
from .http import *
from .errors import *
from .__main__ import *

class VersionInfo(NamedTuple):
  major: int
  minor: int
  micro: int
  releaselevel: Literal["alpha", "beta", "candidate", "final"]
  serial: int

version_info: VersionInfo = VersionInfo(major=0, minor=0, micro=1, releaselevel='alpha', serial=0)