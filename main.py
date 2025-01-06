import os
import matplotlib.pyplot as plt
import numpy as np
from astropy.io import fits

# Chemin vers le dossier contenant les fichiers .fit
folder_path = 'Tarantula/'

# Parcourir les fichiers dans le dossier
for filename in os.listdir(folder_path):
    if filename.endswith('.fit') or filename.endswith('.fits'):
        file_path = os.path.join(folder_path, filename)

        # Lire le fichier .fit
        with fits.open(file_path) as hdul:
            data = hdul[0].data

            # Afficher l'image
            plt.figure()
            plt.imshow(data, cmap='gray', origin='lower')
            plt.colorbar()
            plt.title(f'Image: {filename}')
            plt.xlabel('Pixel X')
            plt.ylabel('Pixel Y')
            plt.show()