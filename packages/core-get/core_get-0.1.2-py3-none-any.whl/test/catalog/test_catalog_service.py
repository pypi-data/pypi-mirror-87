from pathlib import PurePath
from unittest import TestCase
from unittest.mock import Mock

from semver import VersionInfo

from core_get.catalog.catalog_service import CatalogService
from core_get.configuration.credentials import Credentials
from core_get.package.manifest import Manifest


class TestCatalogService(TestCase):

    def make_catalog_service(self, network_service) -> CatalogService:
        credentials_accessor = Mock()
        credentials_accessor.read = Mock(return_value=Credentials('access1234'))
        environment_settings = Mock()
        environment_settings.catalog_url = 'https://core-get.org'
        return CatalogService(credentials_accessor, environment_settings, network_service)

    def test_gets_latest_package_reference(self):
        manifest_2 = Manifest('my_package', VersionInfo.parse('2.0.0'), 'work', 'MyDevice10', [], None, {})
        manifest_3 = Manifest('my_package', VersionInfo.parse('3.0.0'), 'work', 'MyDevice10', [], None, {})
        response_json = {
            'versions': {
                '2.0.0': {'manifest': manifest_2.to_dict()},
                '3.0.0': {'manifest': manifest_3.to_dict()},
            },
        }
        network_service = Mock()
        network_service.get = Mock(return_value=response_json)
        catalog_service = self.make_catalog_service(network_service)
        ref = catalog_service.get_package_reference('my_package')
        self.assertEqual(manifest_3, ref.manifest)

    def test_downloads_correct_package(self):
        network_service = Mock()
        network_service.download_file = Mock(return_value=None)
        catalog_service = self.make_catalog_service(network_service)
        url = 'https://core-get.org/my_package.core'
        path = PurePath('./my_package.core')
        catalog_service.download_package(url, path)
        network_service.download_file.assert_called_once_with(url, path)

    def test_publish_package(self):
        response_json = {'result': 0}
        network_service = Mock()
        network_service.post = Mock(return_value=response_json)
        catalog_service = self.make_catalog_service(network_service)
        package_path = PurePath('./my_package.core')
        catalog_service.publish_package('my_package', package_path)
        network_service.post.assert_called_once_with('https://core-get.org/api/0/packages/my_package/versions',
                                                     headers={'AccessToken': 'access1234'},
                                                     files={'package': package_path})

    def test_yanks_package(self):
        response_json = {'result': 0}
        network_service = Mock()
        network_service.delete = Mock(return_value=response_json)
        catalog_service = self.make_catalog_service(network_service)
        catalog_service.yank_package('my_package', VersionInfo.parse('2.0.0'))
        network_service.delete.assert_called_once_with('https://core-get.org/api/0/packages/my_package/versions/2.0.0',
                                                       headers={'AccessToken': 'access1234'})
