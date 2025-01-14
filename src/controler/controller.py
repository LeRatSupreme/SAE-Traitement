# src/controller/controller.py

from src.model.model import DownloadModel
from src.view.view import MainView
from PyQt6.QtCore import QThread, pyqtSignal

class DownloadThread(QThread):
    update_status_signal = pyqtSignal(str)

    def __init__(self, model, target_name, surveys, save_path):
        super().__init__()
        self.model = model
        self.target_name = target_name
        self.surveys = surveys
        self.save_path = save_path

    def run(self):
        self.update_status_signal.emit("Téléchargement en cours...")
        success = self.model.download_fits_files(self.target_name, self.surveys, self.save_path)
        if success:
            self.update_status_signal.emit("Téléchargement terminé avec succès.")
        else:
            self.update_status_signal.emit("Erreur de téléchargement.")

class MainController:
    def __init__(self):
        self.view = MainView()
        self.model = DownloadModel()

        # Connexion des actions de la vue
        self.view.download_button.clicked.connect(self.start_download)

    def start_download(self):
        target_name = self.view.get_object_name()
        save_path = self.view.get_folder_path()

        if not target_name or not save_path:
            self.view.update_status("Veuillez entrer un nom d'objet et sélectionner un dossier.")
            return

        surveys = ["DSS2 Red", "DSS1 Blue", "GALEX Near UV"]  # Liste des relevés à télécharger

        # Lancer le téléchargement dans un thread séparé pour ne pas bloquer l'interface utilisateur
        self.download_thread = DownloadThread(self.model, target_name, surveys, save_path)
        self.download_thread.update_status_signal.connect(self.view.update_status)
        self.download_thread.start()
