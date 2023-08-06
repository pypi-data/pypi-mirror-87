from dataclasses import dataclass
from pathlib import PurePath
from typing import List

from injector import inject

from core_get.file.file_system import FileSystem
from core_get.vendor.diamond.diamond_project import DiamondProjectReader
from core_get.vendor.project import Project
from core_get.vendor.project_discoverer import ProjectDiscoverer


@inject
@dataclass
class DiamondProjectDiscoverer(ProjectDiscoverer):
    diamond_project_reader: DiamondProjectReader
    file_system: FileSystem

    def discover(self, directory: PurePath) -> List[Project]:
        return [self.diamond_project_reader.read(ldf_file)
                for ldf_file in self.file_system.glob(directory, '*.ldf')]
