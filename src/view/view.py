from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QFileDialog, QGroupBox
from PyQt6.QtCore import Qt
from ImageWidget import ImageWidget

class MainView(QWidget):
    """
    Main view for the application, providing the user interface for downloading and processing images.
    """
    def __init__(self):
        """
        Initialize the main view with all UI components and layout.
        """
        super().__init__()

        self.setWindowTitle("Télécharger et Traiter les Images")
        self.setGeometry(100, 100, 1200, 800)

        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                color: white;
            }
            QPushButton {
                background-color: #333;
                border: 1px solid #444;
                color: white;
                padding: 8px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #555;
            }
            QLineEdit {
                background-color: #333;
                color: white;
                padding: 8px;
                border-radius: 5px;
            }
            QLabel {
                font-size: 16px;
                margin-bottom: 10px;
            }
            QGroupBox {
                border: 1px solid #444;
                padding: 10px;
                background-color: #2e2e2e;
                border-radius: 10px;
            }
        """)

        # Main layout
        self.main_layout = QHBoxLayout(self)

        # Center layout
        self.center_layout = QVBoxLayout()
        self.image_widget = ImageWidget()
        self.center_layout.addWidget(self.image_widget)

        # Button to download the processed image
        self.download_processed_image_button = QPushButton("Télécharger l'image traitée", self)
        self.center_layout.addWidget(self.download_processed_image_button)

        # Right layout
        self.right_layout = QVBoxLayout()

        # Create a single box for controls
        self.control_box = QGroupBox("Contrôles", self)
        self.control_layout = QVBoxLayout()

        # Input field for object name
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Entrez un nom pour l'objet")
        self.control_layout.addWidget(self.name_input)

        # Folder selector
        self.folder_button = QPushButton("Choisir le dossier de destination", self)
        self.folder_button.clicked.connect(self.select_folder)
        self.control_layout.addWidget(self.folder_button)

        # Label to display the selected folder
        self.selected_folder_label = QLabel("Aucun dossier sélectionné", self)
        self.control_layout.addWidget(self.selected_folder_label)

        # Download button
        self.download_button = QPushButton("Télécharger", self)
        self.control_layout.addWidget(self.download_button)

        # Buttons to select FITS files
        self.red_file_button = QPushButton("Sélectionner le fichier FITS pour le canal rouge", self)
        self.red_file_button.clicked.connect(lambda: self.select_fits_file('red'))
        self.control_layout.addWidget(self.red_file_button)

        self.green_file_button = QPushButton("Sélectionner le fichier FITS pour le canal vert", self)
        self.green_file_button.clicked.connect(lambda: self.select_fits_file('green'))
        self.control_layout.addWidget(self.green_file_button)

        self.blue_file_button = QPushButton("Sélectionner le fichier FITS pour le canal bleu", self)
        self.blue_file_button.clicked.connect(lambda: self.select_fits_file('blue'))
        self.control_layout.addWidget(self.blue_file_button)

        # Labels to display selected files
        self.red_file_label = QLabel("Aucun fichier sélectionné pour le canal rouge", self)
        self.control_layout.addWidget(self.red_file_label)

        self.green_file_label = QLabel("Aucun fichier sélectionné pour le canal vert", self)
        self.control_layout.addWidget(self.green_file_label)

        self.blue_file_label = QLabel("Aucun fichier sélectionné pour le canal bleu", self)
        self.control_layout.addWidget(self.blue_file_label)

        # Button to process the image
        self.process_button = QPushButton("Traiter l'image", self)
        self.control_layout.addWidget(self.process_button)

        # Reduce spacing between elements in the box
        self.control_layout.setSpacing(5)

        # Apply the control layout to the box
        self.control_box.setLayout(self.control_layout)
        self.right_layout.addWidget(self.control_box)

        # Add the two layout areas to the main window
        self.main_layout.addLayout(self.center_layout, 80)  # Majority for the image
        self.main_layout.addLayout(self.right_layout, 20)   # Small box for controls
        self.setLayout(self.main_layout)

        # Instance variables to store file paths
        self.red_file_path = ""
        self.green_file_path = ""
        self.blue_file_path = ""

    def update_status(self, message):
        """
        Update the status message displayed on the image widget.

        :param message: The status message to display.
        """
        self.image_widget.label.setText(message)

    def update_image_label(self, image_path):
        """
        Update the image label with a new image.

        :param image_path: The path to the new image.
        """
        pixmap = QPixmap(image_path)
        self.image_widget.setQPixmap(pixmap)
        self.image_widget.label.setText("")

    def select_folder(self):
        """
        Open a dialog to select a folder and update the label with the selected folder path.
        """
        folder = QFileDialog.getExistingDirectory(self, "Sélectionner le dossier")
        if folder:
            self.selected_folder_label.setText(f"Dossier sélectionné : {folder}")
        else:
            self.selected_folder_label.setText("Aucun dossier sélectionné")

    def select_fits_file(self, channel):
        """
        Open a dialog to select a FITS file and update the corresponding label with the selected file path.

        :param channel: The color channel ('red', 'green', or 'blue') for which the file is being selected.
        """
        file, _ = QFileDialog.getOpenFileName(self, "Sélectionner le fichier FITS", "", "FITS Files (*.fits)")
        if file:
            if channel == 'red':
                self.red_file_path = file
                self.red_file_label.setText("Fichier canal rouge sélectionné")
            elif channel == 'green':
                self.green_file_path = file
                self.green_file_label.setText("Fichier canal vert sélectionné")
            elif channel == 'blue':
                self.blue_file_path = file
                self.blue_file_label.setText("Fichier canal bleu sélectionné")

    def get_folder_path(self):
        """
        Get the path of the selected folder.

        :return: The path of the selected folder.
        """
        return self.selected_folder_label.text().replace("Dossier sélectionné : ", "")

    def get_object_name(self):
        """
        Get the name of the object entered by the user.

        :return: The name of the object.
        """
        return self.name_input.text()

    def get_fits_files(self):
        """
        Get the paths of the selected FITS files.

        :return: A dictionary with the paths of the selected FITS files for each color channel.
        """
        return {
            'red': self.red_file_path,
            'green': self.green_file_path,
            'blue': self.blue_file_path
        }