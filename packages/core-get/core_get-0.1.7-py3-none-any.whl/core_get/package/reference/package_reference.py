from __future__ import annotations

from dataclasses import dataclass
from functools import total_ordering
from pathlib import PurePath

from core_get.package.manifest import Manifest


@dataclass
@total_ordering
class PackageReference:
    manifest: Manifest

    def __hash__(self):
        return hash(self._cmp_key())

    def __lt__(self, other):
        if not isinstance(other, PackageReference):
            return NotImplemented
        return self._cmp_key() < other._cmp_key()

    def __eq__(self, other):
        if not isinstance(other, PackageReference):
            return NotImplemented
        return self._cmp_key() == other._cmp_key()

    def _cmp_key(self):
        return self.manifest.name, self.manifest.version


@dataclass(eq=False, order=False)
class LocalPackageReference(PackageReference):
    path: PurePath


@dataclass(eq=False, order=False)
class RemotePackageReference(PackageReference):
    url: str


@dataclass(eq=False, order=False)
class InstalledPackageReference(PackageReference):
    pass
