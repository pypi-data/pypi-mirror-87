import json
from typing import Type

from core_get.configuration.serialization.configuration_serializer import ConfigurationSerializer


class JsonSerializer(ConfigurationSerializer):

    T = ConfigurationSerializer.T

    def from_bytes(self, data: bytes, cls: Type[T]) -> T:
        json_str = data.decode('utf-8')
        json_dict = json.loads(json_str)
        t = cls.from_dict(json_dict)
        return t

    def to_bytes(self, t: T) -> bytes:
        json_dict = t.to_dict()
        json_str = json.dumps(json_dict)
        data = json_str.encode('utf-8')
        return data
