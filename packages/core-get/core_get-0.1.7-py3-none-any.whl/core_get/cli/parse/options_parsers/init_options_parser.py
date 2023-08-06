from argparse import ArgumentParser, Namespace
from dataclasses import dataclass
from pathlib import PurePath

from core_get.actions.init.init_options import InitOptions
from core_get.options.options import Options
from core_get.cli.parse.parser import Parser


@dataclass
class InitOptionsParser(Parser):
    name: str = 'init'
    usage: str = '<package-names>'
    description: str = 'Initialize a repository'

    def add_arguments(self, argument_parser: ArgumentParser) -> None:
        argument_parser.add_argument('path', help='Path to initialize')

    def make_options(self, namespace: Namespace) -> Options:
        return InitOptions(PurePath(namespace.path))
