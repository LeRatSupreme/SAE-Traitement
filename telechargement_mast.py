from astroquery.mast import Observations
from astropy.io import fits
import os

# Étape 1: Télécharger les données
def download_fits_images():
    # Query MAST pour les données JWST, filtrées sur l'instrument F090W et l'objet 'NGC 3132'
    obs_table = Observations.query_criteria(obs_collection='JWST', dataproduct_type='image', filters='F090W', objectname='NGC 3132')

    # Récupérer la liste des produits de données
    data_products = Observations.get_product_list(obs_table)

    # Filtrer les produits pour obtenir ceux de type 'DRZ' (image réduite)
    drz_products = Observations.filter_products(data_products, productSubGroupDescription='DRZ')

    # Télécharger les trois premiers produits DRZ
    fits_files = Observations.download_products(drz_products[:3])

    # Vérifier si des fichiers ont été téléchargés
    if fits_files is None or 'Local Path' not in fits_files.colnames:
        return None

    # Extraire les chemins locaux des fichiers FITS téléchargés
    fits_files_paths = fits_files['Local Path']

    return fits_files_paths

# Étape 2: Charger les fichiers FITS
def load_fits_files(fits_files_paths):
    # Charger les fichiers FITS un par un
    fits_file_one = fits.open(fits_files_paths[0])
    fits_file_two = fits.open(fits_files_paths[1])
    fits_file_three = fits.open(fits_files_paths[2])

    # Afficher les informations de chaque fichier FITS
    print(f"FITS File 1 Info: {fits_file_one.info()}")
    print(f"FITS File 2 Info: {fits_file_two.info()}")
    print(f"FITS File 3 Info: {fits_file_three.info()}")

    return fits_file_one, fits_file_two, fits_file_three

# Fonction principale pour télécharger et charger les fichiers FITS
def main():
    # Télécharger les fichiers FITS
    fits_files_paths = download_fits_images()

    # Vérifier que des fichiers ont été téléchargés
    if fits_files_paths:
        # Charger les fichiers FITS
        load_fits_files(fits_files_paths)
    else:
        print("Aucun fichier n'a été téléchargé.")

# Exécution du script
if __name__ == "__main__":
    main()