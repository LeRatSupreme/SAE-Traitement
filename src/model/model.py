from astroquery.skyview import SkyView
import os

class DownloadModel:
    """
    Model class for downloading FITS files using the SkyView service.
    """
    def __init__(self):
        """
        Initialize the DownloadModel with a SkyView instance.
        """
        self.skyview = SkyView()

    def download_fits_files(self, target_name, surveys, save_path):
        """
        Download FITS files for a given target name from specified surveys and save them to the specified path.

        :param target_name: The name of the target object.
        :param surveys: List of surveys to download from.
        :param save_path: Path to save the downloaded files.
        :return: True if the download was successful, False otherwise.
        """
        try:
            print(f"Recherche des images pour {target_name} dans les relevés : {surveys}")

            # Téléchargement des images FITS
            fits_files = self.skyview.get_images(position=target_name, survey=surveys)

            # Vérifier si des fichiers ont été récupérés
            if not fits_files:
                print(f"Aucune image disponible pour {target_name} dans les relevés demandés.")
                return False

            # Sauvegarde des fichiers FITS
            os.makedirs(save_path, exist_ok=True)  # Créer le dossier si nécessaire
            for idx, hdul in enumerate(fits_files):
                survey_name = surveys[idx].replace(" ", "_")  # Remplacer les espaces pour le nom de fichier
                file_path = f"{save_path}/{target_name.replace(' ', '_')}_{survey_name}.fits"
                hdul.writeto(file_path, overwrite=True)
                print(f"Fichier FITS sauvegardé : {file_path}")

            print("Tous les fichiers ont été téléchargés et enregistrés.")
            return True

        except Exception as e:
            print(f"Erreur lors du téléchargement des fichiers FITS : {e}")
            return False