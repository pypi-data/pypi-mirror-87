from unittest import TestCase

from core_get.package.manifest import VariantManifest
from core_get.package.variant.manifest_variant_matcher import ManifestVariantMatcher
from core_get.package.variant.variant_matcher import VariantMatcher


class TestManifestVariantMatcher(TestCase):
    def test_matches_correct_variant(self):
        variant_manifests = {
            'variant1': VariantManifest('MYFPGA6-*', []),
            'variant2': VariantManifest('MYFPGA5-*', []),
        }
        variant_matcher = VariantMatcher()
        manifest_variant_matcher = ManifestVariantMatcher(variant_matcher)
        variant_name = manifest_variant_matcher.match_variant('MYFPGA5-BGA384', variant_manifests)
        self.assertEqual('variant2', variant_name)

    def test_matches_no_variant(self):
        variant_manifests = {
            'variant1': VariantManifest('MYFPGA6-*', []),
            'variant2': VariantManifest('MYFPGA5-*', []),
        }
        variant_matcher = VariantMatcher()
        manifest_variant_matcher = ManifestVariantMatcher(variant_matcher)
        variant_name = manifest_variant_matcher.match_variant('MYFPGA7-BGA384', variant_manifests)
        self.assertEqual(None, variant_name)

    def test_matches_several_variants(self):
        variant_manifests = {
            'variant1': VariantManifest('*', []),
            'variant2': VariantManifest('MYFPGA6-*', []),
        }
        variant_matcher = VariantMatcher()
        manifest_variant_matcher = ManifestVariantMatcher(variant_matcher)
        variant_name = manifest_variant_matcher.match_variant('MYFPGA6-BGA384', variant_manifests)
        self.assertEqual(None, variant_name)
