import zipfile
from dataclasses import dataclass
from pathlib import PurePath
from typing import IO

from core_get.file.flat.flat_directory import FlatDirectory
from core_get.file.flat.flat_file import FlatFile


@dataclass
class ZipFlatFile(FlatFile):
    _zip_file: zipfile.ZipFile
    _zip_info: zipfile.ZipInfo

    def open(self, mode) -> IO[bytes]:
        return self._zip_file.open(self._zip_info.filename, mode=mode)

    @property
    def path(self) -> PurePath:
        return PurePath(self._zip_info.filename)

    @property
    def size(self) -> int:
        return self._zip_info.file_size


class ZipFlatDirectoryMaker:
    def make(self, zip_file: zipfile.ZipFile) -> FlatDirectory:
        zip_infos = [zip_info for zip_info in zip_file.infolist() if not zip_info.is_dir()]
        files = [ZipFlatFile(zip_file, zip_info) for zip_info in zip_infos]
        return FlatDirectory(files)
