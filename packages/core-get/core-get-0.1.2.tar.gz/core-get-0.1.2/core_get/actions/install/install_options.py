from dataclasses import dataclass
from typing import List

from core_get.options.options import Options


@dataclass
class InstallOptions(Options):
    package_names: List[str]
