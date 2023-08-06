from pathlib import PurePath
from unittest import TestCase
from unittest.mock import Mock

from core_get.configuration.installed_packages import InstalledFile, InstalledPackages, InstalledPackage
from core_get.package.manifest import Manifest
from core_get.package.modify.install.install_order import InstallOrder
from core_get.package.modify.install.package_installer import PackageInstaller
from core_get.package.reference.package_reference import PackageReference
from core_get.vendor.project_source_file import ProjectSourceFile


class TestPackageInstaller(TestCase):
    def test_install_package(self):
        package_file_copier = Mock()
        installed_files = [InstalledFile(PurePath('./extern/my_package-0.0.0/my_hdl_file.vhdl'),
                                         bytes.fromhex(
                                             '00112233445566778899AABBCCDDEEFF00112233445566778899AABBCCDDEEFF'))]
        package_file_copier.copy_package_files = Mock(return_value=installed_files)
        package_installer = PackageInstaller(package_file_copier)
        project = Mock()
        project.add_source_files = Mock()
        installed_packages = InstalledPackages('MYDEVICE', [])
        manifest = Manifest('my_main_project')
        install_manifest = Manifest('my_package', library='mylib')
        reference = PackageReference(install_manifest)
        package_install_order = InstallOrder(reference, 'my_variant', PurePath('./extern/my_package-0.0.0'), True)
        directory = Mock()
        package_installer.install_package(project, installed_packages, manifest, package_install_order, directory)
        project.add_source_files.assert_called_once_with(
            [ProjectSourceFile(PurePath('./extern/my_package-0.0.0/my_hdl_file.vhdl'), 'mylib')])
        self.assertEqual(['my_package'], manifest.dependencies)
        self.assertEqual(InstalledPackages('MYDEVICE', [
            InstalledPackage(install_manifest, 'my_variant', PurePath('./extern/my_package-0.0.0'), True,
                             installed_files)]), installed_packages)
