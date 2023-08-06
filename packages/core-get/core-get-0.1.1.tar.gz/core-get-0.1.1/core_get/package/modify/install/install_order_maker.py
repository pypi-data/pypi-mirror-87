from dataclasses import dataclass
from pathlib import PurePath

from injector import inject

from core_get.package.modify.install.install_order import InstallOrder
from core_get.package.reference.package_reference import PackageReference
from core_get.package.variant.manifest_variant_matcher import ManifestVariantMatcher


@inject
@dataclass
class InstallOrderMaker:
    manifest_variant_matcher: ManifestVariantMatcher

    def make(self, device: str, reference: PackageReference, lib_path: PurePath, is_direct: bool) -> InstallOrder:
        variant = self.manifest_variant_matcher.match_variant(device, reference.manifest.variant_manifests)
        manifest_name = reference.manifest.qualified_name()
        install_path = lib_path / manifest_name
        install_order = InstallOrder(reference, variant, install_path, is_direct)
        return install_order
