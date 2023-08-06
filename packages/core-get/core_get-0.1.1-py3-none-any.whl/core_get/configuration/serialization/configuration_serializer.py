from typing import TypeVar, Type

from core_get.configuration.configuration import Configuration


class ConfigurationSerializer:

    T = TypeVar('T', bound=Configuration)

    def from_bytes(self, data: bytes, cls: Type[T]) -> T:
        raise NotImplementedError

    def to_bytes(self, t: T) -> bytes:
        raise NotImplementedError
