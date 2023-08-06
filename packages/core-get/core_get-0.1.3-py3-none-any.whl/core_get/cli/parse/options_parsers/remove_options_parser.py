from argparse import ArgumentParser, Namespace
from dataclasses import dataclass

from core_get.actions.remove.remove_options import RemoveOptions
from core_get.options.options import Options
from core_get.cli.parse.parser import Parser


@dataclass
class RemoveOptionsParser(Parser):
    name: str = 'remove'
    usage: str = '<package-name>'
    description: str = 'Remove a package'

    def add_arguments(self, argument_parser: ArgumentParser) -> None:
        argument_parser.add_argument('package_names', nargs='+', help='Package names to remove')
        argument_parser.add_argument('--force', action='store_true',
                                     help='Force remove modified packages')

    def make_options(self, namespace: Namespace) -> Options:
        return RemoveOptions(namespace.package_names, namespace.force)
