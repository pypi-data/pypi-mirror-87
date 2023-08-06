from unittest import TestCase
from unittest.mock import Mock

from core_get.cli.parse.main_parser import MainParser
from core_get.cli.parse.parser_selector import InvalidCommandError


class TestMainParser(TestCase):
    def test_does_not_find_parser(self):
        parser_selector = Mock()
        exception = InvalidCommandError('test')
        parser_selector.select_parser = Mock(side_effect=exception)
        composite_parser = Mock()
        main_parser = MainParser(Mock(), [], parser_selector, composite_parser)
        self.assertIsNone(main_parser.parse(['test']))

    def test_finds_parser(self):
        common_options_parser = Mock()
        parser = Mock()
        parser.name = 'test'
        parser_selector = Mock()
        parser_selector.select_parser = Mock(return_value=parser)
        composite_parser = Mock()
        parsed_options = (Mock(), Mock())
        composite_parser.parse = Mock(return_value=parsed_options)
        main_parser = MainParser(common_options_parser, [parser], parser_selector, composite_parser)
        self.assertEqual(parsed_options, main_parser.parse(['test']))
