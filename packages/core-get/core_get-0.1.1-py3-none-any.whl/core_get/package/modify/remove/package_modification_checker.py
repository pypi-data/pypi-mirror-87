from dataclasses import dataclass
from logging import getLogger
from pathlib import PurePath
from typing import List, Optional, NamedTuple

from core_get.file.hash import Hash
from injector import inject

from core_get.configuration.installed_packages import InstalledPackage
from core_get.configuration.project_directory_finder import ProjectDirectoryManager
from core_get.file.file_system import FileSystem

logger = getLogger(__name__)


class PackageModifications(NamedTuple):
    missing_files: List[PurePath]
    modified_files: List[PurePath]
    extra_file: List[PurePath]


@inject
@dataclass
class PackageModificationChecker:
    project_directory_manager: ProjectDirectoryManager
    file_system: FileSystem

    def check_modifications(self, installed_package: InstalledPackage) -> Optional[PackageModifications]:
        project_path = self.project_directory_manager.get_project_directory()
        package_path = installed_package.path

        missing_files = []
        modified_files = []
        for installed_file in installed_package.installed_files:
            try:
                h = Hash(self.file_system.read_file(project_path / installed_file.path))
                if h.digest() != installed_file.hash:
                    modified_files.append(installed_file.path.relative_to(package_path))
            except FileNotFoundError:
                missing_files.append(installed_file.path.relative_to(package_path))

        dir_files = {path.relative_to(project_path / package_path)
                     for path in self.file_system.glob(project_path / package_path, '**')}
        installed_files = {installed_file.path.relative_to(package_path)
                           for installed_file in installed_package.installed_files}
        extra_files = sorted(dir_files - installed_files)

        if missing_files or modified_files or extra_files:
            return PackageModifications(missing_files, modified_files, extra_files)

        return None
