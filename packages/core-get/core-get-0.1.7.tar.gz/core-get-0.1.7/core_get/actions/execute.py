from dataclasses import dataclass
from pathlib import Path, PurePath

from appdirs import user_data_dir
from injector import Injector, Module, Binder

from core_get.actions.action_executor import ActionExecutor
from core_get.actions.module import ActionsModule
from core_get.configuration.environment_settings import EnvironmentSettings
from core_get.options.common_options import CommonOptions
from core_get.options.options import Options
from core_get.vendor.module import VendorModule

APP_NAME = 'core-get'
APP_AUTHOR = 'peppar'


@dataclass
class CommonOptionsModule(Module):
    common_options: CommonOptions

    def configure(self, binder: Binder) -> None:
        binder.bind(CommonOptions, self.common_options)
        binder.bind(EnvironmentSettings, self.make_environment_settings())

    def make_environment_settings(self) -> EnvironmentSettings:
        working_dir = self.common_options.working_dir if self.common_options.working_dir is not None else Path.cwd()
        project_dir = self.common_options.project_dir
        app_dir = PurePath(user_data_dir(APP_NAME, APP_AUTHOR))
        cache_dir = app_dir / 'cache'
        catalog_url = "http://localhost:8000"
        return EnvironmentSettings(working_dir, project_dir, app_dir, cache_dir, catalog_url)


def execute(common_options: CommonOptions, specific_options: Options, app_module: Module) -> int:

    injector = Injector([
        CommonOptionsModule(common_options),
        ActionsModule(),
        VendorModule(),
        app_module,
    ])

    action_executor = injector.get(ActionExecutor)
    action_executor.execute_action(specific_options)

    return 0
