from argparse import ArgumentParser, Namespace
from dataclasses import dataclass

from core_get.actions.login.login_options import LoginOptions
from core_get.options.options import Options
from core_get.cli.parse.parser import Parser


@dataclass
class LoginOptionsParser(Parser):
    name: str = 'login'
    usage: str = '<access-token>'
    description: str = 'Store the access token to publish and yank packages'

    def add_arguments(self, argument_parser: ArgumentParser) -> None:
        argument_parser.add_argument('access_token', help='Access token')

    def make_options(self, namespace: Namespace) -> Options:
        return LoginOptions(namespace.access_token)
