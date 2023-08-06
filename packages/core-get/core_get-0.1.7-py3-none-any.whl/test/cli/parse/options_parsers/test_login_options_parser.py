from unittest import TestCase

from core_get.cli.parse.options_parsers.login_options_parser import LoginOptionsParser
from test.cli.parse.options_parsers.options_parser_test_helper import do_test_parse


class TestLoginOptionsParser(TestCase):
    def test_parses_access_token_correctly(self):
        login_options = do_test_parse(LoginOptionsParser, 'abc123')
        self.assertEqual('abc123', login_options.access_token)

    def test_fails_with_no_access_token(self):
        with self.assertRaises(SystemExit):
            do_test_parse(LoginOptionsParser)
