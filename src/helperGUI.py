from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QDialogButtonBox


class HelpDialog(QDialog):
    STEPS = [
        ("1. Colle l'URL", "Copie l'URL YouTube dans le champ URL en haut.\nLes playlists sont nettoyées automatiquement."),
        ("2. Choisis le type", "Sélectionne Vidéo (image + son) ou Audio seul.\nCe choix filtre les qualités disponibles."),
        ("3. Clique sur Charger", "L'app récupère le titre, la miniature et\nla liste des formats disponibles."),
        ("4. Choisis la qualité", "Sélectionne la résolution dans la liste.\nPour la vidéo, le son est ajouté automatiquement."),
        ("5. Choisis le dossier", "Clique sur Parcourir.\nLe nom du fichier est généré depuis le titre."),
        ("6. Télécharge", "Clique sur Télécharger.\nTu peux annuler à tout moment avec Annuler."),
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Aide")
        self.setMinimumWidth(400)
        layout = QVBoxLayout(self)

        for title, body in self.STEPS:
            title_label = QLabel(title)
            title_label.setStyleSheet("font-weight: bold; font-size: 14px; margin-top: 8px;")
            body_label = QLabel(body)
            body_label.setWordWrap(True)
            layout.addWidget(title_label)
            layout.addWidget(body_label)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        buttons.accepted.connect(self.accept)
        layout.addWidget(buttons)
