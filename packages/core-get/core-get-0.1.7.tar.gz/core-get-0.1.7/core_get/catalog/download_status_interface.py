class DownloadStatusInterface:
    def download_begin(self, filename: str) -> None:
        raise NotImplementedError

    def download_progress(self, downloaded: int, size: int) -> None:
        raise NotImplementedError

    def download_done(self) -> None:
        raise NotImplementedError
