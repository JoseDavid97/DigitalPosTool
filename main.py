import sys
from source.app import MainApp
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    posApp = QApplication(sys.argv)
    lg = MainApp()
    lg.show()
    sys.exit(posApp.exec())