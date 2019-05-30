from __future__ import print_function

import sys

import numpy as np
from matplotlib.figure import Figure
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
# from matplotlib.backends import qt5_compat
# use_pyside = qt5_compat.QT_API == qt5_compat.QT_API_PYSIDE

# if use_pyside:
#     from PySide.QtCore import *
#     from PySide.QtGui import *
# else:
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import random


class window(QMainWindow):
    def __init__(self, width, height, parent=None):
        super(window, self).__init__(parent)
        # QMainWindow.__init__(self, parent)

        self.xpos = 50
        self.ypos = 50
        self.width = width
        self.height = height
        # self.width = 500
        # self height = 300

        self.setGeometry(self.xpos, self.ypos, self.width/2, self.height/2)
        self.setWindowTitle('Test!')

        #self.x, self.y = self.get_data()
        # self.data = self.get_data()
        self.create_main_frame()
        # self.on_draw()


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

        ## to quite ##
        quitAction = QAction('&Exit ', self)
        quitAction.setShortcut('Ctrl+Q')
        quitAction.setStatusTip('Close the window!')
        quitAction.triggered.connect(self.close_application)

        self.statusBar()

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(openFile)
        fileMenu.addAction(saveFile)
        fileMenu.addAction(quitAction)

        test_btn = QPushButton('Test')

        test_btn.resize(test_btn.sizeHint())  # size of the button (width, hight)
        test_btn.move(self.width - 100, self.height - 40)  # location

    def create_main_frame(self):
        self.main_frame = QWidget()

        # self.fig = Figure()
        self.fig = Figure((3.0, 2.0), dpi=100)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
        # self.canvas.setFocusPolicy(Qt.StrongFocus)
        # self.canvas.setFocus()

        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        self.canvas.mpl_connect('key_press_event', self.on_key_press)




        self.btn_plot = QPushButton('Plot')
        self.btn_plot.clicked.connect(self.plot_static)
        self.btn_plot_nxt = QPushButton('Plot next')
        self.btn_plot_nxt.clicked.connect(self.on_draw)
        self.exit_btn = QPushButton('Exit!')
        self.exit_btn.clicked.connect(self.close_application)

        mainHbox = QHBoxLayout()

        self.main_frame.setLayout(mainHbox)
        self.setCentralWidget(self.main_frame)

        vbox = QVBoxLayout()
        vbox.addWidget(self.canvas)  # the matplotlib canvas
        vbox.addWidget(self.mpl_toolbar)

        # vbox.addWidget(self.btn_plot)
        vbox.addWidget(self.btn_plot_nxt)

        # mainHbox = QHBoxLayout()

        # self.main_frame.setLayout(mainHbox)
        # self.setCentralWidget(self.main_frame)

        mainHbox.addLayout(vbox)
        # hbox.addWidget(self.exit_btn)
        mainHbox.addWidget(self.btn_plot)
        # mainHbox.addWidget(self.btn_plot_nxt)
        # mainHbox.addWidget(self.exit_btn)





    def open_file(self):
        name, _ = QFileDialog.getOpenFileName(self, 'Open file')
        # name, _ = QFileDialog.getOpenFileName(self, 'Open file', option=QFileDialog.DontUseNativeDialog)

        print('file name:', name)
        # self.editor()
        # with open(name, 'r') as f:  # this will close the file after use.
            # text = f.read()
            # self.textEdit.setText(text)

    def save_file(self):
        name, _ = QFileDialog.getSaveFileName(self, 'Save file')
        pass


    def get_data(self):
        return [random.random() for i in range(10)]
        # return np.arange(20).reshape([4, 5]).copy() # for imshow

    def plot_static(self):
        self.fig.clear()
        self.axes = self.fig.add_subplot(111)
        self.axes.plot(range(10), 'o-')
        # self.axes.imshow(self.data, interpolation='nearest')
        self.canvas.draw()

    def on_draw(self):
        self.data = self.get_data()
        self.fig.clear() # this will clear the old plot if recalled
        self.axes = self.fig.add_subplot(111)
        self.axes.plot(self.data, 'o-')
        # self.axes.imshow(self.data, interpolation='nearest')
        self.canvas.draw()

    def on_key_press(self, event):
        print('you pressed', event.key)
        # implement the default mpl key press events described at
        # http://matplotlib.org/users/navigation_toolbar.html#navigation-keyboard-shortcuts
        key_press_handler(event, self.canvas, self.mpl_toolbar)

    def close_application(self):

        choice = QMessageBox.question(self, 'Message',
                                      "Are you sure to quit?", QMessageBox.Yes |
                                      QMessageBox.No, QMessageBox.No)

        if choice == QMessageBox.Yes:
            print('Quit application')
            sys.exit()
        else:
            pass


def main():
    app = QApplication(sys.argv)
    screen = app.primaryScreen()
    screen_sz = screen.size()  # returns the current system screen size
    width = screen_sz.width()
    height = screen_sz.height()
    print(screen_sz)
    form = window(width, height)
    form.show()
    app.exec_()

if __name__ == "__main__":
    main()
