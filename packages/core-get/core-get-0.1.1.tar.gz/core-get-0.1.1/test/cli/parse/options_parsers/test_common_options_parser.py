from pathlib import PurePath
from unittest import TestCase

from core_get.cli.parse.options_parsers.common_options_parser import CommonOptionsParser
from test.cli.parse.options_parsers.options_parser_test_helper import do_test_parse


class TestCommonOptionsParser(TestCase):
    def test_parses_project_dir_correctly(self):
        common_options = do_test_parse(CommonOptionsParser, '--project-dir=./../sauce')
        self.assertEqual(PurePath('./../sauce'), common_options.project_dir)

    def test_ignores_project_dir_correctly(self):
        common_options = do_test_parse(CommonOptionsParser)
        self.assertEqual(None, common_options.project_dir)

    def test_parses_working_dir_correctly(self):
        common_options = do_test_parse(CommonOptionsParser, '-C=./../sauce')
        self.assertEqual(PurePath('./../sauce'), common_options.working_dir)

    def test_parses_dry_run_correctly(self):
        common_options = do_test_parse(CommonOptionsParser, '--dry-run')
        self.assertTrue(common_options.dry_run)

    def test_ignores_dry_run_correctly(self):
        common_options = do_test_parse(CommonOptionsParser)
        self.assertFalse(common_options.dry_run)

    def test_parses_offline_correctly(self):
        common_options = do_test_parse(CommonOptionsParser, '--offline')
        self.assertTrue(common_options.offline)

    def test_ignores_offline_correctly(self):
        common_options = do_test_parse(CommonOptionsParser)
        self.assertFalse(common_options.offline)
