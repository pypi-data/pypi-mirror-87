from unittest import TestCase

from core_get.package.variant.variant_matcher import VariantMatcher


class TestVersionMatcher(TestCase):
    def test_is_match_matches_any_device(self):
        matcher = VariantMatcher()
        is_match = matcher.is_match('*', 'LCMXO3L-4300C-5BG324C')
        self.assertEqual(True, is_match)

    def test_is_match_matches_specific_device_family(self):
        matcher = VariantMatcher()
        is_match = matcher.is_match('LCMXO3L-*', 'LCMXO3L-4300C-5BG324C')
        self.assertEqual(True, is_match)

    def test_is_match_does_not_match_wrong_device_family(self):
        matcher = VariantMatcher()
        is_match = matcher.is_match('LCMXO3L-*', '10CX220YU484E5G')
        self.assertEqual(False, is_match)
