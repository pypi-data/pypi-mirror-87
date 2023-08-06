from argparse import ArgumentParser
from typing import List

from core_get.cli.parse.parser import Parser
from core_get.options.options import Options


class CompositeParser:
    def parse(self, parsers: List[Parser], args: List[str], description: str = None, usage: str = None) \
            -> List[Options]:
        argument_parser = ArgumentParser(description=description, usage=usage)
        for parser in parsers:
            parser.add_arguments(argument_parser)
        namespace = argument_parser.parse_args(args)
        return [parser.make_options(namespace) for parser in parsers]
