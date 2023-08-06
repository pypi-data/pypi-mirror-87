import json
from contextlib import ExitStack
from dataclasses import dataclass
from pathlib import PurePath
from typing import Dict, Any

import requests
from injector import inject
from requests import Response, HTTPError

from core_get.catalog.download_status_interface import DownloadStatusInterface
from core_get.options.common_options import CommonOptions


class NetworkException(Exception):
    pass


@inject
@dataclass
class NetworkService:
    download_status_interface: DownloadStatusInterface
    common_options: CommonOptions

    def get(self, url: str, params: Dict[str, str] = None, **kwargs) -> Any:
        self._check_offline()
        response = requests.get(url, params, **kwargs)
        return self._parse_json_response(response)

    def post(self, url: str, files: Dict[str, PurePath] = None, **kwargs) -> Any:
        self._check_offline()
        if self.common_options.dry_run:
            raise RuntimeError("POST with --dry-run flag")
        with ExitStack() as stack:
            file_streams = {key: stack.enter_context(open(file_name, 'rb'))
                            for key, file_name in files.items()} \
                if files is not None else None
            response = requests.post(url, files=file_streams, **kwargs)
            return self._parse_json_response(response)

    def delete(self, url: str, headers: Dict[str, str] = None, **kwargs) -> Any:
        self._check_offline()
        if self.common_options.dry_run:
            raise RuntimeError("DELETE with --dry-run flag")
        response = requests.delete(url, headers=headers, **kwargs)
        return self._parse_json_response(response)

    def download_file(self, url: str, destination_path: PurePath, headers: Dict[str, str] = None) -> None:
        self._check_offline()
        if self.common_options.dry_run:
            raise RuntimeError("Download file with --dry-run flag")
        with open(destination_path, 'wb') as destination_stream:
            with requests.get(url, headers=headers, stream=True) as response:
                response.raise_for_status()
                try:
                    total_length = int(response.headers.get('Content-Length', '0'))
                except ValueError:
                    total_length = 0
                self.download_status_interface.download_begin(destination_path.name)
                count = 0
                for chunk in response.iter_content(chunk_size=8192):
                    destination_stream.write(chunk)
                    count += len(chunk)
                    self.download_status_interface.download_progress(min(total_length, count), count)
                self.download_status_interface.download_done()

    def _check_offline(self):
        if self.common_options.offline:
            raise RuntimeError("Network accessed with --offline flag")

    def _parse_json_response(self, response: Response) -> Any:
        try:
            response.raise_for_status()
        except HTTPError:
            raise NetworkException
        content = response.content
        return json.loads(content)
