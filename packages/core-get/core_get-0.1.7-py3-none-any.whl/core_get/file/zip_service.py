import zipfile
from pathlib import PurePath, Path
from typing import List


class ZipService:
    def make_zip_file(self, zip_path: PurePath, directory: PurePath, include: List[str]):
        path = Path(directory)
        all_files = [file.relative_to(directory) for pattern in include
                     for file in path.glob(pattern)]
        all_files.append(Path("Core.toml"))

        with zipfile.ZipFile(zip_path, 'w') as zip_file:
            for file in all_files:
                data = (path / file).read_bytes()
                zip_file.writestr(file.as_posix(), data)
