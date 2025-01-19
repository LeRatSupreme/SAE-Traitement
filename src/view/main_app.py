from PyQt6.QtWidgets import QApplication
from src.controler.controller import MainController

if __name__ == "__main__":
    app = QApplication([])
    controller = MainController()
    controller.view.show()
    app.exec()



