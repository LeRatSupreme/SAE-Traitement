import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import matplotlib
from skimage.transform import resize

matplotlib.use('TkAgg')

def normalize(data, min_percent=1, max_percent=99):
    min_val = np.percentile(data, min_percent)
    max_val = np.percentile(data, max_percent)
    data = np.clip(data, min_val, max_val)
    return (data - min_val) / (max_val - min_val)

fits_file1 = fits.open('mastDownload/HLA/hst_05369_ly_wfpc2_f606w_pc_01/hst_05369_ly_wfpc2_f606w_pc_01_drz.fits')
fits_file2 = fits.open('mastDownload/HLA/hst_05369_h0_wfpc2_f606w_pc_01/hst_05369_h0_wfpc2_f606w_pc_01_drz.fits')
fits_file3 = fits.open('mastDownload/HLA/hst_05369_h0_wfpc2_f606w_wf_01/hst_05369_h0_wfpc2_f606w_wf_01_drz.fits')

image_data1 = fits_file1[0].data
image_data2 = fits_file2[0].data
image_data3 = fits_file3[0].data

fits_file1.close()
fits_file2.close()
fits_file3.close()

image_data1 = normalize(image_data1)
image_data2 = normalize(image_data2)
image_data3 = normalize(image_data3)

# Resize image_data2 and image_data3 to match the shape of image_data1
image_data2_resized = resize(image_data2, image_data1.shape, anti_aliasing=True)
image_data3_resized = resize(image_data3, image_data1.shape, anti_aliasing=True)

combined_data = (image_data2_resized + image_data3_resized) / 2

rgba_image = np.zeros((image_data1.shape[0], image_data1.shape[1], 4))
rgba_image[..., 0] = image_data2_resized  # Red channel
rgba_image[..., 1] = image_data3_resized  # Green channel
rgba_image[..., 2] = image_data1  # Blue channel
rgba_image[..., 3] = 1.0  # Alpha channel

zoom_x_min, zoom_x_max = 1200, 1800
zoom_y_min, zoom_y_max = 1200, 1800

# Display the RGBA image
plt.figure()
plt.imshow(rgba_image, origin='lower')
plt.colorbar()
plt.show()