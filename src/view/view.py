from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QFileDialog, QGroupBox
from PyQt6.QtCore import Qt

class MainView(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Télécharger et Traiter les Images")
        self.setGeometry(100, 100, 1200, 800)

        # Appliquer un style sombre
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                color: white;
            }
            QPushButton {
                background-color: #333;
                border: 1px solid #444;
                color: white;
                padding: 8px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #555;
            }
            QLineEdit {
                background-color: #333;
                color: white;
                padding: 8px;
                border-radius: 5px;
            }
            QLabel {
                font-size: 16px;
                margin-bottom: 10px;
            }
            QGroupBox {
                border: 1px solid #444;
                padding: 10px;
                background-color: #2e2e2e;
                border-radius: 10px;
            }
        """)

        # Disposition principale
        self.main_layout = QHBoxLayout(self)

        # Disposition centrale pour afficher l'image
        self.center_layout = QVBoxLayout()
        self.image_label = QLabel("Aucune image traitée", self)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.center_layout.addWidget(self.image_label)

        # Disposition à droite pour les contrôles
        self.right_layout = QVBoxLayout()

        # Créer une seule boîte pour les contrôles à droite
        self.control_box = QGroupBox("Contrôles", self)
        self.control_layout = QVBoxLayout()

        # Zone de saisie du nom
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Entrez un nom pour l'objet")
        self.control_layout.addWidget(self.name_input)

        # Sélecteur de dossier
        self.folder_button = QPushButton("Choisir le dossier de destination", self)
        self.folder_button.clicked.connect(self.select_folder)
        self.control_layout.addWidget(self.folder_button)

        # Étiquette pour afficher le dossier sélectionné
        self.selected_folder_label = QLabel("Aucun dossier sélectionné", self)
        self.control_layout.addWidget(self.selected_folder_label)

        # Bouton Télécharger
        self.download_button = QPushButton("Télécharger", self)
        self.control_layout.addWidget(self.download_button)

        # Bouton Traiter
        self.process_button = QPushButton("Traiter l'image", self)
        self.control_layout.addWidget(self.process_button)

        # Réduire l'espacement entre les éléments dans la boîte
        self.control_layout.setSpacing(5)  # Réduit l'espacement entre les widgets

        # Appliquer la disposition des contrôles dans la boîte
        self.control_box.setLayout(self.control_layout)
        self.right_layout.addWidget(self.control_box)

        # Ajouter les deux zones de layout à la fenêtre principale
        self.main_layout.addLayout(self.center_layout, 80)  # La majeure partie pour l'image
        self.main_layout.addLayout(self.right_layout, 20)   # La petite boîte pour les contrôles
        self.setLayout(self.main_layout)

    def update_image_label(self, image_path):
        self.image_label.setPixmap(image_path)
        self.image_label.setText("")

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Sélectionner le dossier")
        if folder:
            self.selected_folder_label.setText(f"Dossier sélectionné : {folder}")
        else:
            self.selected_folder_label.setText("Aucun dossier sélectionné")

    def get_folder_path(self):
        return self.selected_folder_label.text().replace("Dossier sélectionné : ", "")

    def get_object_name(self):
        return self.name_input.text()
