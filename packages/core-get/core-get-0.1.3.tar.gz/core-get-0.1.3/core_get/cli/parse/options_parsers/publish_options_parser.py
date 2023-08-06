from argparse import ArgumentParser, Namespace
from dataclasses import dataclass

from core_get.actions.publish.publish_options import PublishOptions
from core_get.options.options import Options
from core_get.cli.parse.parser import Parser


@dataclass
class PublishOptionsParser(Parser):
    name: str = 'publish'
    usage: str = ''
    description: str = 'Publish a package'

    def add_arguments(self, argument_parser: ArgumentParser) -> None:
        pass

    def make_options(self, namespace: Namespace) -> Options:
        return PublishOptions()
