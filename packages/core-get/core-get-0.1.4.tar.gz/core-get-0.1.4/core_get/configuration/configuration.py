from __future__ import annotations
from typing import Dict


class Configuration:
    @classmethod
    def from_dict(cls, d) -> Configuration:
        raise NotImplementedError

    def to_dict(self) -> Dict:
        raise NotImplementedError
