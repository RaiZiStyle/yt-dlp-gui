# about_dialog.py
from version import __version__
from utils import get_asset

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import QUrl
from PySide6.QtGui import QIcon, QPixmap


class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("À propos")
        self.setFixedWidth(420)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)

        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(20, 20, 20, 20)

        # --- Header : icône + nom + version ---
        header = QHBoxLayout()
        header.setSpacing(14)
        
        pixmap = QPixmap()
        pixmap.loadFromData(get_asset("icon.png").open("rb").read())

        # Redimensionner pour tenir dans le label sans déformer
        pixmap = pixmap.scaled(
            64,
            64,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        icon_label = QLabel()
        icon_label.setPixmap(pixmap)


        title_layout = QVBoxLayout()
        title_layout.setSpacing(2)
        app_name = QLabel("yt-dlp GUI")
        app_name.setStyleSheet("font-size: 17px; font-weight: bold;")
        version_label = QLabel(f"version {__version__}  ·  Licence : The Unlicense")
        version_label.setStyleSheet("font-size: 12px; color: gray;")
        title_layout.addWidget(app_name)
        title_layout.addWidget(version_label)

        header.addWidget(icon_label)
        header.addLayout(title_layout)
        header.addStretch()
        layout.addLayout(header)

        layout.addSpacing(16)
        layout.addWidget(self._separator())
        layout.addSpacing(12)

        # --- Auteur ---
        author_layout = QHBoxLayout()
        author_layout.setSpacing(12)

        avatar = QLabel("AGP")
        avatar.setFixedSize(48, 48)
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avatar.setStyleSheet("""
            background: #e6f1fb; border-radius: 18px;
            font-size: 12px; font-weight: bold; color: #185fa5;
        """)

        author_text = QVBoxLayout()
        author_text.setSpacing(1)
        name_label = QLabel("Arthur Guyot-Premel")
        name_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        pseudo_label = QLabel("RaiZiStyle")
        pseudo_label.setStyleSheet("font-size: 12px; color: gray;")
        author_text.addWidget(name_label)
        author_text.addWidget(pseudo_label)

        author_layout.addWidget(avatar)
        author_layout.addLayout(author_text)
        author_layout.addStretch()
        layout.addLayout(author_layout)

        layout.addSpacing(14)

        # --- Liens ---
        links = [
            ("✉", "E-mail",   "mailto:arthur.guyotpremel@gmail.com"),
            ("⌥", "GitHub",   "https://github.com/RaiZiStyle"),
            ("in", "LinkedIn", "https://www.linkedin.com/in/arthur-guyot-74a296159/"),
        ]
        for icon, label, url in links:
            row = QHBoxLayout()
            ico = QLabel(icon)
            ico.setFixedWidth(20)
            ico.setStyleSheet("color: gray; font-size: 13px;")
            lbl = QLabel(label)
            lbl.setFixedWidth(70)
            lbl.setStyleSheet("color: gray; font-size: 13px;")
            link = QLabel(f'<a href="{url}" style="color: #185fa5;">{url.replace("mailto:","")}</a>')
            link.setOpenExternalLinks(True)
            link.setStyleSheet("font-size: 13px;")
            row.addWidget(ico)
            row.addWidget(lbl)
            row.addWidget(link)
            layout.addLayout(row)
            layout.addSpacing(4)

        layout.addSpacing(12)
        layout.addWidget(self._separator())
        layout.addSpacing(12)

        # --- Footer : source + licence ---
        footer = QHBoxLayout()

        src_btn = QPushButton("Code source")
        src_btn.setStyleSheet("font-size: 12px;")
        src_btn.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl("https://github.com/RaiZiStyle/yt-dlp-gui"))
        )

        lic_btn = QPushButton("The Unlicense")
        lic_btn.setStyleSheet("font-size: 12px;")
        lic_btn.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl("https://unlicense.org"))
        )

        close_btn = QPushButton("Fermer")
        close_btn.clicked.connect(self.accept)

        footer.addWidget(src_btn)
        footer.addWidget(lic_btn)
        footer.addStretch()
        footer.addWidget(close_btn)
        layout.addLayout(footer)

    def _separator(self):
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("color: #e0e0e0;")
        return line