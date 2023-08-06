from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from core_get.options.options import Options


@dataclass
class CommonOptions(Options):
    dry_run: bool
    offline: bool
    project_dir: Optional[Path]
    working_dir: Optional[Path]
