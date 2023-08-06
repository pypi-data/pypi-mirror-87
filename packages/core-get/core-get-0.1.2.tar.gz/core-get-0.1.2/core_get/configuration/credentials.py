from __future__ import annotations

from dataclasses import dataclass

from core_get.configuration.configuration import Configuration


@dataclass
class Credentials(Configuration):
    access_token: str

    @classmethod
    def from_dict(cls, d) -> Credentials:
        return Credentials(d['access_token'])

    def to_dict(self) -> dict:
        return {'access_token': self.access_token}
