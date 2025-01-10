# src/view/app.py

import sys
from PyQt6.QtWidgets import QApplication
from src.controler.install_controller import InstallController
from src.view.install_view import InstallWindow

def main():
    app = QApplication(sys.argv)

    # Créer la vue
    install_window = InstallWindow()

    # Créer le contrôleur et le lier à la vue
    controller = InstallController(install_window)

    install_window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
