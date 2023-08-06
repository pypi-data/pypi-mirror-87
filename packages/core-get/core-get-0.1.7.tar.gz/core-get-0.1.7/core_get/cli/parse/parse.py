from typing import List, Optional, Tuple, NamedTuple

from injector import Module, Binder, Injector

from core_get.cli.parse.options_parsers.init_options_parser import InitOptionsParser
from core_get.cli.parse.options_parsers.install_options_parser import InstallOptionsParser
from core_get.cli.parse.options_parsers.login_options_parser import LoginOptionsParser
from core_get.cli.parse.main_parser import MainParser
from core_get.cli.parse.options_parsers.package_options_parser import PackageOptionsParser
from core_get.cli.parse.options_parsers.yank_options_parser import YankOptionsParser
from core_get.cli.parse.parser import Parser
from core_get.cli.parse.options_parsers.publish_options_parser import PublishOptionsParser
from core_get.cli.parse.options_parsers.remove_options_parser import RemoveOptionsParser
from core_get.options.common_options import CommonOptions
from core_get.options.options import Options
from core_get.utils.injection import MultiClassProvider


class ParsersModule(Module):

    def configure(self, binder: Binder) -> None:
        binder.multibind(List[Parser], to=MultiClassProvider([
            InitOptionsParser,
            InstallOptionsParser,
            LoginOptionsParser,
            PackageOptionsParser,
            PublishOptionsParser,
            RemoveOptionsParser,
            YankOptionsParser,
        ]))


class ParseResult(NamedTuple):
    common_options: CommonOptions
    specific_options: Options


def parse_options(args: List[str]) -> Optional[ParseResult]:
    injector = Injector([ParsersModule()])
    main_parser = injector.get(MainParser)
    options = main_parser.parse(args)
    if options is None:
        return None
    return ParseResult(*options)
