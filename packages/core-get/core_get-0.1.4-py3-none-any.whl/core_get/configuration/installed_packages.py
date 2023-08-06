from __future__ import annotations

from dataclasses import dataclass
from pathlib import PurePath, PurePosixPath
from typing import List

from core_get.configuration.configuration import Configuration
from core_get.package.manifest import Manifest


@dataclass
class InstalledFile(Configuration):
    path: PurePath
    hash: bytes

    @classmethod
    def from_dict(cls, d) -> InstalledFile:
        return InstalledFile(PurePosixPath(d['path']), bytes.fromhex(d['hash']))

    def to_dict(self) -> dict:
        return {'path': self.path.as_posix(), 'hash': self.hash.hex()}


@dataclass
class InstalledPackage(Configuration):
    manifest: Manifest
    variant_name: str
    path: PurePath
    specific: bool
    installed_files: List[InstalledFile]

    @classmethod
    def from_dict(cls, d) -> InstalledPackage:
        return InstalledPackage(Manifest.from_dict(d['manifest']), d['variant_name'],
                                PurePosixPath(d['path']), d['specific'],
                                [InstalledFile.from_dict(installed_file) for installed_file in d['installed_files']])

    def to_dict(self) -> dict:
        return {'manifest': self.manifest.to_dict(), 'variant_name': self.variant_name,
                'path': self.path.as_posix(), 'specific': self.specific,
                'installed_files': [installed_file.to_dict() for installed_file in self.installed_files]}


@dataclass
class InstalledPackages(Configuration):
    device: str
    installed_packages: List[InstalledPackage]

    @classmethod
    def from_dict(cls, d) -> InstalledPackages:
        return InstalledPackages(d['device'],
                                 [InstalledPackage.from_dict(e) for e in d['installed_packages']])

    def to_dict(self) -> dict:
        return {'device': self.device,
                'installed_packages': [installed_package.to_dict() for installed_package in self.installed_packages]}
