import sys
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtGui import QIcon
# from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QAction, QMessageBox
# from PyQt5.uic.properties import QtGui
from PyQt5.QtWidgets import QCheckBox, QProgressBar


class window(QMainWindow):

    def __init__(self):
        super(window, self).__init__()
        self.setGeometry(50, 50, 500, 300)
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

        extractAction = QAction(QIcon('pic.png'), 'flee the scene', self)
        extractAction.triggered.connect(self.close_application)

        self.toolBar = self.addToolBar('extraction')
        self.toolBar.addAction(extractAction)

        self.progress = QProgressBar(self)
        self.progress.setGeometry(200, 80, 250, 20)

        self.home()

    def home(self): # disabling this line will also works fine!
        btn = QPushButton('quit', self)
        btn.clicked.connect(self.close_application)
        btn.resize(btn.sizeHint())  # size of the button (width, hight)
        btn.move(0, 100)  # location

        checkBox = QCheckBox('Enlarge window', self)
        # checkBox.toggle() # to be checked from the beginning
        checkBox.move(0,50)
        checkBox.stateChanged.connect(self.enlarge_window)

        # self.progress = QProgressBar(self)
        # self.progress.setGeometry(200,80,250,20)

        ## this also works!!!
        btn = QPushButton('download', self)
        btn.move(200, 120)
        btn.clicked.connect(self.download)
        # self.progress = QProgressBar(self)
        # self.progress.setGeometry(200,80,250,20)

        # self.btn = QPushButton('download', self)
        # self.btn.move(200, 120)
        # self.btn.clicked.connect(self.download)

        self.show()

    def download(self):
        self.complete = 0

        while self.complete < 100:
            self.complete += 0.0001 # too low value will freez the program
            self.progress.setValue(self.complete)


    def enlarge_window(self, state):
        if state == Qt.Checked:
            self.setGeometry(50,50,1000,600)
        else:
            self.setGeometry(50,50,500,300)

    def close_application(self):
        
        choice = QMessageBox.question(self, 'Message',
        "Are you sure to quit?", QMessageBox.Yes |
        QMessageBox.No, QMessageBox.No)

        if choice == QMessageBox.Yes:
            print('Quit application')
            sys.exit()
        else:
            pass
            

if __name__ == "__main__":

    def run():
        app = QApplication(sys.argv)
        Gui = window()
        sys.exit(app.exec_())

run()
