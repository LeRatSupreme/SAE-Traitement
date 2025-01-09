import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import matplotlib
matplotlib.use('TkAgg')

# Function to normalize the data with cutoff limits
def normalize(data, min_percent=1, max_percent=99):
    if data is None:
        raise ValueError("Data is None")
    min_val = np.percentile(data, min_percent)
    max_val = np.percentile(data, max_percent)
    data = np.clip(data, min_val, max_val)
    return (data - min_val) / (max_val - min_val)

# Open the JWST FITS file
fits_file = 'jwst_fits_files/mastDownload/JWST/jw01522-o002_t001_miri_f1800w-brightsky/jw01522-o002_t001_miri_f1800w-brightsky_i2d.fits'
hdul = fits.open(fits_file)

# Extract the SCI data (assuming the SCI data is in the first extension)
image_data = hdul[1].data

# Close the FITS file
hdul.close()

# Check the image data shape
print(f"Image data shape: {image_data.shape}")
print(f"Min and max values before normalization: {image_data.min()}, {image_data.max()}")

# Normalize the image data
image_data_normalized = normalize(image_data)

# Check the normalized values
print(f"Min and max values after normalization: {image_data_normalized.min()}, {image_data_normalized.max()}")

# Combine the images into a single RGBA image (for simplicity, using the normalized image data for all channels)
rgba_image = np.zeros((image_data_normalized.shape[0], image_data_normalized.shape[1], 4))
rgba_image[..., 0] = image_data_normalized  # Red channel
rgba_image[..., 1] = image_data_normalized  # Green channel
rgba_image[..., 2] = image_data_normalized  # Blue channel
rgba_image[..., 3] = 1.0  # Alpha channel (opacity)

# Zoom in on the region of interest (ensure the values are within bounds)
zoom_x_min, zoom_x_max = 100, 300  # Example range for x-axis (must be within 0-549)
zoom_y_min, zoom_y_max = 100, 300  # Example range for y-axis (must be within 0-550)

# Ensure the zoom coordinates are valid
zoom_x_min = max(zoom_x_min, 0)
zoom_x_max = min(zoom_x_max, image_data_normalized.shape[1])
zoom_y_min = max(zoom_y_min, 0)
zoom_y_max = min(zoom_y_max, image_data_normalized.shape[0])

# Display the full image without zoom (check values across the entire image)
plt.figure()
plt.imshow(image_data_normalized, cmap='gray', origin='lower')
plt.colorbar()
plt.show()

# Display the RGBA image with zoom
plt.figure()
plt.imshow(rgba_image[zoom_y_min:zoom_y_max, zoom_x_min:zoom_x_max], origin='lower')
plt.colorbar()
plt.show()
