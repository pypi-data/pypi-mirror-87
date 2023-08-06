from pathlib import PurePath
from unittest import TestCase
from unittest.mock import Mock

from core_get.configuration.installed_packages import InstalledPackages, InstalledPackage, InstalledFile
from core_get.package.manifest import Manifest
from core_get.package.modify.remove.package_remover import PackageRemover
from core_get.package.reference.package_reference import InstalledPackageReference


class TestPackageRemover(TestCase):
    def test_remove_package(self):
        project_directory_manager = Mock()
        project_directory_manager.get_project_directory = Mock(return_value=PurePath('.'))
        file_system = Mock()
        package_remover = PackageRemover(project_directory_manager, file_system)
        project = Mock()
        remove_manifest = Manifest('my_package')
        installed_files = [InstalledFile(PurePath('extern/my_package-0.0.0/a.vhdl'),
                                         bytes.fromhex(
                                             '97db9eb56b5bb7186291423c00accc458ab65225c79c7f439b6d408a4fa7bcaa'))]
        installed_package = InstalledPackage(remove_manifest, 'my_variant', PurePath('extern/my_package-0.0.0'), True,
                                             installed_files)
        installed_packages = InstalledPackages('MYDEV', [installed_package])
        manifest = Manifest('my_project', dependencies=['my_package'])
        reference = InstalledPackageReference(remove_manifest)
        package_remover.remove_package(project, installed_packages, manifest, reference)
        file_system.delete_file.assert_called_once_with(PurePath('./extern/my_package-0.0.0/a.vhdl'))
        file_system.remove_directory.assert_called_once_with(PurePath('./extern/my_package-0.0.0'))

