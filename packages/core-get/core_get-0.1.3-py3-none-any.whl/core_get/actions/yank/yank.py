from dataclasses import dataclass
from logging import getLogger

from injector import inject

from core_get.actions.action import Action
from core_get.actions.yank.yank_options import YankOptions
from core_get.catalog.catalog_service import CatalogService
from core_get.package.package_manifest_accessor import PackageManifestAccessor

logger = getLogger(__name__)


@inject
@dataclass
class Yank(Action):
    package_manifest_accessor: PackageManifestAccessor
    catalog_service: CatalogService

    def exec(self, options: YankOptions):
        manifest = self.package_manifest_accessor.read()
        self.catalog_service.yank_package(manifest.name, options.version)
