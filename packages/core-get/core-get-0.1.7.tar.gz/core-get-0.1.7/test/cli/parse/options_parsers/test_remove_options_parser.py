from unittest import TestCase

from core_get.cli.parse.options_parsers.remove_options_parser import RemoveOptionsParser
from test.cli.parse.options_parsers.options_parser_test_helper import do_test_parse


class TestRemoveOptionsParser(TestCase):
    def test_parses_correctly(self):
        remove_options = do_test_parse(RemoveOptionsParser, 'my-package-name')
        self.assertEqual(['my-package-name'], remove_options.package_names)

    def test_parses_two_packages_correctly(self):
        remove_options = do_test_parse(RemoveOptionsParser, 'my-package-1', 'my-package-2')
        self.assertEqual(['my-package-1', 'my-package-2'], remove_options.package_names)

    def test_parses_force_correctly(self):
        remove_options = do_test_parse(RemoveOptionsParser, 'my-package-name', '--force')
        self.assertTrue(remove_options.force)

    def test_fails_with_no_package_name(self):
        with self.assertRaises(SystemExit):
            do_test_parse(RemoveOptionsParser)
