import sys
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QAction


class window(QMainWindow):

    def __init__(self):
        super(window, self).__init__()
        self.setGeometry(800, 100, 500, 300)
        self.setWindowTitle('Test!')
        # self.setWindowIcon(QIcon('pic.png'))

        extractAction = QAction('&Get to the choppah', self)
        extractAction.setShortcut('Ctrl+Q')
        extractAction.setStatusTip('leave the app')
        extractAction.triggered.connect(self.close_application)

        self.statusBar()

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(extractAction)

        self.home()

    def home(self):
        btn = QPushButton('quit', self)
        btn.clicked.connect(self.close_application)
        btn.resize(btn.sizeHint())  # size of the button (width, hight)
        btn.move(0, 100)  # location
        self.show()

    def close_application(self):
        print("so custom!")
        sys.exit()


def run():
    app = QApplication(sys.argv)
    Gui = window()
    sys.exit(app.exec_())


run()
