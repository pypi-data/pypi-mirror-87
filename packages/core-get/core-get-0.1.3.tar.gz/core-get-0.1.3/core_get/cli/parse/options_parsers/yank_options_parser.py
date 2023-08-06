from argparse import ArgumentParser, Namespace
from dataclasses import dataclass

from core_get.actions.yank.yank_options import YankOptions
from core_get.cli.parse.parser import Parser
from core_get.options.options import Options


@dataclass
class YankOptionsParser(Parser):
    name: str = 'yank'
    usage: str = '<version>'
    description: str = 'Yank a version of the project package'

    def add_arguments(self, argument_parser: ArgumentParser) -> None:
        argument_parser.add_argument('version', help='Package version')

    def make_options(self, namespace: Namespace) -> Options:
        return YankOptions(namespace.version)
