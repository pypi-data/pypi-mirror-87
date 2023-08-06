from dataclasses import dataclass

from injector import inject

from core_get.actions.action import Action
from core_get.actions.install.install_options import InstallOptions
from core_get.package.modify.package_modifier import PackageModifier


@inject
@dataclass
class Install(Action):
    package_modifier: PackageModifier

    def exec(self, options: InstallOptions) -> None:
        self.package_modifier.modify_packages(options.package_names, [], False)
