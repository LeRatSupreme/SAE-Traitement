import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import matplotlib
matplotlib.use('TkAgg')

# Fonction pour normaliser les données avec des limites de coupure
def normalize(data, min_percent=1, max_percent=99):
    min_val = np.percentile(data, min_percent)
    max_val = np.percentile(data, max_percent)
    data = np.clip(data, min_val, max_val)
    return (data - min_val) / (max_val - min_val)

# Ouvrir les fichiers FITS
fits_file1 = fits.open('jw02731-o001_t017_nircam_clear-f090w_i2d.fits')

# Extraire les données des images
image_data1 = fits_file1[0].data

# Fermer les fichiers FITS
fits_file1.close()

# Normaliser les données des images
image_data1 = normalize(image_data1)

# Combiner les images en une seule image RGB
# Création d'une image RGB
rgb_image = np.zeros((image_data1.shape[0], image_data1.shape[1], 3))
rgb_image[..., 0] = image_data1  # Canal rouge

# Zoom sur la région d'intérêt (par exemple autour du centre)
zoom_x_min, zoom_x_max = 1200, 1800  # Ajustez ces valeurs
zoom_y_min, zoom_y_max = 1200, 1800  # Ajustez ces valeurs

# Afficher l'image RGB
plt.figure()
plt.imshow(image_data1, origin = 'lower')
plt.colorbar()
plt.show()