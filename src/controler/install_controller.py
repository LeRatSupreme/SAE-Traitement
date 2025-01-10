# src/controller/install_controller.py

from src.model.downloader import Downloader
from src.view.install_view import InstallWindow

class InstallController:
    def __init__(self, view: InstallWindow):
        self.view = view
        self.downloader = Downloader()

        # Connecter le bouton de téléchargement
        self.view.download_button.clicked.connect(self.handle_download)

    def handle_download(self):
        target_name = self.view.nebula_name_input.text()
        save_path = self.view.directory_label.text().replace("Répertoire : ", "")

        if target_name and save_path:
            self.downloader.download_fits_files(target_name, save_path)
        else:
            print("Veuillez fournir un nom de nébuleuse et un répertoire pour le téléchargement.")
