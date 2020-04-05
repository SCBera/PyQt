''' See about section at the end for more details...
taken from: https://matplotlib.org/2.0.2/examples/user_interfaces/embedding_in_qt5.html
modified by Subhas Ch Bera
Date: 2019-06-26
'''

import os
import sys
import pickle
import pandas as pd

import matplotlib as mpl
from matplotlib.figure import Figure
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QIntValidator
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QDialog, QApplication, QMessageBox, QStatusBar, QStyleFactory
from PyQt5.uic import loadUi

### the main window:
class MainWin(QMainWindow):
    """
    This creates the main window and embed matplot canvas for plotting. Also contains many functions.
    """
    # from evaluate_data import* # importing func
    def __init__(self, parent=None):
        super(MainWin, self).__init__(parent) # modified from below
        loadUi('Qt_basic.ui', self)
        # loadUi('Qt_stable.ui', self)
        self.setWindowTitle('MT Data Analyzer')
        self.setWindowIcon(QIcon('logo.png'))
        QApplication.setStyle(QStyleFactory.create('Fusion'))
        # app.aboutToQuit.connect(self.close_application)
        #####################################
        ###### Creating the plot area #######
        #####################################
        self.fig = Figure(figsize=(3.54,2.36), tight_layout=True) # auto size
        # self.fig = Figure((3.0, 2.0), dpi=100) # fixed size
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.MainArea)
        self.canvas.setFocusPolicy(Qt.StrongFocus) # this is to avail the key press event of mpl
        self.canvas.setFocus()  # this is to avail the key press event of mpl
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.MainArea) # create the mpl toolbar
        self.setCentralWidget(self.MainArea) # this actually preserves the area for plot in MainWin
        self.canvas.mpl_connect('button_press_event', self.on_click)
        self.canvas.mpl_connect('key_press_event', self.on_key_press) # mpl keypress events
        # # set plot params as default---
        mpl.rcParams['agg.path.chunksize'] = 100000
        mpl.rcParams['axes.linewidth'] = 1  # set the value globally
        # mpl.rcParams['axes.labelweight'] = 'bold'  # set the value globally
        mpl.rcParams['font.sans-serif'] = 'Arial'  # set the value globally
        mpl.rcParams['font.size'] = 12  # set the value globally
        # mpl.rcParams['font.weight'] = 'bold'  # set the value globally
        mpl.rcParams['xtick.top'] = True  # set the value globally
        mpl.rcParams['xtick.direction'] = 'in'  # set the value globally
        mpl.rcParams['xtick.labelsize'] = 12  # set the value globally
        mpl.rcParams['xtick.major.width'] = 1  # set the value globally
        mpl.rcParams['xtick.major.size'] = 7  # set the value globally
        mpl.rcParams['ytick.right'] = True  # set the value globally
        mpl.rcParams['ytick.direction'] = 'in'  # set the value globally
        mpl.rcParams['ytick.labelsize'] = 12  # set the value globally
        mpl.rcParams['ytick.major.width'] = 1  # set the value globally
        mpl.rcParams['ytick.major.size'] = 7  # set the value globally
        mpl.rcParams['svg.fonttype'] = 'none'  # this works for font edit in AI
        mpl.rcParams['pdf.fonttype'] = 42  # this works for font edit in AI
        # print(mpl.rcParams.keys())
        ###### Adding mpl toolbar and canvas to Layout ######
        self.Frame1VLayout.addWidget(self.mpl_toolbar)
        self.Frame1VLayout.addWidget(self.canvas)

        ###################################
        ######### Menu items  #############
        ###################################
        ## to open file ##
        # self.actionOpen.setShortcut('Ctrl+O') # assinging short cut
        # self.actionOpen.setStatusTip('Open file') # This will show in status bar
        self.actionOpen.triggered.connect(self.open_file) # perform the action by calling the function.
        ## to select file ##
        # self.actionSelect.triggered.connect(self.select_data)
        ## to clear current data ##
        self.actionClear.triggered.connect(self.init_params)
        ## to save file ##
        self.actionSave.triggered.connect(self.save_file)
        ## to quite ##
        self.actionExit.triggered.connect(self.close_application)
        self.actionAbout.triggered.connect(self.about)

        
        ## https://stackoverflow.com/questions/19646185/python-qt-updating-status-bar-during-program-execution
        # self.statusbar = QStatusBar()
        self.statusbar1 = QStatusBar()
        self.statusbar2 = QStatusBar()
        self.statusbar.addPermanentWidget(self.statusbar1) # this allign to the right of stat.bar
        self.statusbar.addPermanentWidget(self.statusbar2) # this allign to the right of stat.bar1
        # self.setStatusBar(self.statusbar)
        self.statusbar.showMessage('Ready for status tips!')
        self.statusbar1.showMessage('Ready!')
        self.statusbar2.showMessage('Ready!')

        ########### Button actions #############
        # self.btn = QPushButton('Open Win2')
        self.OpenBtn.clicked.connect(self.open_file)
        self.SaveDataBtn.clicked.connect(self.save_file)
        self.SaveFigBtn.clicked.connect(self.save_fig)
        self.PlotPrevBtn.clicked.connect(self.plot_prev)
        self.PlotNextBtn.clicked.connect(self.plot_next)
        self.PlotRefreshBtn.clicked.connect(self.call_plots)
        # self.SelectBtn.clicked.connect(self.select_data)
        # self.AnalCPABtn.clicked.connect(self.Analyze_CPA)
        self.ExitBtn.clicked.connect(self.close_application)

        ### Line edits ###
        # self.setRef.textChanged.connect(self.set_ref) # call the func during typing
        self.setYlim.editingFinished.connect(self.set_ylim)

        ### Check boxs ###
        # self.PlotXYcheckBox.clicked.connect(self.call_plots)

        ### Combo Box ####
        ## the search methods
        # self.SearchMethcomboBox.addItem("Binary Segmentation")  #BinSeg
        # self.SearchMethcomboBox.addItem("Bottom-up Segmentation")  # BottomUp
        # self.SearchMethcomboBox.addItem("Pelt")  # Pelt
        # self.SearchMethcomboBox.activated[str].connect(self.algorithm_clicked)
        self.init_params()

    def init_params(self):
        self.data_status = None
        self.plot_no = 0
        self.btm = None
        self.top = None


    def set_ylim(self):
        if self.setYlim.text() == '':
            self.btm = None
            self.top = None
        else:
            lims = self.setYlim.text().split(',')
            try:
                self.btm = float(lims[0])
                self.top = float(lims[1])
            except Exception as err:
                self.error_msg(f'Wrong input: {err}')
        self.call_plots()

    def call_plots(self):
        self.warn_msg('Need to setup suitable method!')
        pass

    def open_file(self):
        path = os.getcwd()
        if os.path.exists(f'{path}\\qtdir.path'):
            with open(f'{path}\\qtdir.path', 'r') as f:
                old_path = f.read()
        else:
            old_path = path
        ### options=QFileDialog.DontUseNativeDialog is required it to work!!!
        name, _ = QFileDialog.getOpenFileName(self, 'Open File', old_path, 
                        '*.txt *.csv *.pickle *.pkl', options=QFileDialog.DontUseNativeDialog)

        ## Not working..
        ### https://stackoverflow.com/questions/53763965/pyqt5-reopen-on-the-same-directory-i-visited
        # name, _ = QFileDialog.getactionOpenName(self, 'Open file', option=QFileDialog.DontUseNativeDialog)
        self.filein = name
        print(name)
        if name:
            new_path = os.path.dirname(name) # this returns the folder path containing the file
            hd, tl = os.path.split(name)
            with open(f'{path}\\qtdir.path', 'w') as f:
                f.write(new_path)
            # QFileDialog().setDirectory(str(dir_)) # not working!!!
            # self.statusbar.showMessage(f'Filename: {name}')
            self.read_data()


    def read_data(self):
        self.warn_msg('Need to setup suitable method!')
        pass



    def check_data(self):
        try:
            if self.filein or self.plot_total > 0:
                self.data_status = 'OK'
                return 'OK'
        except:
            self.error_msg('No data found! Please choose data first.') 

    def plot_next(self): # inherited form Mona
        if self.data_status or self.check_data() == 'OK':
            # Function is called upon when button "Plot Next" is pressed. It updates the plot_no value and calls the plot() function
            # when the end of the dataset is reached, plot_no is restored to initial value. User is also informed.
            if self.plot_no + 1 >= self.plot_total:
                self.warn_msg('This was the last dataset! Now, Will plot from the beginning.')
                self.plot_no = 0
                self.call_plots()
            else:
                self.plot_no += 1
                # plot is called upon with updated ii_plot, such that you will plot the next column in the dataset
                self.call_plots()
                # self.statusbar1.showMessage('Plot # {} on display'.format(self.plot_no + 1))

    def plot_prev(self):
        if self.data_status or self.check_data() == 'OK':
            # Function is called upon when button "Plot Next" is pressed. It updates the plot_no value and calls the plot() function
            # when the end of the dataset is reached, plot_no is restored to initial value. User is also informed.
            if self.plot_no - 1 < 0:
                self.warn_msg('This was the first dataset! Now, Will plot from the END.')
                self.plot_no = self.plot_total - 1
                self.call_plots()
            else:
                self.plot_no -= 1
                # plot is called upon with updated plot_no, such that you will plot the next column in the dataset
                self.call_plots()
                # self.statusbar1.showMessage('Plot # {} on display'.format(self.plot_no + 1))

    def plot_data(self):
        pass


    def save_file(self):
        try:
            path = self.fileout
        except AttributeError:
            path = self.filein
        except:
            self.error_msg('Unable to save file')
        f_out, _ = QFileDialog.getSaveFileName(self, 'Save file', path, '*.txt *.csv *.pickle')
        self.fileout = f_out
        self.statusbar.showMessage(f'Output file name: {f_out}')

        if f_out == '':
            pass
        elif '.txt' in self.fileout:
            pdf = pd.DataFrame(self.save_data)
            pdf.to_csv(path_or_buf=self.fileout, sep='\t', header=True, index=False)
            self.statusbar1.showMessage('Data successfully saved as a txt file!')
        elif '.csv' in self.fileout:
            pdf = pd.DataFrame(self.save_data)
            pdf.to_csv(path_or_buf=self.fileout, sep='\t', header=True, index=False)
            self.statusbar1('Data successfully saved as a csv file!')
        elif '.pkl' in self.fileout or 'pickle' in self.fileout:
            with open(self.fileout, 'wb') as myfile:
                if self.CPAcheckBox.isChecked():
                    pickle.dump(self.save_data_CPA, myfile)
                else:
                    pickle.dump(self.save_data, myfile)
                self.statusbar1.showMessage('Data successfully saved as a pickle file!')
        else:
            self.error_msg('Unable to save! check file format/path!')

    def save_fig(self):
        try:
            path = self.fileout
        except:
            path = self.filein
        f_out, _ = QFileDialog.getSaveFileName(self, 'Save current figure', path,  "Images (*.png *.tiff *.eps *.svg *.jpg)")
        self.fileout = f_out
        if f_out == '':
            pass
        else:
            try:
                if 'eps' in f_out:
                    self.fig.savefig(f_out, format='eps')
                elif 'svg' in f_out:
                    self.fig.savefig(f_out, format='svg')
                else:
                    self.fig.savefig(f_out)
                self.statusbar1.showMessage('Figure successfully saved!')
            except Exception as err:
                self.error_msg(f'Unable to save figure: {err}')


    def update_progressBar(self):
        try:
            done = 100 * (self.plot_no + 1)/ self.plot_total # as plot_no starts at 0.
            # set the value of the progressBarbar to a % of the total dataset
            self.progressBar.setValue(done)
            self.statusbar1.showMessage('Plot # {} on display'.format(self.plot_no + 1))
        except Exception as err:
            self.error_msg(f'Error updating progressBar: {err}')

    def on_click(self, event):
        p = round(event.xdata,2)
        print(p)

    def on_key_press(self, event):
        k = event.key
        if k == 'right':
            # print(f'Pressed {k} key.')
            self.plot_next()
        if k == 'left':
            # print(f'Pressed {k} key.')
            self.plot_prev()
        # implement the default mpl key press events described at
        # http://matplotlib.org/users/navigation_toolbar.html#navigation-keyboard-shortcuts
        key_press_handler(event, self.canvas, self.mpl_toolbar)

    def error_msg(self, txt):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(str(txt)) # str to avoid Value error as it takes str only?!
        # msg.setInformativeText(txt)
        msg.setWindowTitle("Error!")
        msg.exec_()

    def warn_msg(self, txt):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText(str(txt))
        msg.setWindowTitle("Warning!")
        msg.exec_()

    def msg_box(self, msg):
        choice = QMessageBox.question(self, 'Message', msg,
                                      QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        return choice

    def close_application(self):
        choice = QMessageBox.question(self, 'Message',
                                      "Are you sure to quit?", QMessageBox.Yes |
                                      QMessageBox.No, QMessageBox.No)
        if choice == QMessageBox.Yes:
            print('Quit application')
            sys.exit()
        else:
            pass

    def about(self):
        QMessageBox.about(self, "About",
                          """embedding matplot in qt5 an example
        Copyright 2015 BoxControL

        This program is inherited from a simple example of a Qt5 application
        embedding matplotlib canvases. It is base on example from matplolib
        documentation, and initially was developed from Florent Rougon and Darren
        Dale. Modified by Subhas Ch Bera, IZKF, FAU, Germany.

        https://matplotlib.org/2.0.2/examples/user_interfaces/embedding_in_qt5.html

        It may be used and modified with no restriction; raw copies as well as
        modified versions may be distributed without limitation."""
                          )

def run():
    app = QApplication(sys.argv)
    Gui = MainWin()
    Gui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run()
