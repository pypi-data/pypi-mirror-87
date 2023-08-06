from typing import Optional, List

from core_get.cli.parse.parser import Parser


class InvalidCommandError(KeyError):

    def __init__(self, command_name: str, *args: object) -> None:
        super().__init__(*args)
        self.command_name = command_name


class ParserSelector:

    def select_parser(self, parsers: List[Parser], args: List[str]) -> Optional[Parser]:
        if len(args) == 0:
            return None
        command_name = args[0]
        if command_name.startswith('-'):
            return None
        try:
            return [p for p in parsers if p.name == command_name][0]
        except IndexError:
            raise InvalidCommandError(command_name)
