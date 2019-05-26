import sys

# from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushbtn
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import random
####https://pythonspot.com/pyqt5-matplotlib/

class App(QMainWindow):

    def __init__(self, parent=None):
        super(App, self).__init__(parent)
        self.left = 50
        self.top = 50
        self.title = 'PyQt5 matplotlib example - pythonspot.com'
        self.width = 800
        self.height = 600

        self.canvas = PlotCanvas(self, width=5, height=3)
        self.canvas.move(50, 100)
        self.toolbar = NavigationToolbar(self.canvas, self)



        # layout = QVBoxLayout()
        # layout.addWidget(self.toolbar)
        # layout.addWidget(self.canvas)
        # # layout.addWidget(self.btn)
        # self.setLayout(layout)

        # self.statusBar()

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # m = PlotCanvas(self, width=3, height=2)
        # m.move(50, 50)
        # toolbar = NavigationToolbar(m, self)
        # self.addWidget(toolbar)

        btn = QPushButton('Exit', self)
        btn.setToolTip('This s an example btn')
        btn.clicked.connect(self.close_application)
        btn.move(700, 500)
        btn.resize(btn.sizeHint())
        # btn.resize(140, 100)

        self.show()

    def close_application(self):

        choice = QMessageBox.question(self, 'Message',
                                      "Are you sure to quit?", QMessageBox.Yes |
                                      QMessageBox.No, QMessageBox.No)

        if choice == QMessageBox.Yes:
            print('Quit application')
            sys.exit()
        else:
            pass


class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(211)
        self.axes1 = fig.add_subplot(212)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot()
        # self.toolbar = NavigationToolbar(self.fig)

    def plot(self):
        data = [random.random() for i in range(25)]
        ax = self.figure.add_subplot(211)
        ax.plot(data, 'r-')
        ax1 = self.figure.add_subplot(212)
        ax1.plot(data, 'g-')
        ax.set_title('PyQt Matplotlib Example')
        plt.tight_layout()
        self.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
