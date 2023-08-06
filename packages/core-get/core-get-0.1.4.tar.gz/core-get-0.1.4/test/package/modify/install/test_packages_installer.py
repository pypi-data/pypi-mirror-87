from pathlib import PurePath
from unittest import TestCase
from unittest.mock import Mock

from core_get.configuration.installed_packages import InstalledPackages
from core_get.package.manifest import Manifest
from core_get.package.modify.install.install_order import InstallOrder
from core_get.package.modify.install.packages_installer import PackagesInstaller
from core_get.package.reference.package_reference import PackageReference


class TestPackagesInstaller(TestCase):
    def test_install_packages(self):
        package_reference_path_resolver = Mock()
        package_reference_path_resolver.resolve_paths = Mock(return_value={'mypkg': PurePath('./mypkg.core')})
        package_flat_directory_maker = Mock()
        flat_directory = Mock()
        package_flat_directory_maker.make_flat_directory = Mock(return_value=flat_directory)
        package_installer = Mock()
        packages_installer = PackagesInstaller(package_reference_path_resolver, package_flat_directory_maker,
                                               package_installer)
        project = Mock()
        manifest = Manifest('my_project', lib_path=PurePath('./external'))
        install_manifest = Manifest('mypkg')
        reference = PackageReference(install_manifest)
        installed_packages = InstalledPackages('MYDEVICE', [])
        install_order = InstallOrder(reference, 'my_variant', PurePath('./external/mypkg-0.0.0'), True)
        packages_installer.install_packages([install_order], project, installed_packages, manifest)
        package_installer.install_package.assert_called_once_with(project, installed_packages, manifest, install_order,
                                                                  flat_directory)
