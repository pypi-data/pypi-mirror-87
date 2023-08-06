from dataclasses import dataclass

from semver import VersionInfo

from core_get.options.options import Options


@dataclass
class YankOptions(Options):
    version: VersionInfo
