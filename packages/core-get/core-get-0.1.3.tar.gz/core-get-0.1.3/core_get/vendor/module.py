from typing import List

from injector import Module, Binder

from core_get.utils.injection import MultiClassProvider
from core_get.vendor.diamond.diamond_project_discoverer import DiamondProjectDiscoverer
from core_get.vendor.project_discoverer import ProjectDiscoverer


class VendorModule(Module):

    def configure(self, binder: Binder) -> None:
        binder.multibind(List[ProjectDiscoverer], to=MultiClassProvider([
            DiamondProjectDiscoverer,
        ]))
