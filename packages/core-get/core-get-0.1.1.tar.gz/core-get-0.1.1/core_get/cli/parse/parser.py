from argparse import ArgumentParser
from dataclasses import dataclass

from core_get.options.options import Options


@dataclass
class Parser:
    name: str = ''
    usage: str = ''
    description: str = ''

    def add_arguments(self, argument_parser: ArgumentParser) -> None:
        raise NotImplementedError

    def make_options(self, namespace) -> Options:
        raise NotImplementedError
