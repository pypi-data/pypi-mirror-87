from dataclasses import dataclass
from pathlib import Path, PurePath
from typing import IO

from core_get.file.flat.flat_file import FlatFile
from core_get.file.flat.flat_directory import FlatDirectory


@dataclass
class DiskFlatFile(FlatFile):
    _path: Path
    _rel_path: PurePath

    def open(self, mode) -> IO[bytes]:
        return self._path.open(mode=mode)

    @property
    def path(self) -> PurePath:
        return self._rel_path

    @property
    def size(self) -> int:
        return self._path.stat().st_size


class DiskFlatDirectoryMaker:

    def make(self, root_path: PurePath) -> FlatDirectory:
        paths = Path(root_path).rglob('*')
        files = [DiskFlatFile(path, path.relative_to(root_path))
                 for path in paths]
        return FlatDirectory(files)
