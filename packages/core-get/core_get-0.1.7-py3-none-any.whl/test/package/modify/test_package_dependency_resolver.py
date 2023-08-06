from unittest import TestCase
from unittest.mock import Mock

from core_get.package.manifest import Manifest
from core_get.package.modify.package_dependency_resolver import PackageDependencyResolver
from core_get.package.reference.package_reference import PackageReference


class TestPackageDependenciesResolver(TestCase):
    def test_resolve_no_dependencies(self):
        package_name_resolver = Mock()
        package_dependencies_resolver = PackageDependencyResolver()
        package_refs = package_dependencies_resolver.resolve_dependencies(set(), package_name_resolver)
        self.assertEqual(set(), package_refs)

    def test_resolve_transitive_dependencies(self):
        package_ref_1 = PackageReference(Manifest('my_package_1', dependencies=['my_package_2']))
        package_ref_2 = PackageReference(Manifest('my_package_2', dependencies=['my_package_3']))
        package_ref_3 = PackageReference(Manifest('my_package_3'))
        resolve = {'my_package_2': package_ref_2, 'my_package_3': package_ref_3}
        package_name_resolver = Mock()
        package_name_resolver.resolve = Mock(side_effect=lambda name: resolve[name])
        package_dependencies_resolver = PackageDependencyResolver()
        package_refs = package_dependencies_resolver.resolve_dependencies({package_ref_1}, package_name_resolver)
        self.assertEqual({package_ref_1, package_ref_2, package_ref_3}, set(package_refs))
