from pathlib import PurePath
from unittest import TestCase
from unittest.mock import Mock

from core_get.package.manifest import Manifest
from core_get.package.modify.package_reference_path_resolver import PackageReferencePathResolver
from core_get.package.reference.package_reference import RemotePackageReference, LocalPackageReference


class TestPackageReferencePathResolver(TestCase):
    def test_resolve_remote_path_downloads_package_file(self):
        package_ref_1 = RemotePackageReference(Manifest('my_package_1'), 'https://localhost/package_ref_1')
        package_cache = Mock()
        package_cache.download_package = Mock(return_value=PurePath('./my_package_1.core'))
        package_reference_path_resolver = PackageReferencePathResolver(package_cache)
        package_references = [package_ref_1]
        package_paths = package_reference_path_resolver.resolve_paths(package_references)
        self.assertEqual({'my_package_1': PurePath('./my_package_1.core')}, package_paths)
        package_cache.download_package.assert_called_once_with(package_ref_1)

    def test_resolve_local_path_uses_existing_path(self):
        package_ref_1 = LocalPackageReference(Manifest('my_package_1'), PurePath('./my_package_1.core'))
        package_cache = Mock()
        package_reference_path_resolver = PackageReferencePathResolver(package_cache)
        package_references = [package_ref_1]
        package_paths = package_reference_path_resolver.resolve_paths(package_references)
        self.assertEqual({'my_package_1': PurePath('./my_package_1.core')}, package_paths)
