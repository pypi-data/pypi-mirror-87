from __future__ import annotations

from dataclasses import dataclass
from pathlib import PurePath
from typing import Dict, IO


@dataclass
class FlatFile:
    def open(self, mode) -> IO[bytes]:
        raise NotImplementedError

    @property
    def path(self) -> PurePath:
        raise NotImplementedError

    @property
    def size(self) -> int:
        raise NotImplementedError


@dataclass
class Directory:
    files: Dict[str, FlatFile]
    directories: Dict[str, Directory]
