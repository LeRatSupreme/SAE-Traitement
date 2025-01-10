# src/view/install_view.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QFileDialog, QLabel
from PyQt6.QtCore import Qt

class InstallWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Configurer la fenêtre
        self.setWindowTitle("Installer une application")
        self.resize(600, 400)

        # Définir un style sombre
        self.setStyleSheet("""
            QWidget { background-color: #2e2e2e; font-family: 'Segoe UI'; color: #ffffff; }
            QLineEdit { font-size: 18px; padding: 10px; border: 2px solid #444444; border-radius: 5px; background-color: #3a3a3a; color: #ffffff; }
            QPushButton { font-size: 18px; padding: 10px; background-color: #1a73e8; color: white; border: none; border-radius: 5px; }
            QPushButton:hover { background-color: #155ab6; }
            QLabel { font-size: 16px; color: #bbbbbb; padding: 0px; margin-bottom: -10px; }
        """)

        # Disposition verticale
        layout = QVBoxLayout()

        # Champ de saisie pour le nom de la nébuleuse
        self.nebula_name_input = QLineEdit(self)
        self.nebula_name_input.setPlaceholderText("Nom de la nébuleuse type NGC 3324, M1 ou CRAB-NEBULA")
        layout.addWidget(self.nebula_name_input)

        # Étiquette pour le répertoire sélectionné
        self.directory_label = QLabel("Répertoire : Aucun sélectionné", self)
        self.directory_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.directory_label)

        # Bouton pour choisir le répertoire
        self.choose_directory_button = QPushButton("Choisir le répertoire")
        self.choose_directory_button.clicked.connect(self.choose_directory)
        layout.addWidget(self.choose_directory_button)

        # Bouton pour télécharger
        self.download_button = QPushButton("Télécharger")
        layout.addWidget(self.download_button)

        # Appliquer la disposition
        self.setLayout(layout)

    def choose_directory(self):
        # Ouvrir un dialogue pour choisir un répertoire
        directory = QFileDialog.getExistingDirectory(self, "Choisir le répertoire")
        if directory:
            self.directory_label.setText(f"Répertoire : {directory}")
