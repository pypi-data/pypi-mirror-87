import os
import zipfile
from dataclasses import dataclass
from logging import getLogger
from pathlib import PurePath

from injector import inject

from core_get.file.flat.disk_flat import DiskFlatDirectoryMaker
from core_get.file.flat.flat_directory import FlatDirectory
from core_get.file.flat.zip_flat import ZipFlatDirectoryMaker

logger = getLogger(__name__)


@inject
@dataclass
class FlatDirectoryMaker:
    disk_flat_directory_maker: DiskFlatDirectoryMaker
    zip_flat_directory_maker: ZipFlatDirectoryMaker

    def make_flat_directory(self, path: PurePath) -> FlatDirectory:
        if os.path.isfile(path):
            if zipfile.is_zipfile(path):
                zip_file = zipfile.ZipFile(path)
                logger.info(f'Reading zip package {path}')
                return self.zip_flat_directory_maker.make(zip_file)
            else:
                logger.error(f'File {path} is not a zip file')
                raise ValueError
        elif os.path.isdir(path):
            logger.info(f'Reading directory package {path}')
            return self.disk_flat_directory_maker.make(path)
        else:
            logger.error(f'Package at {path} not found')
            raise ValueError
