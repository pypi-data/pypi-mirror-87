import zipfile
from dataclasses import dataclass
from logging import getLogger
from pathlib import PurePath, Path

from injector import inject

from core_get.configuration.project_directory_finder import ProjectDirectoryManager
from core_get.file.zip_service import ZipService
from core_get.package.package_manifest_accessor import PackageManifestAccessor

logger = getLogger(__name__)


@inject
@dataclass
class PackageMaker:
    project_directory_manager: ProjectDirectoryManager
    package_manifest_accessor: PackageManifestAccessor
    zip_service: ZipService

    def package(self, output_path: PurePath) -> None:
        project_path = self.project_directory_manager.get_project_directory()
        if project_path is None:
            logger.error('No package directory found')
            return

        manifest = self.package_manifest_accessor.read()
        include = [include for variant_manifest in manifest.variant_manifests.values()
                   for include in variant_manifest.include]

        self.zip_service.make_zip_file(output_path, project_path, include)
        #
        # project_path_path = Path(project_path)
        # all_files = [file.relative_to(project_path) for pattern in include
        #              for file in project_path_path.glob(pattern)]
        # all_files.append(Path("Core.toml"))
        #
        # with zipfile.ZipFile(package_path, 'w') as zip_file:
        #     for file in all_files:
        #         data = (project_path_path / file).read_bytes()
        #         zip_file.writestr(file.as_posix(), data)
