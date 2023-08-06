from dataclasses import dataclass
from logging import getLogger
from pathlib import PurePath
from typing import Dict

from injector import inject
from semver import VersionInfo

from core_get.catalog.network_service import NetworkService, NetworkException
from core_get.configuration.credentials_accessor import CredentialsAccessor
from core_get.configuration.environment_settings import EnvironmentSettings
from core_get.package.manifest import Manifest
from core_get.package.reference.package_reference import RemotePackageReference

logger = getLogger(__name__)


@inject
@dataclass
class CatalogService:
    credentials_accessor: CredentialsAccessor
    environment_settings: EnvironmentSettings
    network_service: NetworkService

    def get_package_reference(self, package_name: str):
        package_url = f'{self.environment_settings.catalog_url}/api/0/packages/{package_name}'
        try:
            package_json = self.network_service.get(package_url)
        except NetworkException:
            return None
        manifests = [Manifest.from_dict(version['manifest'])
                     for version in package_json['versions'].values()]
        # TODO: Introduce version pinning and use semver.match to filter out valid versions
        manifest = max(manifests, key=lambda m: m.version)
        core_url = f'{package_url}/versions/{manifest.version}/{package_name}-{manifest.version}.core'
        return RemotePackageReference(manifest, core_url)

    # Adapted from https://stackoverflow.com/a/16696317
    def download_package(self, url: str, package_path: PurePath) -> None:
        self.network_service.download_file(url, package_path)

    def publish_package(self, package_name: str, package_path: PurePath) -> None:
        headers = self.get_access_headers()
        url = f'{self.environment_settings.catalog_url}/api/0/packages/{package_name}/versions'
        response_json = self.network_service.post(url, headers=headers, files={'package': package_path})

        if response_json.get('result', 1):
            error = response_json.get('error', None)
            if error is not None:
                logger.error(f"Error while publishing package: {error}")
            else:
                logger.error("Unknown error while publishing package")
            return

        logger.info(f"Published package {package_name} successfully")

    def get_access_headers(self) -> Dict[str, str]:
        credentials = self.credentials_accessor.read()
        access_token = credentials.access_token
        return {'AccessToken': access_token}

    def yank_package(self, package_name: str, version: VersionInfo) -> None:
        credentials = self.credentials_accessor.read()
        access_token = credentials.access_token
        url = f'{self.environment_settings.catalog_url}/api/0/packages/{package_name}/versions/{version}'
        headers = {'AccessToken': access_token}
        response_json = self.network_service.delete(url, headers=headers)

        if response_json.get('result', 1):
            error = response_json.get('error', None)
            if error is not None:
                logger.error(f"Error while yanking package: {error}")
            else:
                logger.error("Unknown error while yanking package")
            return

        logger.info(f"Yanked package {package_name} version {version} successfully")
