from dataclasses import dataclass
from typing import NamedTuple, Set

from injector import inject

from core_get.package.modify.package_dependency_resolver import PackageDependencyResolver
from core_get.package.modify.package_name_resolver import PackageNameResolverFactory
from core_get.package.reference.package_reference import PackageReference, InstalledPackageReference


class PackageModifications(NamedTuple):
    install: Set[PackageReference]
    remove: Set[InstalledPackageReference]
    direct: Set[str]


@inject
@dataclass
class PackageModificationMaker:
    package_name_resolver_factory: PackageNameResolverFactory
    package_dependencies_resolver: PackageDependencyResolver

    def make_modifications(self, add_names: Set[str], remove_names: Set[str], dependencies: Set[str],
                           installed_refs: Set[InstalledPackageReference]) -> PackageModifications:
        package_name_resolver = self.package_name_resolver_factory.make(installed_refs)
        dependency_refs = {installed_ref for installed_ref in installed_refs
                           if installed_ref.manifest.name in dependencies}
        add_refs = {package_name_resolver.resolve(name) for name in add_names}
        remove_refs = {ref for ref in installed_refs if ref.manifest.name in remove_names}
        new_direct_refs = dependency_refs - remove_refs | add_refs
        new_refs = self.package_dependencies_resolver.resolve_dependencies(new_direct_refs, package_name_resolver)
        install_refs = new_refs - installed_refs
        remove_refs = installed_refs - new_refs
        return PackageModifications(install_refs, remove_refs, {add_ref.manifest.name for add_ref in add_refs})
