from dataclasses import dataclass
from typing import List

from injector import inject

from core_get.configuration.installed_packages import InstalledPackage
from core_get.package.modify.remove.package_modification_checker import PackageModificationChecker, logger, \
    PackageModifications


@dataclass
class ModifiedPackageException(Exception):
    package_modifications: List[PackageModifications]


@inject
@dataclass
class PackageAggregateModificationChecker:
    package_modification_detector: PackageModificationChecker

    def check_modifications(self, installed_packages_to_remove: List[InstalledPackage], override: bool) -> None:
        package_modifications = \
            [package_modification for package_modification in
             (self.package_modification_detector.check_modifications(installed_package)
              for installed_package in installed_packages_to_remove) if package_modification is not None]

        if any(package_modifications):
            if override:
                logger.warning(f'Packages modified; forcing removal')
            else:
                raise ModifiedPackageException(package_modifications)
