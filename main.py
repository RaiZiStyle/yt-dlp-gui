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


