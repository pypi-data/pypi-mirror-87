from pathlib import PurePath
from unittest import TestCase
from unittest.mock import Mock

from requests import HTTPError
from semver import VersionInfo

from core_get.package.manifest import Manifest
from core_get.package.modify.install.download_cache import DownloadCache
from core_get.package.reference.package_reference import RemotePackageReference


class TestDownloadCache(TestCase):
    def test_download_package_succeeds(self):
        catalog_service = Mock()
        catalog_service.download_package = Mock()
        environment_settings = Mock()
        environment_settings.cache_dir = PurePath('~/.core-get')
        file_system = Mock()
        file_system.make_directory = Mock()
        download_cache = DownloadCache(catalog_service, environment_settings, file_system)
        manifest = Manifest('my_package', VersionInfo(1))
        package_url = 'https://localhost/my_package.core'
        package_path = download_cache.download_package(RemotePackageReference(manifest, package_url))
        file_system.make_directory.assert_called_once_with(PurePath('~/.core-get'))
        self.assertEqual(PurePath('~/.core-get/my_package-1.0.0.core'), package_path)
        catalog_service.download_package.assert_called_once_with(package_url,
                                                                 PurePath('~/.core-get/my_package-1.0.0.core'))

    def test_download_package_fails(self):
        catalog_service = Mock()
        catalog_service.download_package = Mock(side_effect=HTTPError(404))
        environment_settings = Mock()
        environment_settings.cache_dir = PurePath('~/.core-get')
        file_system = Mock()
        file_system.make_directory = Mock()
        download_cache = DownloadCache(catalog_service, environment_settings, file_system)
        manifest = Manifest('my_package', VersionInfo(1))
        package_url = 'https://localhost/my_package.core'
        with self.assertRaises(HTTPError):
            download_cache.download_package(RemotePackageReference(manifest, package_url))
