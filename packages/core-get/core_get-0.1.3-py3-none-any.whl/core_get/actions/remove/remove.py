from dataclasses import dataclass
from logging import getLogger

from injector import inject

from core_get.actions.action import Action
from core_get.package.modify.package_modifier import PackageModifier
from core_get.actions.remove.remove_options import RemoveOptions

logger = getLogger(__name__)


@inject
@dataclass
class Remove(Action):
    package_modifier: PackageModifier

    def exec(self, options: RemoveOptions) -> None:
        self.package_modifier.modify_packages([], options.package_names, options.force)
