from pathlib import PurePath
from unittest import TestCase
from unittest.mock import Mock

from core_get.configuration.installed_packages import InstalledPackage, InstalledFile
from core_get.package.manifest import Manifest
from core_get.package.modify.remove.package_modification_checker import PackageModificationChecker, PackageModifications


class TestPackageModificationChecker(TestCase):
    def test_check_modifications_no_modifications(self):
        project_directory_manager = Mock()
        project_directory_manager.get_project_directory = Mock(return_value='.')
        file_system = Mock()
        file_system.read_file = Mock(return_value=b'hej')
        file_system.glob = Mock(return_value=[PurePath('extern/my_package-0.0.0/a.vhdl')])
        package_modification_checker = PackageModificationChecker(project_directory_manager, file_system)
        manifest = Manifest('my_package')
        installed_files = [InstalledFile(PurePath('extern/my_package-0.0.0/a.vhdl'),
                                         bytes.fromhex(
                                             '97db9eb56b5bb7186291423c00accc458ab65225c79c7f439b6d408a4fa7bcaa'))]
        installed_package = InstalledPackage(manifest, 'my_variant', PurePath('extern/my_package-0.0.0'), True,
                                             installed_files)
        package_modifications = package_modification_checker.check_modifications(installed_package)
        self.assertIsNone(package_modifications)

    def test_check_modifications_modified_file(self):
        project_directory_manager = Mock()
        project_directory_manager.get_project_directory = Mock(return_value='.')
        file_system = Mock()
        file_system.read_file = Mock(return_value=b'hopp')
        file_system.glob = Mock(return_value=[PurePath('extern/my_package-0.0.0/a.vhdl')])
        package_modification_checker = PackageModificationChecker(project_directory_manager, file_system)
        manifest = Manifest('my_package')
        installed_files = [InstalledFile(PurePath('extern/my_package-0.0.0/a.vhdl'),
                                         bytes.fromhex(
                                             '97db9eb56b5bb7186291423c00accc458ab65225c79c7f439b6d408a4fa7bcaa'))]
        installed_package = InstalledPackage(manifest, 'my_variant', PurePath('extern/my_package-0.0.0'), True,
                                             installed_files)
        package_modifications = package_modification_checker.check_modifications(installed_package)
        self.assertEqual(PackageModifications([], [PurePath('a.vhdl')], []),
                         package_modifications)

    def test_check_modifications_extra_file(self):
        project_directory_manager = Mock()
        project_directory_manager.get_project_directory = Mock(return_value='.')
        file_system = Mock()
        file_system.read_file = Mock(return_value=b'hej')
        file_system.glob = Mock(return_value=[PurePath('extern/my_package-0.0.0/a.vhdl'), PurePath('extern/my_package-0.0.0/b.vhdl')])
        package_modification_checker = PackageModificationChecker(project_directory_manager, file_system)
        manifest = Manifest('my_package')
        installed_files = [InstalledFile(PurePath('extern/my_package-0.0.0/a.vhdl'),
                                         bytes.fromhex(
                                             '97db9eb56b5bb7186291423c00accc458ab65225c79c7f439b6d408a4fa7bcaa'))]
        installed_package = InstalledPackage(manifest, 'my_variant', PurePath('extern/my_package-0.0.0'), True,
                                             installed_files)
        package_modifications = package_modification_checker.check_modifications(installed_package)
        self.assertEqual(PackageModifications([], [], [PurePath('b.vhdl')]),
                         package_modifications)

    def test_check_modifications_missing_file(self):
        project_directory_manager = Mock()
        project_directory_manager.get_project_directory = Mock(return_value='.')
        file_system = Mock()
        file_system.read_file = Mock(side_effect=FileNotFoundError)
        file_system.glob = Mock(return_value=[])
        package_modification_checker = PackageModificationChecker(project_directory_manager, file_system)
        manifest = Manifest('my_package')
        installed_files = [InstalledFile(PurePath('extern/my_package-0.0.0/a.vhdl'),
                                         bytes.fromhex(
                                             '97db9eb56b5bb7186291423c00accc458ab65225c79c7f439b6d408a4fa7bcaa'))]
        installed_package = InstalledPackage(manifest, 'my_variant', PurePath('extern/my_package-0.0.0'), True,
                                             installed_files)
        package_modifications = package_modification_checker.check_modifications(installed_package)
        self.assertEqual(PackageModifications([PurePath('a.vhdl')], [], []),
                         package_modifications)
