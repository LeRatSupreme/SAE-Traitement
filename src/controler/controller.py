from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import QFileDialog
from src.model.model import DownloadModel
from src.view.view import MainView
from ImageWidget import ImageWidget
import numpy as np
from astropy.io import fits
from scipy.ndimage import gaussian_filter, laplace
from skimage.filters import unsharp_mask
import os

class DownloadThread(QThread):
    """
    Thread for downloading FITS files in the background.
    """
    update_status_signal = pyqtSignal(str)

    """
    Initialize the download thread.

    :param model: The model to use for downloading.
    :param target_name: The name of the target object.
    :param surveys: List of surveys to download from.
    :param save_path: Path to save the downloaded files.
    """
    def __init__(self, model, target_name, surveys, save_path):
        super().__init__()
        self.model = model
        self.target_name = target_name
        self.surveys = surveys
        self.save_path = save_path

    """
    Run the download process.
    """
    def run(self):
        self.update_status_signal.emit("Téléchargement en cours...")
        success = self.model.download_fits_files(self.target_name, self.surveys, self.save_path)
        if success:
            self.update_status_signal.emit("Téléchargement terminé avec succès.")
        else:
            self.update_status_signal.emit("Erreur de téléchargement.")

class MainController:
    """
    Main controller for the application.
    """

    """
    Initialize the main controller.
    """
    def __init__(self):
        self.view = MainView()
        self.model = DownloadModel()

        # Connect view actions to controller methods
        self.view.download_button.clicked.connect(self.start_download)
        self.view.process_button.clicked.connect(self.process_image)
        self.view.download_processed_image_button.clicked.connect(self.download_processed_image)

    """
    Start the download process.
    """
    def start_download(self):
        target_name = self.view.get_object_name()
        save_path = self.view.get_folder_path()

        if not target_name or not save_path:
            self.view.update_status("Veuillez entrer un nom d'objet et sélectionner un dossier.")
            return

        surveys = ["DSS2 Red", "DSS2 IR", "DSS2 Blue"]  # List of surveys to download

        # Start the download in a separate thread to avoid blocking the UI
        self.download_thread = DownloadThread(self.model, target_name, surveys, save_path)
        self.download_thread.update_status_signal.connect(self.view.update_status)
        self.download_thread.start()

    """
    Process the downloaded FITS files and display the image.
    """
    def process_image(self):
        try:
            fits_files = self.view.get_fits_files()
            fits_file1 = fits.open(fits_files['red'])
            fits_file2 = fits.open(fits_files['green'])
            fits_file3 = fits.open(fits_files['blue'])

            image_data1 = fits_file1[0].data
            image_data2 = fits_file2[0].data
            image_data3 = fits_file3[0].data

            fits_file1.close()
            fits_file2.close()
            fits_file3.close()

            image_data1 = self.normalize(image_data1)
            image_data2 = self.normalize(image_data2)
            image_data3 = self.normalize(image_data3)

            # Apply sharpening filter
            image_data1 = self.sharpen(image_data1)
            image_data2 = self.sharpen(image_data2)
            image_data3 = self.sharpen(image_data3)

            rgba_image = np.zeros((image_data1.shape[0], image_data1.shape[1], 3))
            rgba_image[..., 0] = image_data1  # Red channel
            rgba_image[..., 1] = image_data2  # Green channel
            rgba_image[..., 2] = image_data3  # Blue channel

            # Use ImageWidget to display the image
            self.view.image_widget.setPixmap(rgba_image)
            self.view.update_status("")
        except Exception as e:
            self.view.update_status(f"Erreur lors du traitement de l'image : {e}")
            print(f"Erreur lors du traitement de l'image : {e}")

    """
    Apply a sharpening filter to the image data.

    :param image_data: The image data to sharpen.
    :param alpha: The sharpening factor.
    :param sigma: The standard deviation for Gaussian kernel.
    :return: The sharpened image data.
    """
    def sharpen(self, image_data, alpha=1.5, sigma=1):
        blurred = gaussian_filter(image_data, sigma=sigma)
        high_pass = image_data - blurred
        sharpened = image_data + alpha * high_pass
        return np.clip(sharpened, 0, 1)

    """
    Download the processed image.
    """
    def download_processed_image(self):
        try:
            file_path, _ = QFileDialog.getSaveFileName(self.view, "Enregistrer l'image traitée", "",
                                                       "PNG Files (*.png)")
            if file_path:
                pixmap = self.view.image_widget.label.pixmap()
                if pixmap:
                    pixmap.save(file_path, "PNG")
                    self.view.update_status("Image traitée téléchargée avec succès.")
                else:
                    self.view.update_status("Erreur : aucune image affichée.")
            else:
                self.view.update_status("Téléchargement annulé.")
        except Exception as e:
            self.view.update_status(f"Erreur lors du téléchargement de l'image : {e}")
            print(f"Erreur lors du téléchargement de l'image : {e}")

    """
    Normalize the image data.

    :param data: The image data to normalize.
    :param min_percent: The minimum percentile for normalization.
    :param max_percent: The maximum percentile for normalization.
    :return: The normalized image data.
    """
    def normalize(self, data, min_percent=1, max_percent=99):
        min_val = np.percentile(data, min_percent)
        max_val = np.percentile(data, max_percent)
        data = np.clip(data, min_val, max_val)
        return (data - min_val) / (max_val - min_val)