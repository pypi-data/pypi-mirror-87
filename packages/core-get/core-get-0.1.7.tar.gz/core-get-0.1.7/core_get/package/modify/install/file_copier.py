from dataclasses import dataclass
from typing import List

from injector import inject

from core_get.configuration.installed_packages import InstalledFile
from core_get.file.file_system import FileSystem
from core_get.file.flat.flat_directory import FlatDirectory
from core_get.package.modify.install.install_order import InstallOrder


@inject
@dataclass
class FileCopier:
    file_system: FileSystem

    def copy_package_files(self, package_install_order: InstallOrder, directory: FlatDirectory) \
            -> List[InstalledFile]:
        # Filter out the files for the selected variant
        variant_manifest = package_install_order.reference.manifest.variant_manifests[package_install_order.variant]
        filtered_directory = directory.filter(variant_manifest.include)

        # Write the files
        installed_files = []
        for file in filtered_directory.get_files():
            destination_path = package_install_order.install_path / file.path
            with file.open('r') as source_stream:
                h = self.file_system.write_stream(destination_path, source_stream)
                installed_files.append(InstalledFile(destination_path, h))

        return installed_files
