import sys
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton


class window(QMainWindow):

    def __init__(self):
        super(window, self).__init__()
        self.setGeometry(1000, 100, 300, 300)
        self.setWindowTitle('Test!')
        # self.setWindowIcon(QIcon('pic.png'))
        self.home()

    def home(self):
        btn = QPushButton('quit', self)
        btn.clicked.connect(QCoreApplication.instance().quit)
        btn.resize(50, 30)  # size of the button (width, hight)
        btn.move(200, 200)  # location
        self.show()


def run():
    app = QApplication(sys.argv)
    Gui = window()
    sys.exit(app.exec_())


run()
