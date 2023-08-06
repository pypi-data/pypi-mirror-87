from dataclasses import dataclass
from logging import getLogger

from injector import inject

from core_get.configuration.installed_packages import InstalledPackages
from core_get.configuration.project_directory_finder import ProjectDirectoryManager
from core_get.file.file_system import FileSystem
from core_get.package.manifest import Manifest
from core_get.package.reference.package_reference import InstalledPackageReference
from core_get.vendor.project import Project
from core_get.vendor.project_source_file import ProjectSourceFile

logger = getLogger(__name__)


@inject
@dataclass
class PackageRemover:
    project_directory_manager: ProjectDirectoryManager
    file_system: FileSystem

    def remove_package(self, project: Project, installed_packages: InstalledPackages, manifest: Manifest,
                       reference: InstalledPackageReference) -> None:
        project_path = self.project_directory_manager.get_project_directory()
        installed_package = next((installed_package for installed_package in installed_packages.installed_packages
                                  if installed_package.manifest.name == reference.manifest.name))

        # Remove the physical files
        for installed_file in installed_package.installed_files:
            self.file_system.delete_file(project_path / installed_file.path)
        self.file_system.remove_directory(project_path / installed_package.path)

        # Remove the package from the metadata
        installed_packages.installed_packages.remove(installed_package)
        project.remove_source_files([ProjectSourceFile(installed_file.path, installed_package.manifest.library)
                                     for installed_file in installed_package.installed_files])
        manifest.dependencies.remove(installed_package.manifest.name)
