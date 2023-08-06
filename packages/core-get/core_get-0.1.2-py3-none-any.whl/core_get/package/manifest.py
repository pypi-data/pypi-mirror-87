from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import PurePath
from typing import List, Dict, Optional

from semver import VersionInfo

from core_get.configuration.configuration import Configuration


@dataclass
class VariantManifest:
    target_device: str
    include: List[str]

    @classmethod
    def from_dict(cls, d) -> VariantManifest:
        return VariantManifest(d['target_device'], list(d['include']))

    def to_dict(self) -> dict:
        return {'target_device': self.target_device, 'include': self.include}


@dataclass
class Manifest(Configuration):
    name: str
    version: VersionInfo = VersionInfo(0)
    library: str = 'work'
    device: Optional[str] = None
    dependencies: List[str] = field(default_factory=list)
    lib_path: Optional[PurePath] = None
    variant_manifests: Dict[str, VariantManifest] = field(default_factory=dict)

    def qualified_name(self):
        return f"{self.name}-{self.version}"

    @classmethod
    def from_dict(cls, d) -> Manifest:
        return Manifest(d['name'], VersionInfo.parse(d['version']), d['library'], d['device'],
                        list(d['dependencies']), PurePath(d['lib_path']) if d['lib_path'] is not None else None,
                        {name: VariantManifest.from_dict(e)
                         for name, e
                         in d['version_manifests'].items()})

    def to_dict(self) -> dict:
        return {'name': self.name, 'version': str(self.version), 'library': self.library, 'device': self.device,
                'dependencies': self.dependencies,
                'lib_path': self.lib_path.as_posix() if self.lib_path is not None else None,
                'version_manifests': {name: version_manifest.to_dict()
                                      for name, version_manifest
                                      in self.variant_manifests.items()}}
