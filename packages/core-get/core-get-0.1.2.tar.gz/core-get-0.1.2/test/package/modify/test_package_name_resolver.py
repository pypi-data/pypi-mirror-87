from pathlib import PurePath
from unittest import TestCase
from unittest.mock import Mock

from core_get.package.manifest import Manifest
from core_get.package.modify.package_name_resolver import PackageNameResolver, PackageNotFoundException
from core_get.package.reference.package_reference import LocalPackageReference, RemotePackageReference, \
    InstalledPackageReference


class Test(TestCase):
    def test_name_resolver_resolves_local_name(self):
        ref = LocalPackageReference(Manifest('my_package'), PurePath('./my_package.core'))
        local_reference_maker = Mock()
        local_reference_maker.make = Mock(return_value=ref)
        catalog_service = Mock()
        name_resolver = PackageNameResolver(local_reference_maker, catalog_service, set())
        resolved_ref = name_resolver.resolve('./my_package.core')
        self.assertEqual(ref, resolved_ref)

    def test_name_resolver_resolves_remote_name(self):
        ref = RemotePackageReference(Manifest('my_package'), 'https://localhost/my_package.core')
        local_reference_maker = Mock()
        catalog_service = Mock()
        catalog_service.get_package_reference = Mock(return_value=ref)
        name_resolver = PackageNameResolver(local_reference_maker, catalog_service, set())
        resolved_ref = name_resolver.resolve('my_package')
        self.assertEqual(ref, resolved_ref)

    def test_name_resolver_resolves_installed_name(self):
        ref = InstalledPackageReference(Manifest('my_package'))
        local_reference_maker = Mock()
        catalog_service = Mock()
        name_resolver = PackageNameResolver(local_reference_maker, catalog_service, {ref})
        resolved_ref = name_resolver.resolve('my_package')
        self.assertEqual(ref, resolved_ref)

    def test_name_resolver_does_not_resolve(self):
        local_reference_maker = Mock()
        catalog_service = Mock()
        catalog_service.get_package_reference = Mock(return_value=None)
        name_resolver = PackageNameResolver(local_reference_maker, catalog_service, set())
        with self.assertRaises(PackageNotFoundException):
            name_resolver.resolve('my_package')

