import sys
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtGui import QIcon, QColor
# from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
# from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QAction, QMessageBox
# from PyQt5.uic.properties import QtGui
# from PyQt5.QtWidgets import QCheckBox, QProgressBar, QComboBox, QLabel, QStyleFactory
import matplotlib.pyplot as plt

class window(QMainWindow):

    def __init__(self):
        super(window, self).__init__()

        ### defining window location and size ###
        self.xpos = 50
        self.ypos = 50
        self.win_width = 500
        self.win_hight = 300

        self.setGeometry(self.xpos, self.ypos, self.win_width, self.win_hight)
        self.setWindowTitle('Test!')
        self.setWindowIcon(QIcon('logo.png'))

        ## to do somthing extra ##
        extractAction = QAction('&Exit', self)
        extractAction.setShortcut('Ctrl+Q')
        extractAction.setStatusTip('Exit the app')
        extractAction.triggered.connect(self.close_application)
        ## to open file ##
        openFile = QAction('&Open file', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open file')
        openFile.triggered.connect(self.open_file)
        ## to save file ##
        saveFile = QAction('&Save file', self)
        saveFile.setShortcut('Ctrl+S')
        saveFile.setStatusTip('Save file')
        saveFile.triggered.connect(self.save_file)

        openEditor = QAction('& Open Editor', self)
        saveFile.setShortcut('Ctrl+E')
        openEditor.triggered.connect(self.editor)
        fontChoice = QAction('&Font', self)
        fontChoice.triggered.connect(self.font_choice)
        fontColor = QAction('&font bg color', self)
        fontColor.triggered.connect(self.color_picker)

        self.statusBar()

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(extractAction)
        fileMenu.addAction(openFile)
        fileMenu.addAction(saveFile)

        fileMenu = mainMenu.addMenu('&Edit')
        fileMenu.addAction(openEditor)
        fileMenu.addAction(fontChoice)
        fileMenu.addAction(fontColor)

        extractAction = QAction(QIcon('logo.png'), 'flee the scene', self)
        extractAction.triggered.connect(self.close_application)

        self.toolBar = self.addToolBar('extraction')
        self.toolBar.addAction(extractAction)


        self.home()

    def color_picker(self):
        color = QColorDialog.getColor()
        # self.styleChoice.setStyleSheet(f'QWidget{background-color: {color.name()}}') not working
        self.styleChoice.setStyleSheet('QWidget{background-color: %s}' % color.name())

    def editor(self):
        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)

    def font_choice(self):
        font, valid = QFontDialog.getFont()
        if valid:
            self.styleChoice.setFont(font)

    def save_file(self):
        pass

    def open_file(self):
        name, _ = QFileDialog.getOpenFileName(self, 'Open file')

        print('file name:', name)
        file_ = open(name, 'r')
        text = file_.read()
        print('file cont:', text)
        # self.editor()
        pass

    def home(self): # disabling this line will also works fine!
        btn = QPushButton('quit', self)
        btn.clicked.connect(self.close_application)
        btn.resize(btn.sizeHint())  # size of the button (width, hight)
        btn.move(self.win_width - 100, self.win_hight - 40)  # location

        checkBox = QCheckBox('Enlarge window', self)
        # checkBox.toggle() # to be checked from the beginning
        checkBox.move(0,50)
        checkBox.stateChanged.connect(self.enlarge_window)

        self.progress = QProgressBar(self)
        self.progress.setGeometry(200,80,250,20)

        self.btn = QPushButton('download', self)
        self.btn.move(200, 120)
        self.btn.clicked.connect(self.download)


        self.styleChoice = QLabel('Windows', self)
        comboBox = QComboBox(self)
        comboBox.addItem('motif')
        comboBox.addItem('Windows')
        comboBox.addItem('cde')
        comboBox.addItem('Plastique')
        comboBox.addItem('Cleanlooks')
        comboBox.addItem('windowsvista')

        comboBox.move(25, 250)
        self.styleChoice.move(25, 150)
        comboBox.activated[str].connect(self.style_choice)

        color = QColor(0,0,0)
        # fontColor = QAction('&font bg color', self)
        # fontColor.triggered.connect(self.color_picker)
        # fileMenu.addAction(fontColor)

        self.show()

    def style_choice(self, text):
        self.styleChoice.setText(text)
        QApplication.setStyle(QStyleFactory.create(text))

    def download(self):
        self.complete = 0

        while self.complete < 100:
            self.complete += 0.0002 # too low value will freez the program
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
