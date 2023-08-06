from dataclasses import dataclass
from pathlib import PurePath, PurePosixPath
from typing import List
from xml.etree import ElementTree

from injector import inject

from core_get.file.file_system import FileSystem
from core_get.vendor.project import Project
from core_get.vendor.project_source_file import ProjectSourceFile


def get_implementation(root: ElementTree.Element) -> ElementTree.Element:
    default_implementation = root.attrib['default_implementation']
    return [impl for impl in root.findall('Implementation')
            if impl.get('title') == default_implementation][0]


@dataclass
class DiamondProject(Project):
    ldf_path: PurePath
    root: ElementTree.Element
    file_system: FileSystem

    def get_device(self) -> str:
        return self.root.attrib['device']

    def get_source_files(self) -> List[ProjectSourceFile]:
        impl = get_implementation(self.root)
        return [ProjectSourceFile(PurePosixPath(source_file.attrib['name']))
                for source_file in impl.findall('Source')]

    def add_source_files(self, source_files: List[ProjectSourceFile]) -> None:
        impl = get_implementation(self.root)
        for source_file in source_files:
            attributes = {
                'name': str(source_file.path.as_posix())
            }
            element = ElementTree.Element('Source', attributes)
            impl.append(element)

    def remove_source_files(self, source_files: List[ProjectSourceFile]) -> None:
        impl = get_implementation(self.root)
        paths = set(source_file.path.as_posix() for source_file in source_files)
        for element in impl.findall('Source'):
            if element.attrib['name'] in paths:
                impl.remove(element)

    def write(self) -> None:
        self.file_system.write_file(self.ldf_path, ElementTree.tostring(self.root))


@inject
@dataclass
class DiamondProjectReader:
    file_system: FileSystem

    def read(self, ldf_path: PurePath) -> DiamondProject:
        data = self.file_system.read_file(ldf_path)
        try:
            root = ElementTree.fromstring(data)
        except ElementTree.ParseError:
            raise ValueError()
        if root.tag != 'BaliProject':
            raise ValueError()
        return DiamondProject(ldf_path, root, self.file_system)
