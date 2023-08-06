from dataclasses import dataclass
from pathlib import PurePath

from injector import inject

from core_get.configuration.project_directory_finder import ProjectDirectoryManager
from core_get.configuration.serialization.toml_serializer import TomlSerializer
from core_get.file.file_system import FileSystem
from core_get.package.manifest import Manifest


@inject
@dataclass
class PackageManifestAccessor:
    file_system: FileSystem
    toml_serializer: TomlSerializer
    project_directory_finder: ProjectDirectoryManager

    def read(self) -> Manifest:
        manifest_data = self.file_system.read_file(self.get_manifest_path())
        return self.toml_serializer.from_bytes(manifest_data, Manifest)

    def write(self, manifest: Manifest) -> None:
        manifest_data = self.toml_serializer.to_bytes(manifest)
        self.file_system.write_file(self.get_manifest_path(), manifest_data)

    def get_manifest_path(self) -> PurePath:
        project_path = self.project_directory_finder.get_project_directory()
        return project_path / "Core.toml"
