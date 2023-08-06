from dataclasses import dataclass
from pathlib import PurePath
from typing import Optional

from injector import inject, noninjectable

from core_get.configuration.environment_settings import EnvironmentSettings
from core_get.file.file_system import FileSystem


@inject
@noninjectable('project_directory')
@dataclass
class ProjectDirectoryManager:
    environment_settings: EnvironmentSettings
    file_system: FileSystem
    project_directory: PurePath = None

    def set_project_directory(self, project_directory: PurePath) -> None:
        self.project_directory = project_directory

    def get_project_directory(self) -> PurePath:
        if self.project_directory is None:
            self.project_directory = self.internal_find_project_directory()
            if self.project_directory is None:
                raise ValueError
        return self.project_directory

    def internal_find_project_directory(self) -> Optional[PurePath]:
        if self.environment_settings.project_dir is not None:
            if self.is_project_directory(self.environment_settings.project_dir):
                return self.environment_settings.project_dir
            return None

        project_dir_candidates = self.file_system.get_hierarchy(self.environment_settings.working_dir)
        for project_dir_candidate in project_dir_candidates:
            if self.is_project_directory(project_dir_candidate):
                return project_dir_candidate

        return None

    def is_project_directory(self, directory: PurePath) -> bool:
        return bool(self.file_system.glob(directory, 'Core.toml'))
