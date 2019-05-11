import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton
from PyQt5.QtGui import *
from PyQt5.QtCore import QCoreApplication


class window(QMainWindow):

    def __init__(self):
        super(window, self).__init__()
        self.setGeometry(50, 50, 500, 300)
        self.setWindowTitle('Test!')
        # self.setWindowIcon(QIcon('Penguins.jpg'))
        self.home()

    def home(self):
        btn = QPushButton('Quit', self)
        btn.clicked.connect(QCoreApplication.instance().quit)
        btn.resize(100, 100)
        btn.move(100, 100)
        btn.show()


def run():
    app = QApplication(sys.argv)
    Gui = window()
    sys.exit(app.exec_())


run()
