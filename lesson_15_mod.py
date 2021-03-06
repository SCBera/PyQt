import sys
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtGui import QIcon, QColor
# from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
# from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QAction, QMessageBox
# from PyQt5.uic.properties import QtGui
# from PyQt5.QtWidgets import QCheckBox, QProgressBar, QComboBox, QLabel, QStyleFactory
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import random

class window(QMainWindow):

    def __init__(self, width, height):
        super(window, self).__init__()

        ### calling figure/plot
        # self.w_plot = PlotCanvas(self, width/5, height/5)
        # self.w_plot.move(10,10)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        # self.setCentralWidget(self.canvas)

        self.toolbar = NavigationToolbar(self.canvas, self)
        # self.canvas.draw()

        ### defining window location and size ###
        self.xpos = 50
        self.ypos = 50
        self.width = width/2
        self.height = height/2

        self.setGeometry(self.xpos, self.ypos, self.width, self.height)
        self.setWindowTitle('Test!')
        self.setWindowIcon(QIcon('pic.png'))

        ## to do somthing extra ##
        extractAction = QAction('&Exit', self)
        extractAction.setShortcut('Ctrl+Q')
        extractAction.setStatusTip('Exit the app')
        extractAction.triggered.connect(self.plot)
        # extractAction.triggered.connect(self.close_application)
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
        openEditor.setShortcut('Ctrl+E')
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

        # extractAction = QAction(QIcon('logo.png'), 'flee the scene', self)
        # extractAction.triggered.connect(self.close_application)

        # self.toolBar = self.addToolBar('extraction')
        # self.toolBar.addAction(extractAction)

        # set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.canvas)
        layout.addWidget(self.canvas)


        self.home()

    def plot(self):
        ''' plot some random stuff '''
        # random data
        data = [random.random() for i in range(10)]

        # instead of ax.hold(False)
        self.figure.clear()

        # create an axis
        ax1 = self.figure.add_subplot(211)
        ax2 = self.figure.add_subplot(212)

        # discards the old graph
        # ax.hold(False) # deprecated, see above

        # plot data
        ax1.plot(data, '*-')
        ax2.plot(data, 'r-')

        # refresh canvas
        self.canvas.draw()

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
        name, _ = QFileDialog.getSaveFileName(self, 'Save file')
        text = self.textEdit.toPlainText()
        with open(name, 'w') as f: # this will close the file after use.
            f.write(text)

    def open_file(self):
        name, _ = QFileDialog.getOpenFileName(self, 'Open file')
        # name, _ = QFileDialog.getOpenFileName(self, 'Open file', option=QFileDialog.DontUseNativeDialog)

        print('file name:', name)
        self.editor()
        with open(name, 'r') as f: # this will close the file after use.
            text = f.read()
            self.textEdit.setText(text)
        

    def home(self): # disabling this line will also works fine!
        btn = QPushButton('quit', self)
        btn.clicked.connect(self.close_application)
        btn.resize(btn.sizeHint())  # size of the button (width, hight)
        btn.move(self.width - 100, self.height - 40)  # location

        checkBox = QCheckBox('Enlarge window', self)
        # checkBox.toggle() # to be checked from the beginning
        checkBox.move(0,50)
        checkBox.stateChanged.connect(self.enlarge_window)

        self.progress = QProgressBar(self)
        self.progress.setGeometry(200,80,250,20)

        # self.btn = QPushButton('download', self)
        # self.btn.move(200, 120)
        # self.btn.clicked.connect(self.download)


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
            self.setGeometry(self.xpos,self.ypos,self.width/1.3,self.height/1.3)
        else:
            self.setGeometry(self.xpos,self.ypos,self.width/2,self.height/2)

    def close_application(self):
        
        choice = QMessageBox.question(self, 'Message',
        "Are you sure to quit?", QMessageBox.Yes |
        QMessageBox.No, QMessageBox.No)

        if choice == QMessageBox.Yes:
            print('Quit application')
            sys.exit()
        else:
            pass
            

# class PlotCanvas(FigureCanvas):

#     def __init__(self, parent=None, width=5, height=4, dpi=100):
#         fig = Figure(figsize=(width, height), dpi=dpi)
#         self.axes = fig.add_subplot(111)

#         FigureCanvas.__init__(self, fig)
#         self.setParent(parent)

#         FigureCanvas.setSizePolicy(self,
#                                    QSizePolicy.Expanding,
#                                    QSizePolicy.Expanding)
#         FigureCanvas.updateGeometry(self)
#         self.plot()

    # def plot1(self):
    #     data = [random.random() for i in range(25)]
    #     ax = self.figure.add_subplot(111)
    #     ax.plot(data, 'r-')
    #     ax.set_title('PyQt Matplotlib Example')
    #     self.draw()


if __name__ == "__main__":

    def run():
        app = QApplication(sys.argv)
        screen = app.primaryScreen()
        screen_sz = screen.size() # returns the current system screen size
        width = screen_sz.width()
        height = screen_sz.height()
        # print(screen_sz)
        Gui = window(width, height)
        sys.exit(app.exec_())

run()
