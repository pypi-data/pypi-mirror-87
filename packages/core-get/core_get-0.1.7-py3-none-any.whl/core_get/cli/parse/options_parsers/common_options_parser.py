from argparse import ArgumentParser, Namespace
from pathlib import Path

from core_get.cli.parse.parser import Parser
from core_get.options.common_options import CommonOptions
from core_get.options.options import Options


class CommonOptionsParser(Parser):

    def add_arguments(self, argument_parser: ArgumentParser) -> None:
        argument_parser.add_argument('--dry-run', action='store_true',
                                     help='Dry run; do not commit any changes to disk or network')
        argument_parser.add_argument('--project-dir', default=None,
                                     help='Specify directory of project')
        argument_parser.add_argument('-C', default=None, dest='working_dir',
                                     help='Specify the working directory')
        argument_parser.add_argument('--offline', action='store_true',
                                     help='Forbid all network activity')

    def make_options(self, namespace: Namespace) -> Options:
        return CommonOptions(namespace.dry_run, namespace.offline,
                             Path(namespace.project_dir) if namespace.project_dir is not None else None,
                             Path(namespace.working_dir) if namespace.working_dir is not None else None)
