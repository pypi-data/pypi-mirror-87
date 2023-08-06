from dataclasses import dataclass
from logging import getLogger
from pathlib import PurePath
from typing import List, Optional

from injector import inject

from core_get.configuration.project_directory_finder import ProjectDirectoryManager
from core_get.vendor.project import Project
from core_get.vendor.project_discoverer import ProjectDiscoverer

logger = getLogger(__name__)


@inject
@dataclass
class ProjectFinder:
    project_directory_finder: ProjectDirectoryManager
    project_discoverers: List[ProjectDiscoverer]

    def find_project(self, project_path: PurePath = None) -> Optional[Project]:
        if project_path is None:
            project_path = self.project_directory_finder.get_project_directory()
        projects = [project for project_discoverer in self.project_discoverers
                    for project in project_discoverer.discover(project_path)]
        if len(projects) == 0:
            logger.error('No projects found in the current directory')
            return None
        elif len(projects) > 1:
            logger.error('More than one project found')
            return None
        return projects[0]
