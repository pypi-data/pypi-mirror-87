from pathlib import PurePath
from unittest import TestCase
from unittest.mock import Mock

from core_get.package.manifest import Manifest, VariantManifest
from core_get.package.modify.install.install_order import InstallOrder
from core_get.package.modify.install.install_order_maker import InstallOrderMaker
from core_get.package.reference.package_reference import PackageReference


class TestInstallOrderMaker(TestCase):
    def test_make(self):
        manifest_variant_matcher = Mock()
        manifest_variant_matcher.match_variant = Mock(return_value='my_variant')
        install_order_maker = InstallOrderMaker(manifest_variant_matcher)
        variant_manifest = VariantManifest('MYDEVICE', ['src/*'])
        manifest = Manifest('my_package', variant_manifests={'my_variant': variant_manifest})
        package_reference = PackageReference(manifest)
        install_order = install_order_maker.make('MYDEVICE', package_reference, PurePath('./extern'), True)
        self.assertEqual(InstallOrder(package_reference, 'my_variant', PurePath('./extern/my_package-0.0.0'), True), install_order)
