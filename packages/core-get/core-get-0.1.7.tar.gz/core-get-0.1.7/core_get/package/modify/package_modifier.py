from dataclasses import dataclass
from logging import getLogger
from typing import List

from injector import inject

from core_get.configuration.installed_packages_accessor import InstalledPackagesAccessor
from core_get.package.modify.install.install_order import InstallOrder
from core_get.package.modify.install.install_order_maker import InstallOrderMaker
from core_get.package.modify.install.packages_installer import PackagesInstaller
from core_get.package.modify.package_modification_maker import PackageModificationMaker
from core_get.package.modify.package_name_resolver import PackageNotFoundException
from core_get.package.modify.remove.package_aggregate_remover import PackageAggregateRemover
from core_get.package.package_manifest_accessor import PackageManifestAccessor
from core_get.package.reference.package_reference import InstalledPackageReference
from core_get.vendor.project_finder import ProjectFinder

logger = getLogger(__name__)


class PackageModificationInterface:
    def verify_install(self, install_orders: List[InstallOrder], removed_refs: List[InstalledPackageReference]) -> bool:
        raise NotImplementedError


class PackageNotFoundInterface:
    def package_not_found(self, name: str) -> None:
        raise NotImplementedError


@inject
@dataclass
class PackageModifier:
    package_manifest_accessor: PackageManifestAccessor
    installed_packages_accessor: InstalledPackagesAccessor
    project_finder: ProjectFinder
    package_modification_maker: PackageModificationMaker
    package_not_found_interface: PackageNotFoundInterface
    package_install_order_maker: InstallOrderMaker
    package_modification_interface: PackageModificationInterface
    packages_remover: PackageAggregateRemover
    packages_installer: PackagesInstaller

    def modify_packages(self, add_names: List[str], remove_names: List[str], force: bool):
        # Read in the manifest, installed packages metadata and the vendor project
        manifest = self.package_manifest_accessor.read()
        installed_packages = self.installed_packages_accessor.read()
        project = self.project_finder.find_project()

        installed_references = {InstalledPackageReference(installed_package.manifest)
                                for installed_package in installed_packages.installed_packages}
        try:
            package_modifications = \
                self.package_modification_maker.make_modifications(set(add_names), set(remove_names),
                                                                   set(manifest.dependencies), installed_references)
        except PackageNotFoundException as e:
            self.package_not_found_interface.package_not_found(e.name)
            return

        device = project.get_device()
        package_install_orders = \
            [self.package_install_order_maker.make(device, reference, manifest.lib_path,
                                                   reference.manifest.name in package_modifications.direct)
             for reference in package_modifications.install]

        # UI: Verify packages to download and install
        if not self.package_modification_interface.verify_install(package_install_orders,
                                                                  list(package_modifications.remove)):
            return

        # Remove packages
        self.packages_remover.remove_packages(project, installed_packages, manifest,
                                              list(package_modifications.remove), force)

        # Download and install all packages
        self.packages_installer.install_packages(package_install_orders, project, installed_packages, manifest)

        # Write back all changes
        self.package_manifest_accessor.write(manifest)
        self.installed_packages_accessor.write(installed_packages)
        project.write()
