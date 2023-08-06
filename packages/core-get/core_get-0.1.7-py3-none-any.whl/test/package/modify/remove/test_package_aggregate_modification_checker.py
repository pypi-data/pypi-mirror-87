from pathlib import PurePath
from unittest import TestCase
from unittest.mock import Mock

from core_get.configuration.installed_packages import InstalledPackage, InstalledFile
from core_get.package.manifest import Manifest
from core_get.package.modify.remove.package_aggregate_modification_checker import PackageAggregateModificationChecker, \
    ModifiedPackageException
from core_get.package.modify.remove.package_modification_checker import PackageModificationChecker


class TestPackageAggregateModificationChecker(TestCase):
    def test_check_modifications_detects_modification(self):
        package_modification_detector = Mock()
        package_modification_detector.check_modifications = Mock(return_value=True)
        package_aggregate_modification_checker = PackageAggregateModificationChecker(package_modification_detector)
        installed_files = [InstalledFile(PurePath('./extern/my_package-0.0.0/a.vhdl'),
                                         b'00112233445566778899AABBCCDDEEFF00112233445566778899AABBCCDDEEFF')]
        manifest = Manifest('my_package')
        installed_packages = [InstalledPackage(manifest, 'my_variant', PurePath('./extern/my_package-0.0.0'), True, installed_files)]
        with self.assertRaises(ModifiedPackageException):
            package_aggregate_modification_checker.check_modifications(installed_packages, False)

    def test_check_modifications_overridden(self):
        package_modification_detector = Mock()
        package_modification_detector.check_modifications = Mock(return_value=True)
        package_aggregate_modification_checker = PackageAggregateModificationChecker(package_modification_detector)
        installed_files = [InstalledFile(PurePath('./extern/my_package-0.0.0/a.vhdl'),
                                         b'00112233445566778899AABBCCDDEEFF00112233445566778899AABBCCDDEEFF')]
        manifest = Manifest('my_package')
        installed_packages = [InstalledPackage(manifest, 'my_variant', PurePath('./extern/my_package-0.0.0'), True, installed_files)]
        package_aggregate_modification_checker.check_modifications(installed_packages, True)

    def test_check_modifications_detects_nothing(self):
        package_modification_detector = Mock()
        package_modification_detector.check_modifications = Mock(return_value=False)
        package_aggregate_modification_checker = PackageAggregateModificationChecker(package_modification_detector)
        installed_files = [InstalledFile(PurePath('./extern/my_package-0.0.0/a.vhdl'),
                                         b'00112233445566778899AABBCCDDEEFF00112233445566778899AABBCCDDEEFF')]
        manifest = Manifest('my_package')
        installed_packages = [InstalledPackage(manifest, 'my_variant', PurePath('./extern/my_package-0.0.0'), True, installed_files)]
        package_aggregate_modification_checker.check_modifications(installed_packages, False)
