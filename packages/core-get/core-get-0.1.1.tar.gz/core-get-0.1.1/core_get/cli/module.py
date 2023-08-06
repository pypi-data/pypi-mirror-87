import sys
from dataclasses import dataclass
from typing import List

from injector import Module, Binder

from core_get.package.modify.install.install_order import InstallOrder
from core_get.package.modify.package_modifier import PackageModificationInterface, PackageNotFoundInterface
from core_get.catalog.download_status_interface import DownloadStatusInterface
from core_get.package.reference.package_reference import InstalledPackageReference


class CliPackageNotFoundInterface(PackageNotFoundInterface):
    def package_not_found(self, name: str) -> None:
        sys.stderr.write(f"Package {name} was not found")


class CliPackageModificationInterface(PackageModificationInterface):
    def verify_install(self, install_orders: List[InstallOrder], removed_refs: List[InstalledPackageReference]) -> bool:
        if not install_orders and not removed_refs:
            return True
        if install_orders:
            install_package_names = [install_order.reference.manifest.name for install_order in install_orders]
            sys.stdout.write(f"The following packages will be installed: {', '.join(install_package_names)}\n")
        if removed_refs:
            remove_package_names = [removed_ref.manifest.name for removed_ref in removed_refs]
            sys.stdout.write(f"The following packages will be removed: {', '.join(remove_package_names)}\n")
        while True:
            choice = input(f"Proceed? [Y/n] ").lower()
            if choice == '' or choice == 'y':
                return True
            if choice == 'n':
                return False
            sys.stdout.write("Please respond with 'y' or 'n'\n")


@dataclass
class CliDownloadStatusInterface(DownloadStatusInterface):
    filename: str = ''

    def download_begin(self, filename: str) -> None:
        self.filename = filename
        sys.stdout.write(f"Download {self.filename}...")

    def download_progress(self, downloaded: int, size: int) -> None:
        sys.stdout.write(f"\rDownload {self.filename}: {100 * downloaded // size}%")

    def download_done(self) -> None:
        sys.stdout.write(f"\rDownload {self.filename}: 100%\n")


class CliModule(Module):

    def configure(self, binder: Binder) -> None:
        binder.bind(PackageModificationInterface, CliPackageModificationInterface)
        binder.bind(PackageNotFoundInterface, CliPackageNotFoundInterface)
        binder.bind(DownloadStatusInterface, CliDownloadStatusInterface)

