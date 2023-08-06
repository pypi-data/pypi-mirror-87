from unittest.case import TestCase
from unittest.mock import Mock

from core_get.configuration.serialization.json_serializer import JsonSerializer


class TestJsonSerializer(TestCase):
    def test_parse_forwards_provided_data(self):
        mock_cls = Mock()
        mock_cls.from_dict = Mock(return_value=None)
        json_reader_writer = JsonSerializer()
        json_reader_writer.from_bytes(b'["hej", 5]', mock_cls)
        mock_cls.from_dict.assert_called_with(['hej', 5])

    def test_parse_returns_provided_instance(self):
        mock_inst = Mock()
        mock_cls = Mock()
        mock_cls.from_dict = Mock(return_value=mock_inst)
        json_reader_writer = JsonSerializer()
        result_inst = json_reader_writer.from_bytes(b'null', mock_cls)
        self.assertEqual(mock_inst, result_inst)

    def test_print_uses_provided_data(self):
        mock_inst = Mock()
        mock_inst.to_dict = Mock(return_value=['hej', 5])
        json_reader_writer = JsonSerializer()
        result_data = json_reader_writer.to_bytes(mock_inst)
        self.assertEqual(b'["hej", 5]', result_data)
