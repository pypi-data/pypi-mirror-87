from pathlib import PurePath
from unittest import TestCase
from unittest.mock import Mock

from core_get.vendor.diamond.diamond_project_discoverer import DiamondProjectDiscoverer


class TestDiamondProjectDiscover(TestCase):

    def test_discovers_no_projects_successfully(self):
        file_system = Mock()
        file_system.glob = Mock(return_value=[])
        diamond_project_reader = Mock()
        diamond_project_discover = DiamondProjectDiscoverer(diamond_project_reader, file_system)
        discovered_projects = diamond_project_discover.discover(PurePath('.'))
        self.assertEqual([], discovered_projects)

    def test_discovers_one_project_successfully(self):
        file_system = Mock()
        file_system.glob = Mock(return_value=[PurePath('test.ldf')])
        diamond_project = Mock()
        diamond_project_reader = Mock()
        diamond_project_reader.read = Mock(return_value=diamond_project)
        diamond_project_discover = DiamondProjectDiscoverer(diamond_project_reader, file_system)
        discovered_projects = diamond_project_discover.discover(PurePath('.'))
        self.assertEqual([diamond_project], discovered_projects)

    def test_discover_forwards_file(self):
        file_system = Mock()
        file_system.glob = Mock(return_value=[PurePath('test.ldf')])
        diamond_project = Mock()
        diamond_project_reader = Mock()
        diamond_project_reader.read = Mock(return_value=diamond_project)
        diamond_project_discover = DiamondProjectDiscoverer(diamond_project_reader, file_system)
        diamond_project_discover.discover(PurePath('.'))
        diamond_project_reader.read.assert_called_with(PurePath('test.ldf'))

    def test_discover_queries_given_folder_and_correct_pattern(self):
        file_system = Mock()
        file_system.glob = Mock(return_value=[])
        diamond_project_reader = Mock()
        diamond_project_discover = DiamondProjectDiscoverer(diamond_project_reader, file_system)
        diamond_project_discover.discover(PurePath('my_path'))
        file_system.glob.assert_called_with(PurePath('my_path'), '*.ldf')
