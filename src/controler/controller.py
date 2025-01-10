from src.model.downloader import Downloader
from src.view.install_view import InstallWindow

class InstallController:
    def __init__(self, view: InstallWindow):
        self.view = view
        self.downloader = Downloader()

        # Connecter les actions dans la vue aux méthodes du contrôleur
        self.view.download_button.clicked.connect(self.download_fits_files)

    def download_fits_files(self):
        # Récupérer le nom de la nébuleuse et le répertoire à partir de la vue
        nebula_name = self.view.nebula_name_input.text()
        directory = self.view.directory_label.text().replace("Répertoire : ", "")

        if nebula_name and directory:
            self.downloader.download_fits_files(nebula_name, directory)
        else:
            print("Veuillez entrer un nom de nébuleuse et sélectionner un répertoire.")
