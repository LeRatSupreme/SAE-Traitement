from astroquery.mast import Observations

# Rechercher des observations sur MAST
def search_and_download_files(target_name, download_path):
    print("Début de la recherche d'observations pour :", target_name)

    # Effectuer une recherche des observations avec un critère d'ID spécifique
    try:
        # ID d'observation spécifique pour JWST
        observations = Observations.query_criteria(
            obs_collection="JWST",
            dataRights="public", 
            obs_id="jw02731-o001_t017_nircam_clear-f090w"
        )
        print(f"Nombre d'observations trouvées pour {target_name} : {len(observations)}")
    except Exception as e:
        print("Erreur lors de la recherche d'observations :", e)
        return

    # Télécharger tous les produits associés, sans filtrage spécifique
    try:
        print("Récupération de la liste des produits...")
        products = Observations.get_product_list(observations)
        print(f"Nombre total de produits trouvés : {len(products)}")
    except Exception as e:
        print("Erreur lors de la récupération de la liste des produits :", e)
        return

    # Télécharger les fichiers sans aucun filtrage
    try:
        print("Téléchargement des fichiers...")
        download_results = Observations.download_products(products, download_dir=download_path, mrp_only=True)
        print(f"Téléchargement terminé. Les fichiers sont enregistrés dans : {download_path}")
    except Exception as e:
        print("Erreur lors du téléchargement des fichiers :", e)
        return


# Remplissez ici le nom de l'objet cible et le chemin de téléchargement
target_name = "NGC 3324"  # Exemple : région "Carina Nebula"
download_path = "./jwst_fits_files"  # Chemin où les fichiers seront téléchargés

# Lancer le téléchargement
search_and_download_files(target_name, download_path)
