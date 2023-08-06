from dataclasses import dataclass
from logging import getLogger
from pathlib import PurePath

from injector import inject
from semver import VersionInfo

from core_get.actions.action import Action
from core_get.actions.init.init_options import InitOptions
from core_get.configuration.installed_packages import InstalledPackages
from core_get.configuration.installed_packages_accessor import InstalledPackagesAccessor
from core_get.file.file_system import FileSystem
from core_get.package.manifest import Manifest, VariantManifest
from core_get.package.package_manifest_accessor import PackageManifestAccessor
from core_get.vendor.project_finder import ProjectFinder

logger = getLogger(__name__)


@inject
@dataclass
class Init(Action):
    project_finder: ProjectFinder
    installed_packages_accessor: InstalledPackagesAccessor
    package_manifest_accessor: PackageManifestAccessor
    file_system: FileSystem

    def exec(self, options: InitOptions):
        project_path = options.path
        project = self.project_finder.find_project(project_path)
        if project is None:
            return

        installed_packages = InstalledPackages(project.get_device(), [])
        self.installed_packages_accessor.write(installed_packages)

        package_name = self.file_system.get_file_name(project_path)
        default_variant_manifest = VariantManifest("*", ["src/**/*.vhd"])

        manifest = Manifest(name=package_name, version=VersionInfo.parse("0.0.0"), library=package_name,
                            device=project.get_device(), dependencies=[], lib_path=PurePath('external'),
                            variant_manifests={"default": default_variant_manifest})
        self.package_manifest_accessor.write(manifest)

        logger.info("Package {} with device {} initialized".format(package_name, installed_packages.device))
