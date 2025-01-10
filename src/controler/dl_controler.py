import os
import requests

class SkyViewModel:
    def __init__(self):
        self.directory = None
        self.nebula_name = None

    def set_directory(self, directory):
        self.directory = directory

    def set_nebula_name(self, nebula_name):
        self.nebula_name = nebula_name

    def download_skyview(self):
        if not self.directory or not self.nebula_name:
            raise ValueError("Directory and nebula name must be set before downloading.")

        # Example URL for downloading from SkyView (this is a placeholder)
        url = f"https://skyview.gsfc.nasa.gov/current/cgi/runquery.pl?Position={self.nebula_name}&Survey=dss"
        response = requests.get(url)

        if response.status_code == 200:
            file_path = os.path.join(self.directory, f"{self.nebula_name}.fits")
            with open(file_path, 'wb') as file:
                file.write(response.content)
            return file_path
        else:
            raise Exception("Failed to download data from SkyView.")