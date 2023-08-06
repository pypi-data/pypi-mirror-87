from dataclasses import dataclass
from logging import getLogger

from injector import inject

from core_get.actions.action import Action
from core_get.actions.publish.publish_options import PublishOptions
from core_get.catalog.catalog_service import CatalogService
from core_get.configuration.environment_settings import EnvironmentSettings
from core_get.package.package_maker import PackageMaker
from core_get.package.package_manifest_accessor import PackageManifestAccessor

logger = getLogger(__name__)


@inject
@dataclass
class Publish(Action):
    package_manifest_accessor: PackageManifestAccessor
    environment_settings: EnvironmentSettings
    package_maker: PackageMaker
    catalog_service: CatalogService

    def exec(self, options: PublishOptions):
        manifest = self.package_manifest_accessor.read()
        package_path = self.environment_settings.app_dir / f"{manifest.name}-{manifest.version}.core"
        self.package_maker.package(package_path)
        self.catalog_service.publish_package(manifest.name, package_path)
