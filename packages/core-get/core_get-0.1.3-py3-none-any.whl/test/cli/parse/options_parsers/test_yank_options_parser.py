from unittest import TestCase

from semver import VersionInfo

from core_get.cli.parse.options_parsers.yank_options_parser import YankOptionsParser
from test.cli.parse.options_parsers.options_parser_test_helper import do_test_parse


class TestYankOptionsParser(TestCase):
    def test_parses_version_correctly(self):
        yank_options = do_test_parse(YankOptionsParser, '1.2.3')
        self.assertEqual(VersionInfo.parse('1.2.3'), yank_options.version)

    def test_fails_with_no_version(self):
        with self.assertRaises(SystemExit):
            do_test_parse(YankOptionsParser)
