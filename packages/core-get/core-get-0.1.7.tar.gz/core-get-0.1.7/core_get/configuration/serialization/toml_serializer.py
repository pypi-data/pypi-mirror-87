from typing import Type

import tomlkit

from core_get.configuration.serialization.configuration_serializer import ConfigurationSerializer


class TomlSerializer(ConfigurationSerializer):

    T = ConfigurationSerializer.T

    def from_bytes(self, data: bytes, cls: Type[T]) -> T:
        toml_str = data.decode('utf-8')
        toml_dict = tomlkit.loads(toml_str)
        t = cls.from_dict(toml_dict)
        return t

    def to_bytes(self, t: T) -> bytes:
        toml_dict = t.to_dict()
        toml_str = tomlkit.dumps(toml_dict)
        data = toml_str.encode('utf-8')
        return data
