from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from re import sub
from pathlib import Path
from logging import Logger, StreamHandler, Formatter, DEBUG, INFO, getLogger, FileHandler
import os
import sys

_logger_configured = False


def get_logger(name: str | None = None) -> Logger:
    global _logger_configured
    logger = getLogger(name)

    if not _logger_configured:
        root_logger = getLogger()
        root_logger.setLevel(DEBUG)

        formatter = Formatter("%(asctime)s [%(levelname)s] [%(name)s:%(funcName)s:%(lineno)d] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        # formatter = Formatter("%(asctime)s [%(levelname)s] ")

        # Handler console
        # console_handler = StreamHandler()
        # console_handler.setLevel(INFO)
        # console_handler.setFormatter(formatter)
        # root_logger.addHandler(console_handler)

        # Handler file
        log_path = os.path.join(os.path.dirname(__file__), "yt-dlp-gui.log")
        file_handler = FileHandler(log_path, mode="a", encoding="utf-8")
        file_handler.setLevel(DEBUG)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

        _logger_configured = True
        root_logger.debug("test")
        root_logger.info(f"Logger configured. Log file: {log_path}")

    return logger


logger = get_logger(__name__)


def format_size(octets: int) -> str:
    units = ["o", "Ko", "Mo", "Go", "To", "Po", "Eo"]
    size = float(octets)

    for unit in units[:-1]:
        if abs(size) < 1024:
            formatted = f"{size:.2f}".rstrip("0").rstrip(".")
            return f"{formatted} {unit}"
        size /= 1024

    formatted = f"{size:.2f}".rstrip("0").rstrip(".")
    return f"{formatted} {units[-1]}"


def clean_url(url, keep_params=("v",)):
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    filtered = {k: v[0] for k, v in query.items() if k in keep_params}
    new_query = urlencode(filtered)
    return urlunparse(parsed._replace(query=new_query))


def _strip_ansi(text: str) -> str:
    """Remove ANSI terminal escape sequences from a string."""
    return sub(r"\x1b\[[0-9;]*m", "", text)


def get_asset(filename: str) -> Path:
    """Résout le chemin vers assets/ que ce soit en dev ou dans le bundle PyInstaller."""
    logger.debug(f"Getting asset path for: {filename}")
    if getattr(sys, "frozen", False):
        base = Path(sys._MEIPASS)  # type: ignore[attr-defined]
    else:
        base = Path(__file__).parent.parent
    return base / "assets" / filename
