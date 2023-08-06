from dataclasses import dataclass
from typing import Set

from injector import inject

from core_get.package.modify.package_name_resolver import PackageNameResolver
from core_get.package.reference.package_reference import PackageReference


@inject
@dataclass
class PackageDependencyResolver:

    def resolve_dependencies(self, references: Set[PackageReference],
                             name_resolver: PackageNameResolver) -> Set[PackageReference]:
        refs = {ref.manifest.name: ref for ref in references}
        while True:
            unresolved_names = set().union(*(ref.manifest.dependencies for ref in refs.values())).difference(
                refs.keys())
            if not unresolved_names:
                break
            new_references = [name_resolver.resolve(unresolved_name) for unresolved_name in unresolved_names]
            refs.update(**{ref.manifest.name: ref for ref in new_references})

        return set(refs.values())
