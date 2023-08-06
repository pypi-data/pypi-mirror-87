from pathlib import PurePath
from unittest import TestCase
from unittest.mock import Mock

from core_get.package.manifest import Manifest, VariantManifest
from core_get.package.package_maker import PackageMaker


class TestPackageMaker(TestCase):
    def test_package_zips_right_directory(self):
        project_directory_manager = Mock()
        project_directory_manager.get_project_directory = Mock(return_value=PurePath('./myproj'))
        package_manifest_accessor = Mock()
        manifest = Manifest('myproj', variant_manifests={'my_variant': VariantManifest('MYDEVICE', ['a', 'b'])})
        package_manifest_accessor.read = Mock(return_value=manifest)
        zip_service = Mock()
        package_maker = PackageMaker(project_directory_manager, package_manifest_accessor, zip_service)
        package_maker.package(PurePath('./myproj.core'))
        zip_service.make_zip_file.assert_called_once_with(PurePath('./myproj.core'), PurePath('./myproj'), ['a', 'b'])
