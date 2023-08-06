from dataclasses import dataclass
from pathlib import PurePath

from injector import inject

from core_get.configuration.credentials import Credentials
from core_get.configuration.environment_settings import EnvironmentSettings
from core_get.configuration.serialization.toml_serializer import TomlSerializer
from core_get.file.file_system import FileSystem
from core_get.file.flat.flat_file import FlatFile


@inject
@dataclass
class CredentialsAccessor:
    file_system: FileSystem
    toml_serializer: TomlSerializer
    environment_settings: EnvironmentSettings

    def read(self) -> Credentials:
        credentials_data = self.file_system.read_file(self.get_credentials_path())
        return self.toml_serializer.from_bytes(credentials_data, Credentials)

    def write(self, credentials: Credentials) -> None:
        credentials_data = self.toml_serializer.to_bytes(credentials)
        self.file_system.write_file(self.get_credentials_path(), credentials_data)

    def get_credentials_path(self) -> FlatFile:
        return self.environment_settings.app_dir / "credentials.toml"
