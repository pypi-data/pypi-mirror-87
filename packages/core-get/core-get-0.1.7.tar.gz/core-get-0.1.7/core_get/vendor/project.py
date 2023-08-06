from __future__ import annotations

from core_get.vendor.project_source_file import ProjectSourceFile


class Project:
    def get_device(self) -> str:
        raise NotImplementedError

    def get_source_files(self) -> [ProjectSourceFile]:
        raise NotImplementedError

    def add_source_files(self, source_files: [ProjectSourceFile]) -> None:
        raise NotImplementedError

    def remove_source_files(self, source_files: [ProjectSourceFile]) -> None:
        raise NotImplementedError

    def write(self) -> None:
        raise NotImplementedError

