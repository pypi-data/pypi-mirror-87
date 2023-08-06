from dataclasses import dataclass
from pathlib import PurePath

from core_get.options.options import Options


@dataclass
class InitOptions(Options):
    path: PurePath


