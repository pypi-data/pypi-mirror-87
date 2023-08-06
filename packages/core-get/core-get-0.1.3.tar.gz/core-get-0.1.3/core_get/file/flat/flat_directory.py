from __future__ import annotations

from dataclasses import dataclass
from typing import List

from core_get.file.flat.flat_file import FlatFile


@dataclass
class FlatDirectory:
    files: List[FlatFile]

    def get_files(self) -> List[FlatFile]:
        return self.files

    def filter(self, patterns: List[str]) -> FlatDirectory:
        files = [file for file in self.files
                 if any(file.path.match(pattern) for pattern in patterns)]
        return FlatDirectory(files)
