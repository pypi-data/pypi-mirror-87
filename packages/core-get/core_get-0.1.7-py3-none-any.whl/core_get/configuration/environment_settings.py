from dataclasses import dataclass
from pathlib import PurePath
from typing import Optional


@dataclass(frozen=True)
class EnvironmentSettings:
    working_dir: PurePath
    project_dir: Optional[PurePath]
    app_dir: PurePath
    cache_dir: PurePath
    catalog_url: str
