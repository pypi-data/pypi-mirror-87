from pathlib import PurePath, PurePosixPath
from unittest import TestCase
from unittest.mock import Mock

from core_get.vendor.diamond.diamond_project import DiamondProject, DiamondProjectReader
from core_get.vendor.project_source_file import ProjectSourceFile


class TestDiamondProject(TestCase):

    def parse(self, s: bytes) -> DiamondProject:
        file_system = Mock()
        file_system.read_file = Mock(return_value=s)
        diamond_project_reader = DiamondProjectReader(file_system)
        return diamond_project_reader.read(PurePath('test.ldf'))

    def get_example_diamond_project(self) -> DiamondProject:
        return self.parse(b'''<?xml version="1.0" encoding="UTF-8"?>
        <BaliProject version="3.2" title="myfpga" device="mydevice" default_implementation="impl1">
        <Options/>
        <Implementation title="impl1" dir="impl1" description="impl1" synthesis="synplify" default_strategy="Strategy1">
        <Source name="src/file1.vhd" type="VHDL" type_short="VHDL"><Options/></Source>
        </Implementation>
        </BaliProject>''')

    def test_get_device_returns_example_device(self):
        project = self.get_example_diamond_project()
        device = project.get_device()
        self.assertEqual(device, 'mydevice')

    def test_get_source_files_returns_correct_files(self):
        project = self.get_example_diamond_project()
        source_files = project.get_source_files()
        self.assertEqual(source_files, [ProjectSourceFile(PurePosixPath('src/file1.vhd'))])

    def test_add_source_files_adds_correct_file(self):
        project = self.get_example_diamond_project()
        project.add_source_files([ProjectSourceFile(PurePath('src/file2.vhd'))])
        source_files = project.get_source_files()
        self.assertEqual(source_files, [ProjectSourceFile(PurePosixPath('src/file1.vhd')),
                                        ProjectSourceFile(PurePosixPath('src/file2.vhd'))])

    def test_remove_source_files_removes_correct_file(self):
        project = self.get_example_diamond_project()
        project.remove_source_files([ProjectSourceFile(PurePosixPath('src/file1.vhd'))])
        source_files = project.get_source_files()
        self.assertEqual(source_files, [])

    def test_parse_fails_due_to_invalid_root_tag(self):
        contents = b'''<?xml version="1.0" encoding="UTF-8"?>
<ErrorProject/>'''
        with self.assertRaises(ValueError):
            self.parse(contents)

    def test_parse_fails_due_to_invalid_xml(self):
        contents = b'''<?xml version="1.0" encoding="UTF-8"?>
<ErrorProject>'''
        with self.assertRaises(ValueError):
            self.parse(contents)
