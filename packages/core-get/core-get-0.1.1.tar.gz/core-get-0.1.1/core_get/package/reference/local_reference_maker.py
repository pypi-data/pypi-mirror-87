import zipfile
from dataclasses import dataclass
from pathlib import PurePath
from typing import Optional

from injector import inject

from core_get.configuration.serialization.toml_serializer import TomlSerializer
from core_get.package.manifest import Manifest
from core_get.package.reference.package_reference import LocalPackageReference


@inject
@dataclass
class LocalReferenceMaker:
    toml_serializer: TomlSerializer

    def make(self, name: str) -> Optional[LocalPackageReference]:
        path = PurePath(name)
        zip_file = zipfile.ZipFile(path)
        with zip_file.open('Core.toml') as file:
            manifest_data = file.read()
            manifest = self.toml_serializer.from_bytes(manifest_data, Manifest)

        return LocalPackageReference(manifest, path)
