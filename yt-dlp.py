import json
from subprocess import run, CompletedProcess
import sys
from pathlib import Path


class YoutubeDL_interface:
    def __init__(self, youtube_dl_binary: Path) -> None:
        self.youtube_dl_binary = youtube_dl_binary

    def query(self, url: str):
        result = run([self.youtube_dl_binary, "-J", url], capture_output=True, text=True)
        self.get_format(result)

    def get_format(self, result: CompletedProcess[str]):
        info = json.loads(result.stdout)

        format_output = {
            "filesize": 0,
            "resolution": "",
            "format": "",
            "fps": "",
        }
        arrayFormat = []

        for fmt in info["formats"]:
            if fmt.get("ext") == "mhtml":
                continue

            filesize = fmt.get("filesize", 0)
            if filesize is None:
                filesize = 0
            filesize_mb = filesize / (1024 * 1024)  # Convert bytes to MB
            format_output["filesize"] = filesize_mb
            format_output["format"] = fmt.get("format", "Unknown")
            format_output["resolution"] = fmt.get("resolution", "Unknown")
            format_output["fps"] = fmt.get("fps", "Unknown")

            arrayFormat.append(format_output)
            print(
                f"Resulution : {format_output["resolution"]}, format : {format_output["format"]}, Size : {format_output["filesize"]:.2f} MB, FPS : {format_output["fps"]}"
            )

            """
            fmt important stuff : 
            - format
            - resolution
            - fps
            - filesize 
            """
