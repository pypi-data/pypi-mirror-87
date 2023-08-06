import logging
from typing import List

from core_get.actions.execute import execute
from core_get.cli.module import CliModule
from core_get.cli.parse.parse import parse_options


def cli_main(args: List[str]) -> int:
    logger = logging.getLogger('')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())

    options = parse_options(args)
    if options is None:
        return 101

    return execute(options.common_options, options.specific_options, CliModule())
