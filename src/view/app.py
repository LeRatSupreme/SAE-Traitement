import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt  # Importation de Qt pour AlignCenter
from install_view import InstallWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configurer la fenêtre principale
        self.setWindowTitle("Application PyQt6")
        self.resize(800, 600)

        # Définir un style sombre
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2e2e2e; 
                font-family: 'Segoe UI'; 
                color: #ffffff;
            }
            QLabel {
                font-size: 24px; 
                font-weight: bold; 
                color: #ffffff; 
                margin-bottom: 20px;
            }
            QPushButton {
                font-size: 18px; 
                padding: 10px; 
                background-color: #1a73e8; 
                color: white; 
                border: none; 
                border-radius: 5px;
                margin: 5px 0;
            }
            QPushButton:hover {
                background-color: #155ab6; 
            }
        """)

        # Créer un widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Créer une disposition verticale
        layout = QVBoxLayout()

        # Ajouter un label de bienvenue
        self.label = QLabel("Bienvenue dans l'application PyQt6!")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Correction ici
        layout.addWidget(self.label)

        # Ajouter un bouton pour installer une application
        self.install_button = QPushButton("Installer une application")
        self.install_button.clicked.connect(self.install_application)
        layout.addWidget(self.install_button)

        # Ajouter un bouton pour traiter une image
        self.process_button = QPushButton("Traiter une image")
        self.process_button.clicked.connect(self.process_image)
        layout.addWidget(self.process_button)

        # Appliquer la disposition au widget central
        central_widget.setLayout(layout)

    def install_application(self):
        # Ouvrir la fenêtre d'installation
        self.install_window = InstallWindow()
        self.install_window.show()

    def process_image(self):
        # Modifier le texte du label pour indiquer le traitement
        self.label.setText("Traitement de l'image en cours...")

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Créer et afficher la fenêtre principale
    window = MainWindow()
    window.show()

    sys.exit(app.exec())
