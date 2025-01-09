from astroquery.skyview import SkyView
import os


# Fonction pour télécharger plusieurs fichiers FITS d'un objet céleste
def download_fits_files(target_name, surveys, save_path):
    try:
        print(f"Recherche des images pour {target_name} dans les relevés : {surveys}")

        # Initialiser l'objet SkyView
        skyview = SkyView()

        # Téléchargement des images FITS
        # "get_images" nécessite la position (target_name) et le(s) survey(s) spécifié(s)
        fits_files = skyview.get_images(position="M1", survey=['Fermi 5', 'HRI', 'DSS'])

        # Vérifier si des fichiers ont été récupérés
        if not fits_files:
            print(f"Aucune image disponible pour {target_name} dans les relevés demandés.")
            return

        # Sauvegarde des fichiers FITS
        for idx, hdul in enumerate(fits_files):
            survey_name = surveys[idx].replace(" ", "_")  # Remplacer les espaces pour le nom de fichier
            file_path = f"{save_path}/{target_name.replace(' ', '_')}_{survey_name}.fits"
            hdul.writeto(file_path, overwrite=True)
            print(f"Fichier FITS sauvegardé : {file_path}")

        print("Tous les fichiers ont été téléchargés et enregistrés.")

    except Exception as e:
        print(f"Erreur lors du téléchargement des fichiers FITS : {e}")


# Exemple d'utilisation
target_name = "NGC 3324"  # Exemple : nébuleuse dans la région Carina
surveys = ["DSS2 Red", "2MASS-J", "GALEX Near UV"]  # Liste corrigée des relevés
save_path = "./fits_files"  # Répertoire pour enregistrer les fichiers

# Créer le dossier si nécessaire
os.makedirs(save_path, exist_ok=True)

# Lancer le téléchargement
download_fits_files(target_name, surveys, save_path)
