from dataclasses import dataclass

from injector import inject

from core_get.configuration.installed_packages import InstalledPackages, InstalledPackage
from core_get.file.flat.flat_directory import FlatDirectory
from core_get.package.manifest import Manifest
from core_get.package.modify.install.file_copier import FileCopier
from core_get.package.modify.install.install_order import InstallOrder
from core_get.vendor.project import Project
from core_get.vendor.project_source_file import ProjectSourceFile


@inject
@dataclass
class PackageInstaller:
    package_file_copier: FileCopier

    def install_package(self, project: Project, installed_packages: InstalledPackages, manifest: Manifest,
                        package_install_order: InstallOrder, directory: FlatDirectory) -> None:
        installed_files = self.package_file_copier.copy_package_files(package_install_order, directory)
        installed_package = InstalledPackage(package_install_order.reference.manifest, package_install_order.variant,
                                             package_install_order.install_path, package_install_order.is_direct,
                                             installed_files)
        installed_packages.installed_packages.append(installed_package)

        project.add_source_files(
            [ProjectSourceFile(installed_file.path, package_install_order.reference.manifest.library)
             for installed_file in installed_files])

        if package_install_order.is_direct:
            manifest.dependencies.append(package_install_order.reference.manifest.name)
