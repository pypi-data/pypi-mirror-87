from dataclasses import dataclass
from pathlib import PurePath
from typing import Optional

from core_get.package.reference.package_reference import PackageReference


@dataclass
class InstallOrder:
    reference: PackageReference
    variant: Optional[str]
    install_path: PurePath
    is_direct: bool
