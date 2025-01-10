import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import matplotlib
from scipy.ndimage import gaussian_filter, median_filter, sobel
from skimage import img_as_float
from skimage.filters import unsharp_mask

matplotlib.use('TkAgg')

def normalize(data, min_percent=1, max_percent=99):
    min_val = np.percentile(data, min_percent)
    max_val = np.percentile(data, max_percent)
    data = np.clip(data, min_val, max_val)
    return (data - min_val) / (max_val - min_val)

# Open FITS files
fits_file1 = fits.open('Tarantula/Tarantula_Nebula-halpha.fit')
fits_file2 = fits.open('Tarantula/Tarantula_Nebula-oiii.fit')
fits_file3 = fits.open('Tarantula/Tarantula_Nebula-sii.fit')

# Extract image data
image_data1 = fits_file1[0].data
image_data2 = fits_file2[0].data
image_data3 = fits_file3[0].data

# Close FITS files
fits_file1.close()
fits_file2.close()
fits_file3.close()

# Normalize image data
image_data1 = normalize(image_data1)
image_data2 = normalize(image_data2)
image_data3 = normalize(image_data3)

# Apply filters
image_data1_filtered = gaussian_filter(image_data1, sigma=1)
image_data2_filtered = median_filter(image_data2, size=3)
image_data3_filtered = sobel(image_data3)

# Apply unsharp masking to enhance sharpness
image_data1_sharpened = unsharp_mask(image_data1_filtered, radius=1, amount=1)
image_data2_sharpened = unsharp_mask(image_data2_filtered, radius=1, amount=1)
image_data3_sharpened = unsharp_mask(image_data3_filtered, radius=1, amount=1)

# Combine filtered images into an RGBA image
rgba_image = np.zeros((image_data1.shape[0], image_data1.shape[1], 4))
rgba_image[..., 0] = image_data1_sharpened  # Red channel
rgba_image[..., 1] = image_data2_sharpened  # Green channel
rgba_image[..., 2] = image_data3_sharpened  # Blue channel
rgba_image[..., 3] = 1.0  # Alpha channel

# Clip the RGBA image to the valid range [0, 1]
rgba_image = np.clip(rgba_image, 0, 1)

# Display the RGBA image
plt.figure()
plt.imshow(rgba_image, origin='lower')
plt.colorbar()
plt.show()