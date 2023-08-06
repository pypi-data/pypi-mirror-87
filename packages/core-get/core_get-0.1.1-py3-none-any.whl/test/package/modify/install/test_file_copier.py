from pathlib import PurePath
from unittest import TestCase
from unittest.mock import Mock

from core_get.configuration.installed_packages import InstalledFile
from core_get.file.flat.flat_directory import FlatDirectory
from core_get.package.manifest import Manifest, VariantManifest
from core_get.package.modify.install.file_copier import FileCopier
from core_get.package.modify.install.install_order import InstallOrder
from core_get.package.reference.package_reference import PackageReference


class TestFileCopier(TestCase):
    def test_copy_package_files(self):
        file_system = Mock()
        file_system.write_stream = Mock(return_value=b'00112233445566778899AABBCCDDEEFF00112233445566778899AABBCCDDEEFF')
        flat_file = Mock()
        flat_file.path = PurePath('src/a.vhdl')
        stream = Mock()
        stream.__enter__ = Mock(return_value=stream)
        stream.__exit__ = Mock()
        flat_file.open = Mock(return_value=stream)
        flat_directory = FlatDirectory([flat_file])
        file_copier = FileCopier(file_system)
        manifest = Manifest('my_package', variant_manifests={'my_variant': VariantManifest('MYDEV', ['src/*'])})
        reference = PackageReference(manifest)
        install_order = InstallOrder(reference, 'my_variant', PurePath(''), True)
        installed_files = file_copier.copy_package_files(install_order, flat_directory)
        self.assertEqual([InstalledFile(PurePath('src/a.vhdl'), b'00112233445566778899AABBCCDDEEFF00112233445566778899AABBCCDDEEFF')], installed_files)
