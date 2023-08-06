from dataclasses import dataclass
from pathlib import PurePath


@dataclass(frozen=True)
class ProjectSourceFile:
    path: PurePath
    library: str = 'work'
