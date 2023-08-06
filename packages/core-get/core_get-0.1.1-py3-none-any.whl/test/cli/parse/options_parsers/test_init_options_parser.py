from pathlib import PurePath
from unittest import TestCase

from core_get.cli.parse.options_parsers.init_options_parser import InitOptionsParser
from test.cli.parse.options_parsers.options_parser_test_helper import do_test_parse


class TestInitOptionsParser(TestCase):
    def test_parses_relative_path_correctly(self):
        init_options = do_test_parse(InitOptionsParser, './..')
        self.assertEqual(PurePath('./..'), init_options.path)

    def test_parses_path_correctly(self):
        init_options = do_test_parse(InitOptionsParser, 'my-path')
        self.assertEqual(PurePath('my-path'), init_options.path)
