from typing import Dict, Type

from injector import Module, Binder

from core_get.actions.action import Action
from core_get.actions.init.init import Init
from core_get.actions.init.init_options import InitOptions
from core_get.actions.install.install import Install
from core_get.actions.install.install_options import InstallOptions
from core_get.actions.login.login import Login
from core_get.actions.login.login_options import LoginOptions
from core_get.actions.package.package import Package
from core_get.actions.package.package_options import PackageOptions
from core_get.actions.publish.publish import Publish
from core_get.actions.publish.publish_options import PublishOptions
from core_get.actions.remove.remove import Remove
from core_get.actions.remove.remove_options import RemoveOptions
from core_get.actions.yank.yank import Yank
from core_get.actions.yank.yank_options import YankOptions
from core_get.options.options import Options
from core_get.utils.injection import MultiMapClassProvider


class ActionsModule(Module):

    def configure(self, binder: Binder) -> None:
        binder.multibind(Dict[Type[Options], Action], to=MultiMapClassProvider({
            InitOptions: Init,
            InstallOptions: Install,
            LoginOptions: Login,
            PackageOptions: Package,
            PublishOptions: Publish,
            RemoveOptions: Remove,
            YankOptions: Yank,
        }))
