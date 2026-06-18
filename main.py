#!/usr/bin/env python3

import json
import subprocess
import sys

YOUTUBE_DL_BINARY = "./yt-dlp_linux"


try:
    url = sys.argv[1]
except IndexError:
    url = "https://www.youtube.com/watch?v=dCzo86OgxEg"


result = subprocess.run([YOUTUBE_DL_BINARY, "-J", url], capture_output=True, text=True)

info = json.loads(result.stdout)

for fmt in info["formats"]:
    if fmt.get("ext") == "mhtml":
        continue

    resolution = fmt.get("resolution", "Unknown")
    fps = fmt.get("fps", "Unknown")
    filesize = fmt.get("filesize", 0)
    if filesize is None:
        filesize = 0
    filesize_mb = filesize / (1024 * 1024)  # Convert bytes to MB
    format = fmt.get("format", "Unknown")
    print(f"Resulution : {resolution}, format : {format}, Size : {filesize_mb:.2f} MB, FPS : {fps}")

    """
    fmt important stuff : 
    - format
    - resolution
    - fps
    - filesize 
    """
