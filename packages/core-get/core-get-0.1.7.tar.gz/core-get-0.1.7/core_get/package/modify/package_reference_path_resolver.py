from dataclasses import dataclass
from pathlib import PurePath
from typing import List, Dict

from injector import inject

from core_get.package.modify.install.download_cache import DownloadCache
from core_get.package.reference.package_reference import PackageReference, LocalPackageReference, RemotePackageReference


@inject
@dataclass
class PackageReferencePathResolver:
    package_cache: DownloadCache

    def resolve_paths(self, references: List[PackageReference]) -> Dict[str, PurePath]:
        # Use LocalReferences directly
        package_paths = {reference.manifest.name: reference.path
                         for reference in references if isinstance(reference, LocalPackageReference)}

        # Download all RemoteReferences to the repository cache
        package_paths.update({reference.manifest.name: self.package_cache.download_package(reference)
                              for reference in references if isinstance(reference, RemotePackageReference)})

        return package_paths
