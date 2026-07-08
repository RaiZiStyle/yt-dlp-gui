#!/usr/bin/env python3
# Local import
from PySide6.QtWidgets import QApplication
import sys
from pathlib import Path
from logging  import Logger, StreamHandler, Formatter, DEBUG, INFO, getLogger, FileHandler
import os

_logger_configured = False

def get_logger(name : str | None = None) -> Logger:
    global _logger_configured
    logger = getLogger(name)
    
    if not _logger_configured: 
        root_logger = getLogger()
        root_logger.setLevel(DEBUG)
        
        formatter = Formatter("%(asctime)s [%(levelname)s] [%(name)s:%(funcName)s:%(lineno)d] %(message)s",datefmt="%Y-%m-%d %H:%M:%S")
        # formatter = Formatter("%(asctime)s [%(levelname)s] ")
        
        # Handler console
        console_handler = StreamHandler()
        console_handler.setLevel(INFO)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)
        
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
        
    

if __name__ == "__main__":
    from gui import MainWindow
    app = QApplication(sys.argv)

    app.setStyle("Fusion")

    app.setStyleSheet("""
        QLineEdit {
            padding: 6px;
        }
        QGroupBox {
            font-weight: bold;
            margin-top: 16px;
            padding-top: 6px;
            border: 1px solid #aaaaaa;
            border-radius: 4px;
        }

        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top left;
            left: 10px;
            padding: 0 4px;
        }
        QPushButton {
            min-height: 32px;
        }

        QProgressBar {
            height: 22px;
        }

        """)

    window = MainWindow()
    window.show()

    print("Taille réelle :", window.size())  # taille en pixels logiques
    print("Scale factor :", app.devicePixelRatio())  # facteur de scaling

    sys.exit(app.exec())
