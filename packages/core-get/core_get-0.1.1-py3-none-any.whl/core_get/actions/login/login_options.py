from dataclasses import dataclass

from core_get.options.options import Options


@dataclass
class LoginOptions(Options):
    access_token: str
