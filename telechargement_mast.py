from astroquery.mast import Mast
from astroquery.mast import Observations
import os


# Fonction pour télécharger les images à partir de MAST
def download_mast_images(target_name, radius, download_dir="./mast_images/"):
    # Crée le dossier de téléchargement si nécessaire
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    # Recherche des observations du télescope Hubble sur la cible
    observations = Observations.query_criteria(target_name=target_name, radius=radius)

    # Affiche les observations disponibles
    print(f"Observations disponibles pour {target_name} :")
    print(observations)

    # Télécharge les fichiers FITS associés aux observations
    if len(observations) > 0:
        # Téléchargement des fichiers FITS
        for observation in observations:
            file_table = Observations.get_product_list(observation)
            fits_files = file_table[file_table['productSubGroupDescription'] == 'FITS']

            # Télécharge chaque fichier FITS
            for _, fits_file in fits_files.iterrows():
                file_url = fits_file['dataURL']
                file_name = fits_file['productFilename']
                print(f"Téléchargement du fichier : {file_name}")
                Observations.download_products([fits_file], download_dir)
                print(f"Fichier téléchargé : {file_name}")
    else:
        print("Aucune observation trouvée pour cette cible.")


# Exemple d'utilisation
target_name = "M51"  # Nom de la cible (ex: M51, un objet astronomique)
radius = 0.1  # Rayon de recherche en degrés

# Lancer le téléchargement des images FITS
download_mast_images(target_name, radius)
