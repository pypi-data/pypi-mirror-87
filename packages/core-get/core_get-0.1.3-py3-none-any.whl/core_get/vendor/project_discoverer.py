from pathlib import PurePath
from typing import List

from core_get.vendor.project import Project


class ProjectDiscoverer(object):

    def discover(self, directory: PurePath) -> List[Project]:
        raise NotImplementedError
