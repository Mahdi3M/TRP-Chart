from PyQt5.QtWidgets import *
from lib.MyWindow import *
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CustomWindow()
    window.setWindowIcon(QIcon('Images\logo.jpg'))
    window.show()
    app.exec()
