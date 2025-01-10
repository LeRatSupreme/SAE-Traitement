import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import matplotlib
matplotlib.use('TkAgg')

def normalize(data, min_percent=1, max_percent=99):
    min_val = np.percentile(data, min_percent)
    max_val = np.percentile(data, max_percent)
    data = np.clip(data, min_val, max_val)
    return (data - min_val) / (max_val - min_val)

fits_file1 = fits.open('fits_files/NGC_3324_DSS2_Red.fits')
fits_file2 = fits.open('fits_files/NGC_3324_GALEX_Near_UV.fits')
fits_file3 = fits.open('fits_files/NGC_3324_2MASS-J.fits')

image_data1 = fits_file1[0].data
image_data2 = fits_file2[0].data
image_data3 = fits_file3[0].data

fits_file1.close()
fits_file2.close()
fits_file3.close()

image_data1 = normalize(image_data1)
image_data2 = normalize(image_data2)
image_data3 = normalize(image_data3)

combined_data = (image_data2 + image_data3) / 2

rgba_image = np.zeros((image_data1.shape[0], image_data1.shape[1], 4))
#Verifier ca pas fini
rgba_image[..., 0] = image_data2  # Red channel
rgba_image[..., 1] = image_data3  # Green channel
rgba_image[..., 2] = image_data1  # Blue channel
rgba_image[..., 3] = 1.0  # Alpha channel

zoom_x_min, zoom_x_max = 1200, 1800
zoom_y_min, zoom_y_max = 1200, 1800

# Display the RGBA image
plt.figure()
plt.imshow(rgba_image, origin='lower')
plt.colorbar()
plt.show()