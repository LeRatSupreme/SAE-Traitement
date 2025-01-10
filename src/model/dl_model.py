from PyQt6.QtWidgets import QFileDialog
from dl_model import SkyViewModel
from install_view import InstallWindow

class InstallController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        self.view.choose_directory_button.clicked.connect(self.choose_directory)
        self.view.download_button.clicked.connect(self.download_skyview)

    def choose_directory(self):
        directory = QFileDialog.getExistingDirectory(self.view, "Choisir le répertoire")
        if directory:
            self.model.set_directory(directory)
            self.view.directory_label.setText(f"Répertoire : {directory}")

    def download_skyview(self):
        nebula_name = self.view.nebula_name_input.text()
        self.model.set_nebula_name(nebula_name)
        try:
            file_path = self.model.download_skyview()
            self.view.directory_label.setText(f"Téléchargé : {file_path}")
        except Exception as e:
            self.view.directory_label.setText(f"Erreur : {str(e)}")