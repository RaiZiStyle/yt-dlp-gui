# Local import
from ytdlpInterface import YoutubeDL_interface

from pathlib import Path
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFileDialog,
    QButtonGroup,
    QComboBox,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QProgressBar,
    QRadioButton,
    QVBoxLayout,
    QWidget,
)



class MainWindow(QMainWindow):
    def __init__(self, youtube_dl_binary: Path):
        super().__init__()
        self.ytDL_interface = YoutubeDL_interface(youtube_dl_binary)
        
        

        self.setWindowTitle("yt-dlp GUI")
        self.resize(800, 650)
        self.setFixedSize(800, 650)  # ← bloque toute tentative de resize

        central = QWidget()
        central.setMinimumSize(780, 620)  # ← sur le widget central
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)
        main_layout.setSpacing(10)
        main_layout.setSizeConstraint(QVBoxLayout.SizeConstraint.SetMinimumSize)  # ← ajoute ça


        # ==================================================
        # URL
        # ==================================================

        url_group = QGroupBox("URL")
        url_layout = QHBoxLayout()

        self.url_edit = QLineEdit()
        self.url_edit.setPlaceholderText("https://www.youtube.com/watch?v=...")

        self.load_button = QPushButton("Charger")

        url_layout.addWidget(self.url_edit)
        url_layout.addWidget(self.load_button)

        url_group.setLayout(url_layout)

        # ==================================================
        # Video info
        # ==================================================

        info_group = QGroupBox("Informations")
        info_layout = QHBoxLayout()

        self.thumbnail_label = QLabel()

        self.thumbnail_label.setFixedSize(200, 120)
        self.thumbnail_label.setFrameShape(QFrame.Box)
        self.thumbnail_label.setAlignment(Qt.AlignCenter)
        self.thumbnail_label.setText("Miniature")

        info_text_layout = QVBoxLayout()

        self.title_label = QLabel("Titre de la vidéo")
        self.channel_label = QLabel("Chaîne Youtube")
        self.duration_label = QLabel("Durée : --:--")

        self.title_label.setWordWrap(True)

        info_text_layout.addWidget(self.title_label)
        info_text_layout.addWidget(self.channel_label)
        info_text_layout.addWidget(self.duration_label)
        info_text_layout.addStretch()

        info_layout.addWidget(self.thumbnail_label)
        info_layout.addLayout(info_text_layout)

        info_group.setLayout(info_layout)

        # ==================================================
        # Download options
        # ==================================================

        options_group = QGroupBox("Options")
        options_layout = QVBoxLayout()

        #
        # Type
        #

        type_label = QLabel("Type")

        self.video_radio = QRadioButton("Vidéo")
        self.audio_radio = QRadioButton("Audio")

        self.video_radio.setChecked(True)

        radio_group = QButtonGroup(self)
        radio_group.addButton(self.video_radio)
        radio_group.addButton(self.audio_radio)

        #
        # Quality
        #

        quality_label = QLabel("Qualité")

        self.quality_combo = QComboBox()

        #
        # Destination
        #

        destination_label = QLabel("Dossier")

        destination_layout = QHBoxLayout()

        self.destination_edit = QLineEdit()

        self.browse_button = QPushButton("Parcourir")

        destination_layout.addWidget(self.destination_edit)
        destination_layout.addWidget(self.browse_button)

        options_layout.addWidget(type_label)
        options_layout.addWidget(self.video_radio)
        options_layout.addWidget(self.audio_radio)

        options_layout.addSpacing(10)

        options_layout.addWidget(quality_label)
        options_layout.addWidget(self.quality_combo)

        options_layout.addSpacing(10)

        options_layout.addWidget(destination_label)
        options_layout.addLayout(destination_layout)

        options_group.setLayout(options_layout)

        # ==================================================
        # Progress
        # ==================================================

        progress_group = QGroupBox("Téléchargement")
        progress_layout = QVBoxLayout()

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(62)

        self.speed_label = QLabel("Téléchargement : TODO MB/s")
        self.eta_label = QLabel("Temps restant : TODO")

        progress_layout.addWidget(self.progress_bar)
        progress_layout.addWidget(self.speed_label)
        progress_layout.addWidget(self.eta_label)

        progress_group.setLayout(progress_layout)

        # ==================================================
        # Download button
        # ==================================================

        button_layout = QHBoxLayout()

        button_layout.addStretch()

        self.download_button = QPushButton("Télécharger")
        self.download_button.setMinimumWidth(180)

        button_layout.addWidget(self.download_button)

        # ==================================================
        # Main Layout
        # ==================================================

        main_layout.addWidget(url_group)
        main_layout.addWidget(info_group)
        main_layout.addWidget(options_group)
        main_layout.addWidget(progress_group)
        main_layout.addLayout(button_layout)

        # ==================================================
        # Signals
        # ==================================================

        self.browse_button.clicked.connect(self.select_download_directory)

        self.audio_radio.toggled.connect(self.update_quality_list)
        
        # self.load_button.clicked.connect()
        

    def select_download_directory(self):
        directory = QFileDialog.getExistingDirectory(
            self,
            "Choisir un dossier",
        )

        if directory:
            self.destination_edit.setText(directory)

    def update_quality_list(self):

        self.quality_combo.clear()



