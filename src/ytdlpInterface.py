#!/usr/bin/env python3
# LOCAL IMPORTS
from utils import get_logger, format_size

from pathlib import Path
from enum import Enum
from typing import Callable, Optional, Any, cast


import yt_dlp
from yt_dlp.utils import DownloadError


class E_QUERY_TYPE(Enum):
    UNKNOWN = 0
    VIDEO = 1
    AUDIO = 2


class YoutubeDL_interface:
    FORMAT_FIELDS = {
        "format_id": "",
        "filesize": 0,
        "resolution": "N/A",
        "format": "N/A",
        "fps": "N/A",
        "audio_ext": "N/A",
        "video_ext": "N/A",
        "ext": "N/A",
        "acodec": "N/A",
        "vcodec": "N/A",
    }

    VIDEO_FIELD = {"title": "", "channel": "", "duration": 0, "thumbnail": ""}

    TIMEOUT = 5

    def __init__(self) -> None:
        # No binary needed anymore, just keep the common options
        self.formats: list[dict] = []
        self.videoMetadata: dict = {}
        self.url: str = ""
        self.query_type: E_QUERY_TYPE = E_QUERY_TYPE.UNKNOWN
        self.output: str = ""
        self._cancel_flag = None

        # optional callback wired up from the Qt side (e.g. for a QProgressBar)
        # expected signature: progress_callback(d: dict) -> None
        self.progress_callback: Optional[Callable[[dict], None]] = None

        self.logger = get_logger(__name__)

    def _base_opts(self) -> dict[str, object]:
        """Options shared by every YoutubeDL instance."""
        return {
            "socket_timeout": YoutubeDL_interface.TIMEOUT,
            "quiet": True,
            "no_warnings": True,
            "noplaylist": True,
        }

    def _internal_progress_hook(self, d: dict) -> None:
        """Internal hook passed to yt-dlp, relays to the Qt callback if set."""
        # d contains, among others: status, info_dict, filename, tmpfilename,
        # downloaded_bytes, total_bytes / total_bytes_estimate, speed, eta,
        # _percent_str, _speed_str, _eta_str (see yt-dlp progress_hooks docs)
        # Cancellation: raising from the hook stops yt-dlp cleanly
        # self.logger.info(f"Progress hook called with status: {d.get('status')}")
        # self.logger.info(f"State of cancel flag: {self._cancel_flag}")
        if self._cancel_flag and self._cancel_flag():
            self.logger.info("Download cancelled by user")
            raise Exception("Download cancelled by user")
        if self.progress_callback is not None:
            self.progress_callback(d)
        else:
            if d.get("status") == "downloading":
                pct = d.get("_percent_str", "N/A")
                speed = d.get("_speed_str", "N/A")
                self.logger.info(f"\rDownloading: {pct} at {speed}")
            elif d.get("status") == "finished":
                self.logger.info(f"\nDone: {d.get('filename')}")
            elif d.get("status") == "error":
                self.logger.error("\nError during download")

    def print_formats(self, formats: list[dict]) -> None:
        # Compute the max width per column (content vs header)
        col_widths = {
            field: max(
                len(field),
                max(len(str(fmt.get(field, "N/A"))) for fmt in formats),
            )
            for field in self.FORMAT_FIELDS
        }
        idx_width = max(len(str(len(formats))), 2)

        # Header
        # header = f"{'#':<{idx_width}}  " + "  ".join(f"{field:<{col_widths[field]}}" for field in self.FORMAT_FIELDS)
        # self.logger.info(header)
        # self.logger.info("-" * len(header))

        # Rows
        for i, fmt in enumerate(formats):
            row = f"{i:<{idx_width}}  " + "  ".join(f"{str(fmt.get(field, 'N/A')):<{col_widths[field]}}" for field in self.FORMAT_FIELDS)
            self.logger.info(row)

    def set_cancel_flag(self, flag_fn) -> None:
        """
        Pass a callable that returns True when cancellation is requested.
        Called on every progress tick, inside the worker thread — no Qt widgets.
        Example: interface.set_cancel_flag(lambda: self.worker._cancelled)
        """
        self.logger.info("Setting cancel flag callable")
        self._cancel_flag = flag_fn

    def query(self, url: str, query_type: str = "video") -> tuple[dict[Any, Any], list[Any]]:
        """
        Query the video or audio formats and metadata for the given URL and return them as a tuple (videoMetadata, formats).
        """
        self.url = url
        if query_type == "video":
            self.query_type = E_QUERY_TYPE.VIDEO
        elif query_type == "audio":
            self.query_type = E_QUERY_TYPE.AUDIO
        else:
            self.query_type = E_QUERY_TYPE.UNKNOWN

        info: Any | None = None
        try:
            ydl_opts = self._base_opts()
            with yt_dlp.YoutubeDL(cast(Any, ydl_opts)) as ydl:  # Trick for pylance to be happy with the type.
                self.logger.info(f"Query url : {url}")
                info = ydl.extract_info(url, download=False)
            self.logger.info("Query succeeded")
        except DownloadError as e:
            self.logger.error(f"DownloadError : {e}")
            raise e

        except Exception as e:
            self.logger.error(f"Other Error : {e}")
            raise e

        assert info is not None

        formated_format = self.get_format(info)
        formated_videoMetadata = self.get_video_data(info)
        formated_format = self.extract(formated_format, query_type)
        self.formats = formated_format
        self.videoMetadata = formated_videoMetadata
        return formated_videoMetadata, formated_format

    def download(self, url: str, format_id: str, output_folder: Path) -> None:
        """
        Download the video or audio in the specified format to the output folder.
        """
        index = next(
            (i for i, x in enumerate(self.formats) if x["format_id"] == format_id),
            None,
        )
        format_id_selected = None

        try:
            if index is not None:
                format_id_selected = self.formats[index].get("format_id", -999999)
            else:
                format_id_selected = -66666
        except IndexError:
            format_id_selected = None

        if format_id_selected is None:
            self.logger.warning("Warning : format not found")
            return

        ydl_opts = self._base_opts()
        ydl_opts["quiet"] = False
        ydl_opts["progress_hooks"] = [self._internal_progress_hook]
        # outtmpl expects a filename template, not just a folder
        # ydl_opts["outtmpl"] = str(output_folder.resolve() / "%(title)s.%(ext)s")
        ydl_opts["outtmpl"] = str(output_folder.resolve()) + ".%(ext)s"
        self.logger.info(f"outtmpl : {ydl_opts['outtmpl']}")

        if self.query_type is E_QUERY_TYPE.VIDEO:
            ydl_opts["format"] = f"{format_id_selected}+bestaudio"
            self.logger.info(f"VIDEO download, format : {ydl_opts['format']}")
        elif self.query_type is E_QUERY_TYPE.AUDIO:
            ydl_opts["format"] = f"{format_id_selected}"
            self.logger.info(f"AUDIO download, format : {ydl_opts['format']}")
        else:
            self.logger.error("Error : unknown query type")
            return

        try:
            with yt_dlp.YoutubeDL(cast(Any, ydl_opts)) as ydl:
                ydl.download([url])
        except DownloadError as e:
            self.logger.error(f"Error during download : {e}")

    def set_progress_callback(self, callback: Optional[Callable[[dict], None]]) -> None:
        """Call this from the Qt side to wire up a QProgressBar / Qt signal.

        Example on the Qt side (with a QObject emitting a signal):
            interface.set_progress_callback(self._on_progress)

            def _on_progress(self, d: dict):
                if d.get("status") == "downloading":
                    total = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
                    downloaded = d.get("downloaded_bytes", 0)
                    if total:
                        self.progressChanged.emit(int(downloaded * 100 / total))
        """
        self.progress_callback = callback

    def get_video_data(self, info: dict) -> dict:
        """
        Extracts and formats the video metadata from the info dict.
        Field from : VIDEO_FIELD
        """
        formated_data_video = dict(self.VIDEO_FIELD)

        minutes, seconds = divmod(info.get("duration", 0) or 0, 60)

        formated_data_video["title"] = info.get("title", "N/A")
        formated_data_video["duration"] = f"{minutes:02}:{seconds:02}"
        formated_data_video["channel"] = info.get("channel", "N/A")
        formated_data_video["thumbnail"] = info.get("thumbnail", "N/A")

        return formated_data_video

    def get_format(self, info: dict) -> list[dict]:
        """
        Extracts and formats the available formats from the info dict.
        """
        arrayFormat = []

        for fmt in info.get("formats", []):
            if fmt.get("ext") == "mhtml":
                continue

            filesize = fmt.get("filesize", 0)
            filesizeFormated = format_size(filesize) if filesize is not None else "N/A"
            self.logger.debug(f"filesize before: {filesize}, after : {filesizeFormated}\n\n")
            fmt["filesize"] = f"{filesizeFormated}"

            format_output = {field: fmt.get(field, "N/A") for field in self.FORMAT_FIELDS}

            arrayFormat.append(format_output)
        return arrayFormat

    def extract(self, results, query_type: str):
        """
        Extract formats based on the query type (audio or video).
        """
        match query_type:
            case "audio":
                results = [r for r in results if r["vcodec"] == "none"]
            case "video":
                results = [r for r in results if r["acodec"] == "none"]
            case _:
                self.logger.error("ERROR")
                exit()
        self.logger.info(f"{'#'*60}")
        self.print_formats(results)
        return results


if __name__ == "__main__":
    yt_dl = YoutubeDL_interface()
    yt_dl.query("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

    from pprint import pprint

    pprint(yt_dl.formats)
