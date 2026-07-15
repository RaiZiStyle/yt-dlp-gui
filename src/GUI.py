# LOCAL IMPORTS
from about import AboutDialog
from ytdlpInterface import YoutubeDL_interface
from worker import Worker
from utils import get_logger, _strip_ansi, clean_url, get_asset
from helperGUI import HelpDialog
from version import __version__

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
    QMessageBox,
)
from PySide6.QtGui import QIcon
from PySide6.QtGui import QPixmap
import requests


from yt_dlp.utils import DownloadError

URL_THAT_FAILED = "https://www.youtube.com/watch?v=9J62hGda9BQ&list=RD9J62hGda9BQ&start_radio=1"

DEFAULT_URL = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
# DEFAULT_URL = URL_THAT_FAILED


class MainWindow(QMainWindow):
    TITLE_PREFIX = "Titre de la vidéo : "
    CHANNEL_PREFIX = "Chaîne Youtube : "
    DURATION_PREFIX = "Durée : "
    DESTIATION_PREFIX = str(Path.home() / "Downloads")

    HEIGH_SIZE = 800
    WIDTH_SIZE = 680
    MAX_SIZE_OFFSET = 200

    DEFAULT_DELAY_STATUSBAR = 5000  # ms
    GITHUB_REPO = "RaiZiStyle/yt-dlp-gui"  # 

    def __init__(self):

        super().__init__()
        self.logger = get_logger(MainWindow.__name__)
        self.ytDL_interface = YoutubeDL_interface()

        self.setWindowIcon(QIcon(str(get_asset("icon.png"))))

        self.statusBar()  # active la barre

        self.setWindowTitle(f"yt-dlp GUI v{__version__}")
        self.resize(MainWindow.WIDTH_SIZE, MainWindow.HEIGH_SIZE)
        self.setMinimumSize(MainWindow.WIDTH_SIZE, MainWindow.HEIGH_SIZE)  # ← bloque toute tentative de resize
        self.setMaximumSize(MainWindow.WIDTH_SIZE + self.MAX_SIZE_OFFSET, MainWindow.HEIGH_SIZE + self.MAX_SIZE_OFFSET)  # ← bloque toute tentative de resize

        central = QWidget()
        # central.setMinimumSize(780, 620)  # ← sur le widget central
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)
        main_layout.setSpacing(10)

        # ==================================================
        # Toolbar
        # ==================================================
        toolbar = self.addToolBar("Aide")
        toolbar.setMovable(False)
        help_action = toolbar.addAction("Aide")
        help_action.setToolTip("Aide")
        help_action.triggered.connect(self.on_help)

        # ==================================================
        # About
        # ==================================================
        about_action = toolbar.addAction("À propos")
        about_action.triggered.connect(self.on_about)

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
        self.thumbnail_label.setFrameShape(QFrame.Box)  # type: ignore
        self.thumbnail_label.setAlignment(Qt.AlignCenter)  # type: ignore
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

        # ==================================================
        # Type
        # ==================================================
        type_label = QLabel("Type")

        self.video_radio = QRadioButton("Vidéo")
        self.audio_radio = QRadioButton("Audio")

        self.video_radio.setChecked(True)

        radio_group = QButtonGroup(self)
        radio_group.addButton(self.video_radio)
        radio_group.addButton(self.audio_radio)

        # ==================================================
        # Quality
        # ==================================================
        quality_label = QLabel("Qualité")

        self.quality_combo = QComboBox()

        # ==================================================
        # Destination
        # ==================================================
        destination_label = QLabel("Dossier")
        self.destination_layout = QHBoxLayout()
        self.destination_edit = QLineEdit(self.DESTIATION_PREFIX)
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
        # self.progress_bar.setValue(62)

        self.speed_label = QLabel("Téléchargement : MB/s")
        self.eta_label = QLabel("Temps restant : s")

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
        # Cancel button
        # ==================================================
        self.cancel_button = QPushButton("Annuler")
        self.cancel_button.setEnabled(False)
        button_layout.addWidget(self.cancel_button)

        # ==================================================
        # Main Layout
        # ==================================================
        main_layout.addWidget(url_group)
        main_layout.addWidget(info_group)
        main_layout.addWidget(options_group)
        main_layout.addWidget(progress_group)
        main_layout.addLayout(button_layout)
        
        
        self.check_for_update()

        # ==================================================
        # Signals
        # ==================================================
        self.browse_button.clicked.connect(self.select_download_directory)
        self.audio_radio.toggled.connect(self.update_quality_list)
        self.load_button.clicked.connect(self.on_load)
        self.download_button.clicked.connect(self.on_download)
        self.cancel_button.clicked.connect(self.on_cancel)

    def on_help(self):
        dialog = HelpDialog(self)
        dialog.exec()

    def on_about(self):
        AboutDialog(self).exec()

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
            self.quality_combo.addItem(label, userData=fmt["format_id"])  # userData = index dans self.formats

    def resetInfo(self, isLoading: bool, isDownloading: bool):
        if isLoading:
            self.title_label.setText(MainWindow.TITLE_PREFIX)
            self.channel_label.setText(MainWindow.CHANNEL_PREFIX)
            self.duration_label.setText(MainWindow.DURATION_PREFIX)
            self.formats = []
            self.update_quality_list()
            self.thumbnail_label.setText("Miniature")
        if isDownloading:
            self.progress_bar.setValue(0)
            self.speed_label.setText("Téléchargement : --")  # ← neutre, pas "erreur"
            self.eta_label.setText("Temps restant : --")  # ← remet à zéro

    def resizeEvent(self, event):
        new_size = event.size()
        # TODO: REMOVE CAUSE IT'S SPAMMY
        self.logger.debug(f"New size : {new_size.width()} x {new_size.height()}")

        super().resizeEvent(event)  # important

    def on_load(self):
        """
        Launch the query thread for `YoutubeDL_interface`.
        """
        self.statusBar().showMessage("Chargement des informations de la vidéo...", 10000)
        url = self.url_edit.text().strip()
        url = clean_url(url)
        self.url_edit.setText(str(url))
        if not url:
            self.logger.error("ERROR, NO URL GIVEN")
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
        self.statusBar().showMessage("Informations de la vidéo chargées.", self.DEFAULT_DELAY_STATUSBAR)
        self.videoMetadata, self.formats = result

        self.title_label.setText(MainWindow.TITLE_PREFIX + self.videoMetadata.get("title", "N/A"))
        self.channel_label.setText(MainWindow.CHANNEL_PREFIX + self.videoMetadata.get("channel", "N/A"))
        self.duration_label.setText(MainWindow.DURATION_PREFIX + str(self.videoMetadata.get("duration", 0)))

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
        self.destination_edit.setText(str(Path(self.DESTIATION_PREFIX) / self.videoMetadata.get("title", "N/A")))

    def on_query_error(self, e: DownloadError):
        """
        Slot for when the thread of query is finish with an error| Exception
        """
        assert e.msg is not None
        errorMsg = _strip_ansi(e.msg).split(":")[-1].strip()
        self.statusBar().showMessage(f"Erreur  : {errorMsg}", 10000)
        self.resetInfo(isLoading=True, isDownloading=False)

        self.logger.error(errorMsg)

    def on_download(self):
        """
        Launch the download thread for `YoutubeDL_interface`.
        """
        format_id = self.quality_combo.currentData()
        self.ytDL_interface.url
        output_file = self.destination_edit.text()
        output_dir = Path(output_file).parent

        if output_file == "":
            self.logger.error(f"ERROR : output is empty")
            self.statusBar().showMessage(f"Erreur : le chemin de sortie est vide", 10000)
            exit()
        pathOutput_file = Path(output_file)
        if pathOutput_file.is_dir() is True:
            self.logger.error(f"ERROR : output is a directory {pathOutput_file.resolve()}")
            self.statusBar().showMessage(f"Erreur : chemin est un dossier {pathOutput_file.resolve()}", 10000)
            return
        elif pathOutput_file.exists() is True:
            self.logger.info(f"ERROR : output file already exists {pathOutput_file.resolve()}")
            self.statusBar().showMessage(f"Erreur : le fichier de sortie existe déjà {pathOutput_file.resolve()}", 10000)
            return

        self.progress_bar.setValue(0)
        self.speed_label.setText("Téléchargement : -- MB/s")
        self.eta_label.setText("Temps restant : --")

        # Launch the thread
        self.downloadThread = QThread()

        self.worker = Worker(
            self.ytDL_interface.download,
            self.ytDL_interface.url,
            format_id,
            pathOutput_file,
        )

        self.worker.moveToThread(self.downloadThread)

        self.download_button.setEnabled(False)  # ← désactive pendant le DL
        self.cancel_button.setEnabled(True)  # ← active le bouton annuler

        self.ytDL_interface.set_cancel_flag(lambda: self.worker._cancelled)
        self.ytDL_interface.set_progress_callback(self.worker.progress.emit)

        # yt-dlp's progress_hook runs INSIDE the worker thread (it's called
        # synchronously from .download(), which itself runs in downloadThread).
        # We never touch widgets from there directly. Instead the hook is just
        # self.worker.progress.emit — emitting a Qt signal is thread-safe.
        # Because the receiver (self.on_download_progress) lives on the UI
        # thread and the emitter lives on downloadThread, Qt automatically
        # uses a queued connection: the slot actually runs later, on the UI
        # thread's event loop. That's what makes it safe to touch the
        # progress bar / labels inside on_download_progress.
        # Jesus claude chill out.
        self.ytDL_interface.set_progress_callback(self.worker.progress.emit)
        self.worker.progress.connect(self.on_download_progress)

        self.downloadThread.started.connect(self.worker.run)
        self.worker.finished.connect(self.on_download_finished)
        self.worker.error.connect(self.on_download_error)

        self.worker.finished.connect(self.downloadThread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.downloadThread.finished.connect(self.downloadThread.deleteLater)

        self.downloadThread.start()

    def on_cancel(self):
        """
        Slot for when the cancel button is clicked.
        """
        if hasattr(self, "worker") and self.worker:
            self.logger.info("Cancel download")
            # self.ytDL_interface.set_cancel_flag(None)  # ← désactive le hook
            self.worker.cancel()  # pose le flag → le hook lève l'exception au prochain tick
            self.cancel_button.setEnabled(False)
            self.resetInfo(isLoading=False, isDownloading=True)
            self.statusBar().showMessage("Annulation du téléchargement...", self.DEFAULT_DELAY_STATUSBAR)

    def on_download_progress(self, d: dict):
        status = d.get("status")

        if status == "downloading":
            self.statusBar().showMessage(f"Téléchargement en cours", self.DEFAULT_DELAY_STATUSBAR)
            total = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
            downloaded = d.get("downloaded_bytes", 0)
            if total:
                percent = int(downloaded * 100 / total)
                self.progress_bar.setValue(percent)

            speed = _strip_ansi(d.get("_speed_str", "N/A"))  # ← strip ici
            eta = _strip_ansi(d.get("_eta_str", "N/A"))  # ← et ici
            self.speed_label.setText(f"Téléchargement : {speed}")
            self.eta_label.setText(f"Temps restant : {eta}")

        elif status == "finished":
            self.logger.info(f"Téléchargement terminé : {d.get('filename')}")
            self.statusBar().showMessage("Téléchargement terminé.", self.DEFAULT_DELAY_STATUSBAR)
            self.progress_bar.setValue(100)
            self.speed_label.setText("Téléchargement : terminé")
            self.eta_label.setText("Temps restant : --")

        elif status == "error":
            self.logger.error(f"Erreur lors du téléchargement.")
            self.statusBar().showMessage("Erreur lors du téléchargement.", 10000)
            self.speed_label.setText("Téléchargement : erreur")
            self.resetInfo(isLoading=False, isDownloading=True)

    def on_download_finished(self):
        """
        Slot for when the download thread is fully done.
        Always called after on_download_error if there was an error/cancellation.
        Only update UI here if it wasn't an error (error slot already handled it).
        """
        self.ytDL_interface.set_cancel_flag(None)
        self.ytDL_interface.set_progress_callback(None)
        self.download_button.setEnabled(True)
        self.cancel_button.setEnabled(False)
        # Ne touche PAS la statusBar ni les labels ici —
        # on_download_error les a déjà mis à jour si nécessaire,
        # et on_download_progress gère le cas "finished" normal.

    def on_download_error(self, e: DownloadError | Exception):
        """
        Slot for when the download thread raised an exception.
        """
        is_cancelled = "cancelled" in str(e).lower()

        if is_cancelled:
            self.statusBar().showMessage("Téléchargement annulé.", self.DEFAULT_DELAY_STATUSBAR)
            self.progress_bar.setValue(0)
            self.speed_label.setText("Téléchargement : annulé")
            self.eta_label.setText("Temps restant : --")
        else:
            errorMsg = ""
            if isinstance(e, DownloadError) and e.msg is not None:
                errorMsg = _strip_ansi(e.msg).split(":")[-1].strip()
            else:
                errorMsg = str(e)
            self.statusBar().showMessage(f"Erreur : {errorMsg}", 10000)
            self.speed_label.setText("Téléchargement : erreur")
            self.eta_label.setText("Temps restant : --")

        self.download_button.setEnabled(True)
        self.cancel_button.setEnabled(False)
        self.progress_bar.setValue(0)

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

    def check_for_update(self):
        """Check latest GitHub release tag against current __version__."""
        try:
            r = requests.get(
                f"https://api.github.com/repos/{self.GITHUB_REPO}/releases/latest",
                timeout=5,
            )
            r.raise_for_status()
            data = r.json()
            latest = data.get("tag_name", "").lstrip("v")
            current = __version__.lstrip("v")

            if not latest or latest == current:
                self.logger.debug("App is up to date.")
                return

            # Récupère le lien du .exe dans les assets
            download_url = next(
                (a["browser_download_url"] for a in data.get("assets", []) if a["name"].endswith(".exe")),
                data.get("html_url", ""),  # fallback sur la page de release
            )

            self.logger.info(f"Update available: {current} → {latest}")

            msg = QMessageBox(self)
            msg.setWindowTitle("Mise à jour disponible")
            msg.setIcon(QMessageBox.Information)
            msg.setText(f"Une nouvelle version est disponible : <b>v{latest}</b><br>(version actuelle : v{current})")
            msg.setInformativeText(f'<a href="{download_url}">Télécharger la nouvelle version</a>')
            msg.setTextFormat(Qt.RichText)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()

        except Exception as e:
            self.logger.warning(f"Update check failed: {e}")