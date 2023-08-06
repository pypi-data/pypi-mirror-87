from dataclasses import dataclass
from typing import Dict, Optional

from injector import inject

from core_get.package.manifest import VariantManifest
from core_get.package.variant.variant_matcher import VariantMatcher


@inject
@dataclass
class ManifestVariantMatcher:
    variant_matcher: VariantMatcher

    def match_variant(self, device: str, variant_manifests: Dict[str, VariantManifest]) -> Optional[str]:
        matched_variant_names = [name for name, variant_manifest in variant_manifests.items()
                                 if self.variant_matcher.is_match(variant_manifest.target_device, device)]
        if len(matched_variant_names) != 1:
            return None
        return matched_variant_names[0]
