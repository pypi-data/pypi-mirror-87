from dataclasses import dataclass
from typing import List

from injector import inject

from core_get.configuration.installed_packages import InstalledPackages
from core_get.package.manifest import Manifest
from core_get.package.modify.remove.package_aggregate_modification_checker import PackageAggregateModificationChecker
from core_get.package.modify.remove.package_remover import PackageRemover
from core_get.package.reference.package_reference import InstalledPackageReference
from core_get.vendor.project import Project


@inject
@dataclass
class PackageAggregateRemover:
    package_aggregate_modification_checker: PackageAggregateModificationChecker
    package_remover: PackageRemover

    def remove_packages(self, project: Project, installed_packages: InstalledPackages, manifest: Manifest,
                        references: List[InstalledPackageReference], force: bool) -> None:
        remove = [reference.manifest.name for reference in references]
        installed_packages_to_remove = \
            [installed_package for installed_package in installed_packages.installed_packages
             if installed_package.manifest.name in remove]
        self.package_aggregate_modification_checker.check_modifications(installed_packages_to_remove, force)

        for reference in references:
            self.package_remover.remove_package(project, installed_packages, manifest, reference)
