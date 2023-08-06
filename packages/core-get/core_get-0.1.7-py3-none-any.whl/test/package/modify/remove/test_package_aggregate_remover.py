from pathlib import PurePath
from unittest import TestCase
from unittest.mock import Mock

from core_get.configuration.installed_packages import InstalledPackages, InstalledPackage, InstalledFile
from core_get.package.manifest import Manifest
from core_get.package.modify.remove.package_aggregate_remover import PackageAggregateRemover
from core_get.package.reference.package_reference import PackageReference, InstalledPackageReference


class TestPackageAggregateRemover(TestCase):
    def test_remove_packages(self):
        package_aggregate_modification_checker = Mock()
        package_aggregate_modification_checker.check_modifications = Mock()
        package_remover = Mock()
        package_remover.remove_package = Mock()
        package_aggregate_remover = PackageAggregateRemover(package_aggregate_modification_checker, package_remover)
        project = Mock()
        manifest = Manifest('my_project')
        installed_manifest = Manifest('my_package')
        installed_files = [InstalledFile(PurePath('./extern/my_package-0.0.0/a.vhdl'),
                                         b'00112233445566778899AABBCCDDEEFF00112233445566778899AABBCCDDEEFF')]
        installed_packages = InstalledPackages('MYDEV', [InstalledPackage(installed_manifest, 'my_variant',
                                                                          PurePath('./extern/my_package-0.0.0'), True,
                                                                          installed_files)])
        reference = InstalledPackageReference(installed_manifest)
        package_aggregate_remover.remove_packages(project, installed_packages, manifest, [reference], False)
        package_remover.remove_package.assert_called_once_with(project, installed_packages, manifest, reference)
