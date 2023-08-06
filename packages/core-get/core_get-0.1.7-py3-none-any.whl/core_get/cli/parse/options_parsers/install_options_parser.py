from argparse import ArgumentParser, Namespace
from dataclasses import dataclass

from core_get.actions.install.install_options import InstallOptions
from core_get.options.options import Options
from core_get.cli.parse.parser import Parser


@dataclass
class InstallOptionsParser(Parser):
    name: str = 'install'
    usage: str = '<package-names>'
    description: str = 'Install a package'

    def add_arguments(self, argument_parser: ArgumentParser) -> None:
        argument_parser.add_argument('package_names', nargs='+', help='Package names to install')

    def make_options(self, namespace: Namespace) -> Options:
        return InstallOptions(namespace.package_names)
