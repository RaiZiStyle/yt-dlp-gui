# Local import
from ytdlpInterface import YoutubeDL_interface
from worker import Worker

from pathlib import Path
from PySide6.QtCore import Qt, QThread
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
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode
from PySide6.QtGui import QPixmap
import requests

URL_THAT_FAILED = "https://www.youtube.com/watch?v=xpFL0hvqZLw&list=PL_cpYW68sLfhG6YXPalPJw-lSaKsdE10-&index=56"

DEFAULT_URL = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
DEFAULT_URL = URL_THAT_FAILED

class MainWindow(QMainWindow):
    TITLE_PREFIX = "Titre de la vidéo : "
    CHANNEL_PREFIX = "Chaîne Youtube : "
    DURATION_PREFIX = "Durée : "
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
        main_layout.setSizeConstraint(
            QVBoxLayout.SizeConstraint.SetMinimumSize
        )  # ← ajoute ça

        # ==================================================
        # URL
        # ==================================================

        url_group = QGroupBox("URL")
        url_layout = QHBoxLayout()

        self.url_edit = QLineEdit()
        # self.url_edit.setPlaceholderText("https://www.youtube.com/watch?v=...")
        self.url_edit.setText(DEFAULT_URL)

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

        self.title_label = QLabel(MainWindow.TITLE_PREFIX)
        self.channel_label = QLabel(MainWindow.CHANNEL_PREFIX)
        self.duration_label = QLabel(MainWindow.DURATION_PREFIX)

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

        self.destination_layout = QHBoxLayout()

        self.destination_edit = QLineEdit(str(Path("").resolve()))

        self.browse_button = QPushButton("Parcourir")

        self.destination_layout.addWidget(self.destination_edit)
        self.destination_layout.addWidget(self.browse_button)

        options_layout.addWidget(type_label)
        options_layout.addWidget(self.video_radio)
        options_layout.addWidget(self.audio_radio)

        options_layout.addSpacing(10)

        options_layout.addWidget(quality_label)
        options_layout.addWidget(self.quality_combo)

        options_layout.addSpacing(10)

        options_layout.addWidget(destination_label)
        options_layout.addLayout(self.destination_layout)

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
        self.load_button.clicked.connect(self.on_load)
        self.download_button.clicked.connect(self.on_download)


    def on_download(self):
        """
        Launch the download thread for `YoutubeDL_interface`. 
        """
        format_id = self.quality_combo.currentData()
        self.ytDL_interface.url
        output_folder = self.destination_edit.text()
        pathOutput_folder = Path(output_folder)
        if pathOutput_folder.exists() is True:
            print(f"ERROR : output exists {pathOutput_folder.resolve}")
            exit()
        
        # Launch the thread
        self.downloadThread = QThread()

        self.worker = Worker(
            self.ytDL_interface.download,
            self.ytDL_interface.url,
            format_id,
            pathOutput_folder,
        )

        self.worker.moveToThread(self.downloadThread)


        self.downloadThread.started.connect(self.worker.run)
        # self.worker.result.connect(self.on_download_finished)
        # self.worker.error.connect(self.on_download_error)

        self.worker.finished.connect(self.downloadThread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.downloadThread.finished.connect(self.downloadThread.deleteLater)

        self.downloadThread.start()

    def on_load(self):
        """
        Launch the query thread for `YoutubeDL_interface`. 
        """
        url = self.url_edit.text().strip()
        url = clean_url(url)
        self.url_edit.setText(str(url))
        if not url:
            print("ERROR, NO URL GIVEN")
            return

        query_type = "audio" if self.audio_radio.isChecked() else "video"

        # Launch the thread
        self.downloadThread = QThread()

        self.worker = Worker(
            self.ytDL_interface.query,
            url,
            query_type,
        )

        self.worker.moveToThread(self.downloadThread)

        self.downloadThread.started.connect(self.worker.run)

        self.worker.result.connect(self.on_query_finished)
        self.worker.error.connect(self.on_query_error)

        self.worker.finished.connect(self.downloadThread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.downloadThread.finished.connect(self.downloadThread.deleteLater)

        self.downloadThread.start()

    def on_query_finished(self, result):
        """
        Slot for when the thread of query is finish
        """
        self.videoMetadata, self.formats = result

        self.title_label.setText(
            MainWindow.TITLE_PREFIX + self.videoMetadata.get("title", "N/A")
        )
        self.channel_label.setText(
            MainWindow.CHANNEL_PREFIX + self.videoMetadata.get("channel", "N/A")
        )
        self.duration_label.setText(
            MainWindow.DURATION_PREFIX + str(self.videoMetadata.get("duration", 0))
        )

        # Update thumbnail
        thumbnail_url = self.videoMetadata.get("thumbnail", "")
        if thumbnail_url:
            response = requests.get(thumbnail_url)
            pixmap = QPixmap()
            pixmap.loadFromData(response.content)

            # Redimensionner pour tenir dans le label sans déformer
            pixmap = pixmap.scaled(
                200,
                120,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )

            self.thumbnail_label.setText("")  # Supprimer le texte "Miniature"
            self.thumbnail_label.setPixmap(pixmap)
        # Peuple la combo
        self.update_quality_list()
    
    def on_query_error(self, e):
        """
        Slot for when the thread of query is finish with an error
        """        
        print(e)
        exit()
        
    def update_quality_list(self):
        """
        Updated the `self.quality_combo` based on `self.formats`
        """        
        self.quality_combo.clear()

        if not hasattr(self, "formats") or not self.formats:
            return

        for i, fmt in enumerate(self.formats):
            resolution = fmt.get("resolution", "N/A")
            ext = fmt.get("ext", "N/A")
            filesize = fmt.get("filesize", "N/A")
            fps = fmt.get("fps", "N/A")
            label = f"{resolution} — {ext} ({filesize}) - FPS : {fps}"
            self.quality_combo.addItem(
                label, userData=fmt["format_id"]
            )  # userData = index dans self.formats


    def select_download_directory(self):
        """
        Slot for the `self.browse_button`
        """              
        directory = QFileDialog.getExistingDirectory(
            self,
            "Choisir un dossier",
        )

        if directory:
            self.destination_edit.setText(directory)



def clean_url(url, keep_params=("v",)):
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    filtered = {k: v[0] for k, v in query.items() if k in keep_params}
    new_query = urlencode(filtered)
    return urlunparse(parsed._replace(query=new_query))