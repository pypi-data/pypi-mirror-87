from dataclasses import dataclass
from pathlib import PurePath

from injector import inject

from core_get.catalog.catalog_service import CatalogService
from core_get.configuration.environment_settings import EnvironmentSettings
from core_get.file.file_system import FileSystem
from core_get.package.reference.package_reference import RemotePackageReference


@inject
@dataclass
class DownloadCache:
    catalog_service: CatalogService
    environment_settings: EnvironmentSettings
    file_system: FileSystem

    def download_package(self, reference: RemotePackageReference) -> PurePath:
        package_filename = reference.manifest.qualified_name() + '.core'
        package_path = self.environment_settings.cache_dir / package_filename
        self.file_system.make_directory(self.environment_settings.cache_dir)
        self.catalog_service.download_package(reference.url, package_path)
        return package_path
