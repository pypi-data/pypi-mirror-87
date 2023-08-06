from unittest.case import TestCase
from unittest.mock import Mock

from core_get.configuration.serialization.toml_serializer import TomlSerializer


class TestTomlSerializer(TestCase):
    def test_parse_forwards_provided_data(self):
        mock_cls = Mock()
        mock_cls.from_dict = Mock(return_value=None)
        toml_reader_writer = TomlSerializer()
        toml_reader_writer.from_bytes(b'a = 5', mock_cls)
        mock_cls.from_dict.assert_called_with({'a': 5})

    def test_parse_returns_provided_instance(self):
        mock_inst = Mock()
        mock_cls = Mock()
        mock_cls.from_dict = Mock(return_value=mock_inst)
        toml_reader_writer = TomlSerializer()
        result_inst = toml_reader_writer.from_bytes(b'', mock_cls)
        self.assertEqual(mock_inst, result_inst)

    def test_print_uses_provided_data(self):
        mock_inst = Mock()
        mock_inst.to_dict = Mock(return_value={'a': 5})
        toml_reader_writer = TomlSerializer()
        result_data = toml_reader_writer.to_bytes(mock_inst)
        self.assertEqual(b'a = 5\n', result_data)
