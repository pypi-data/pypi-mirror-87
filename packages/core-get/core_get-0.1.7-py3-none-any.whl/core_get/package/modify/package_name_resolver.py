from dataclasses import dataclass
from typing import Set

from injector import inject

from core_get.catalog.catalog_service import CatalogService
from core_get.package.reference.package_reference import InstalledPackageReference, PackageReference
from core_get.package.reference.local_reference_maker import LocalReferenceMaker


@dataclass
class PackageNotFoundException(Exception):
    name: str


@dataclass
class PackageNameResolver:
    local_reference_maker: LocalReferenceMaker
    catalog_service: CatalogService
    installed_references: Set[InstalledPackageReference]

    def resolve(self, name: str) -> PackageReference:
        if name.endswith('.core'):
            return self.local_reference_maker.make(name)

        installed_reference = next((installed_reference for installed_reference in self.installed_references
                                    if installed_reference.manifest.name == name), None)
        if installed_reference is not None:
            return installed_reference

        remote_reference = self.catalog_service.get_package_reference(name)
        if remote_reference is not None:
            return remote_reference

        raise PackageNotFoundException(name)


@inject
@dataclass
class PackageNameResolverFactory:
    local_reference_maker: LocalReferenceMaker
    catalog_service: CatalogService

    def make(self, installed_references: Set[InstalledPackageReference]):
        return PackageNameResolver(self.local_reference_maker, self.catalog_service, installed_references)
