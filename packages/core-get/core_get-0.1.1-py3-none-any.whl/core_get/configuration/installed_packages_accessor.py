from dataclasses import dataclass
from pathlib import PurePath

from injector import inject

from core_get.configuration.installed_packages import InstalledPackages
from core_get.configuration.project_directory_finder import ProjectDirectoryManager
from core_get.configuration.serialization.toml_serializer import TomlSerializer
from core_get.file.file_system import FileSystem


@inject
@dataclass
class InstalledPackagesAccessor:
    file_system: FileSystem
    toml_serializer: TomlSerializer
    project_directory_manager: ProjectDirectoryManager

    def read(self) -> InstalledPackages:
        settings_data = self.file_system.read_file(self.get_settings_path())
        return self.toml_serializer.from_bytes(settings_data, InstalledPackages)

    def write(self, settings: InstalledPackages) -> None:
        settings_data = self.toml_serializer.to_bytes(settings)
        self.file_system.write_file(self.get_settings_path(), settings_data)

    def get_settings_path(self) -> PurePath:
        project_path = self.project_directory_manager.get_project_directory()
        return project_path / ".core-get.toml"
