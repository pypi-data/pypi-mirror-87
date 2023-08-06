from dataclasses import dataclass
from logging import getLogger
from pathlib import Path

from injector import inject

from core_get.actions.action import Action
from core_get.actions.package.package_options import PackageOptions
from core_get.configuration.project_directory_finder import ProjectDirectoryManager
from core_get.package.package_maker import PackageMaker
from core_get.package.package_manifest_accessor import PackageManifestAccessor

logger = getLogger(__name__)


@inject
@dataclass
class Package(Action):
    package_maker: PackageMaker
    project_directory_manager: ProjectDirectoryManager
    package_manifest_accessor: PackageManifestAccessor

    def exec(self, options: PackageOptions) -> None:
        project_path = self.project_directory_manager.get_project_directory()
        if project_path is None:
            logger.error('No package directory found')
            return

        manifest = self.package_manifest_accessor.read()
        package_path = Path(project_path) / f"{manifest.name}.core"
        self.package_maker.package(package_path)

        logger.info(f"Created package {package_path.absolute()}")
