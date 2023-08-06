import unittest
from unittest.mock import Mock
from core_get.cli.parse.parser_selector import ParserSelector, InvalidCommandError


class TestParserSelector(unittest.TestCase):
    def test_parse_command_finds_command(self):
        parser = Mock()
        parser.name = 'test_command'
        parser.usage = '<test-id>'
        parser_selector = ParserSelector()
        returned_parser = parser_selector.select_parser([parser], ['test_command'])
        self.assertEqual(parser, returned_parser)

    def test_parse_command_invalid_command(self):
        parser = Mock()
        parser.name = 'test_command'
        parser.usage = '<test-id>'
        parser_selector = ParserSelector()
        with self.assertRaises(InvalidCommandError):
            _ = parser_selector.select_parser([parser], ['test_invalid_command'])

    def test_parse_command_no_command_with_flag(self):
        parser_selector = ParserSelector()
        returned_parser = parser_selector.select_parser([], ['--my-flag'])
        self.assertIs(None, returned_parser)
