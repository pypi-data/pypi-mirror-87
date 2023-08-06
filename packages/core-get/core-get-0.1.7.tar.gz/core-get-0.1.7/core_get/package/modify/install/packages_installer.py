from dataclasses import dataclass
from typing import List

from injector import inject

from core_get.configuration.installed_packages import InstalledPackages
from core_get.package.manifest import Manifest
from core_get.package.modify.install.install_order import InstallOrder
from core_get.package.modify.install.package_installer import PackageInstaller
from core_get.package.modify.package_reference_path_resolver import PackageReferencePathResolver
from core_get.file.flat.flat_directory_maker import FlatDirectoryMaker
from core_get.vendor.project import Project


@inject
@dataclass
class PackagesInstaller:
    package_reference_path_resolver: PackageReferencePathResolver
    package_flat_directory_maker: FlatDirectoryMaker
    package_installer: PackageInstaller

    def install_packages(self, package_install_orders: List[InstallOrder], project: Project,
                         installed_packages: InstalledPackages, manifest: Manifest):
        install_references = [package_install_order.reference for package_install_order in package_install_orders]

        package_paths = self.package_reference_path_resolver.resolve_paths(install_references)

        # TODO: Verify the integrity of all packages, and any signatures
        package_flat_directories = {name: self.package_flat_directory_maker.make_flat_directory(path)
                                    for name, path in package_paths.items()}

        for package_install_order in package_install_orders:
            package_flat_directory = package_flat_directories[package_install_order.reference.manifest.name]
            self.package_installer.install_package(project, installed_packages, manifest, package_install_order,
                                                   package_flat_directory)
