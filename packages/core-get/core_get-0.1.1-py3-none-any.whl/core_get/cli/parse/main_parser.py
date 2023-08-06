from dataclasses import dataclass
from logging import getLogger
from typing import List, Optional

from injector import inject

from core_get.cli.parse.composite_parser import CompositeParser
from core_get.cli.parse.options_parsers.common_options_parser import CommonOptionsParser
from core_get.cli.parse.parser import Parser
from core_get.cli.parse.parser_selector import ParserSelector, InvalidCommandError
from core_get.options.options import Options

logger = getLogger(__name__)


@inject
@dataclass
class MainParser:
    common_options_parser: CommonOptionsParser
    all_parsers: List[Parser]
    parser_selector: ParserSelector
    composite_parser: CompositeParser

    def parse(self, args: List[str]) -> Optional[List[Options]]:
        try:
            parser = self.parser_selector.select_parser(self.all_parsers, args[1:])
        except InvalidCommandError as e:
            command_name_list = self.make_command_name_list(self.all_parsers)
            logger.error(f'Invalid command name {e.command_name}\nValid commands are: {command_name_list}')
            return None
        if parser is None:
            usage_string = self.make_usage_string(self.all_parsers)
            logger.info(f'Usage:\n{usage_string}')
            return None
        return self.composite_parser.parse([self.common_options_parser, parser], args[2:],
                                           parser.description, parser.usage)

    def make_command_name_list(self, parsers: List[Parser]) -> str:
        return ', '.join(parser.name for parser in parsers)

    def make_usage_string(self, parsers: List[Parser]) -> str:
        return 'core-get <command> [<args>]\n\n' + \
               '\n'.join(f'core-get {parser.name} {parser.usage}' for parser in parsers)
