#!/usr/bin/env python3

import json
from subprocess import run, CompletedProcess
from pathlib import Path


class YoutubeDL_interface:
    FORMAT_FIELDS = {
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

    def __init__(self, youtube_dl_binary: Path) -> None:
        assert youtube_dl_binary.exists() is True
        self.youtube_dl_binary: Path = youtube_dl_binary

    def print_formats(self, formats: list[dict]):
        # Calcule la largeur max par colonne (contenu vs header)
        col_widths = {
            field: max(
                len(field),
                max(len(str(fmt.get(field, "N/A"))) for fmt in formats),
            )
            for field in self.FORMAT_FIELDS
        }
        idx_width = max(len(str(len(formats))), 2)

        # Header
        header = f"{'#':<{idx_width}}  " + "  ".join(
            f"{field:<{col_widths[field]}}" for field in self.FORMAT_FIELDS
        )
        print(header)
        print("-" * len(header))

        # Rows
        for i, fmt in enumerate(formats):
            row = f"{i:<{idx_width}}  " + "  ".join(
                f"{str(fmt.get(field, 'N/A')):<{col_widths[field]}}"
                for field in self.FORMAT_FIELDS
            )
            print(row)

    def query(
        self, url: str, query_type: str = "video"
    ):  # -> tuple[dict[Any, Any], list[Any]]:# -> tuple[dict[Any, Any], list[Any]]:

        results: CompletedProcess | None = None
        try:
            results = run(
                [self.youtube_dl_binary.resolve(), "-J", url],
                capture_output=True,
                text=True,
            )
            print("Query succed")
        except Exception as e:
            print(f"Error : {e}")

        assert results is not None

        formated_format = self.get_format(results)
        formated_videoMetadata = self.get_video_data(results)
        formated_format = self.extract(formated_format, query_type)
        return formated_videoMetadata, formated_format

    def get_video_data(self, result: CompletedProcess) -> dict:
        json_info = json.loads(result.stdout)
        formated_data_video = self.VIDEO_FIELD

        minutes, seconds = divmod(json_info.get("duration", 0), 60)

        formated_data_video["title"] = json_info.get("title", "N/A")
        formated_data_video["duration"] = f"{minutes:02}:{seconds:02}"
        formated_data_video["channel"] = json_info.get("channel", "N/A")
        formated_data_video["thumbnail"] = json_info.get("thumbnail", "N/A")

        return formated_data_video

    def get_format(self, result: CompletedProcess) -> list[dict]:
        info = json.loads(result.stdout)

        format_output = self.FORMAT_FIELDS

        arrayFormat = []

        for fmt in info["formats"]:
            if fmt.get("ext") == "mhtml":
                continue

            filesize = fmt.get("filesize", 0)
            if filesize is None:
                filesize = 0
            tmpfloat = float(filesize / (1024 * 1024))
            fmt["filesize"] = f"{tmpfloat:.4f} MB"  # Convert bytes to MB

            format_output = {
                field: fmt.get(field, "N/A") for field in self.FORMAT_FIELDS
            }

            arrayFormat.append(format_output)
            # print(
            #     f"Resulution : {format_output['resolution']}, format : {format_output['format']}, Size : {format_output['filesize']:.2f} MB, FPS : {format_output['fps']}"
            # )
        return arrayFormat

    def extract(self, results, query_type: str):

        match query_type:
            case "audio":
                results = [r for r in results if r["vcodec"] == "none"]
            case "video":
                results = [r for r in results if r["acodec"] == "none"]
                pass
            case _:
                print("ERROR")
                exit()
        print(f"{'#'*60}")
        self.print_formats(results)
        return results


YOUTUBE_DL_BINARY = Path("yt-dlp_linux")

assert YOUTUBE_DL_BINARY.exists() is True

if __name__ == "__main__":
    yt_dl = YoutubeDL_interface(YOUTUBE_DL_BINARY)
    yt_dl.query("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
