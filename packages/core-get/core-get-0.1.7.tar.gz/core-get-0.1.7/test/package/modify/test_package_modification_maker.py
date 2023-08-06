from typing import Any, Dict
from unittest import TestCase
from unittest.mock import Mock

from core_get.package.manifest import Manifest
from core_get.package.modify.package_dependency_resolver import PackageDependencyResolver
from core_get.package.modify.package_modification_maker import PackageModificationMaker
from core_get.package.reference.package_reference import InstalledPackageReference, PackageReference, \
    RemotePackageReference


class TestPackageModificationMaker(TestCase):
    def test_no_op_does_nothing(self):
        package_dependency_resolver = PackageDependencyResolver()
        package_modification_maker = PackageModificationMaker(self._make_resolver_factory({}),
                                                              package_dependency_resolver)
        orders = package_modification_maker.make_modifications(set(), set(), set(), set())
        self.assertEqual(set(), orders.remove)
        self.assertEqual(set(), orders.install)

    def test_remove_package_removes_transitive_dependency(self):
        package_ref_1 = InstalledPackageReference(Manifest('my_package_1', dependencies=['my_package_2']))
        package_ref_2 = InstalledPackageReference(Manifest('my_package_2'))
        resolve = {'my_package_2': package_ref_2}
        package_dependency_resolver = PackageDependencyResolver()
        package_modification_maker = PackageModificationMaker(self._make_resolver_factory(resolve),
                                                              package_dependency_resolver)
        orders = package_modification_maker.make_modifications(set(), {'my_package_1'}, {'my_package_1'},
                                                               {package_ref_1, package_ref_2})
        self.assertEqual({package_ref_1, package_ref_2}, orders.remove)
        self.assertEqual(set(), orders.install)

    def test_add_package_installs_new_reference(self):
        package_ref_1 = RemotePackageReference(Manifest('my_package_1'), 'https://localhost/my_package_1.core')
        resolve = {'my_package_1': package_ref_1}
        package_dependency_resolver = PackageDependencyResolver()
        package_modification_maker = PackageModificationMaker(self._make_resolver_factory(resolve),
                                                              package_dependency_resolver)
        orders = package_modification_maker.make_modifications({'my_package_1'}, set(), set(), set())
        self.assertEqual(set(), orders.remove)
        self.assertEqual({package_ref_1}, orders.install)

    def _make_resolver_factory(self, resolve: Dict[str, PackageReference]) -> Any:
        package_name_resolver = Mock()
        package_name_resolver.resolve = Mock(side_effect=lambda name: resolve[name])
        package_name_resolver_factory = Mock()
        package_name_resolver_factory.make = Mock(return_value=package_name_resolver)
        return package_name_resolver_factory
