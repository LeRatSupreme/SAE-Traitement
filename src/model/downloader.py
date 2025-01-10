import os
from astroquery.skyview import SkyView

class Downloader:
    def download_fits_files(self, target_name, save_path):
        try:
            print(f"Recherche des images pour {target_name}")

            # Initialiser l'objet SkyView
            skyview = SkyView()

            # Téléchargement des images FITS
            fits_files = skyview.get_images(position=target_name, survey=["DSS2 Red", "DSS1 Blue", "GALEX Near UV"])

            # Vérifier si des fichiers ont été récupérés
            if not fits_files:
                print(f"Aucune image disponible pour {target_name}.")
                return

            # Sauvegarde des fichiers FITS
            for idx, hdul in enumerate(fits_files):
                survey_name = f"survey_{idx}"
                file_path = f"{save_path}/{target_name.replace(' ', '_')}_{survey_name}.fits"
                hdul.writeto(file_path, overwrite=True)
                print(f"Fichier FITS sauvegardé : {file_path}")

            print("Tous les fichiers ont été téléchargés et enregistrés.")

        except Exception as e:
            print(f"Erreur lors du téléchargement des fichiers FITS : {e}")
