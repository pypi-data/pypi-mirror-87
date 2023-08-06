from argparse import ArgumentParser, Namespace
from dataclasses import dataclass

from core_get.actions.package.package_options import PackageOptions
from core_get.options.options import Options
from core_get.cli.parse.parser import Parser


@dataclass
class PackageOptionsParser(Parser):
    name: str = 'package'
    usage: str = ''
    description: str = 'Assemble the local package into a distributable zip file'

    def add_arguments(self, argument_parser: ArgumentParser) -> None:
        pass

    def make_options(self, namespace: Namespace) -> Options:
        return PackageOptions()
