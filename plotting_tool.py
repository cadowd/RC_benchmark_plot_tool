# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 15:48:20 2017

@author: lis-15-15
"""

import sys
from PyQt5 import QtCore, QtGui, uic, QtWidgets

import os
from matplotlib.figure import Figure
import itertools
import numpy as np
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
    
import numbers

import data_extraction
 
qtCreatorFile = "./UI/main_window.ui" # Enter file here.
 
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

def get_csv_names(folder):
    #Get names and locations of all suitable data files
    file_names=[]
    for file in os.listdir(folder):
        if file.endswith(".csv"):
#            data_file=os.path.join(folder, file)
            file_name=file.split("/")[-1]
            file_name=file_name.rsplit(".",1)[0]
            file_names.append(file_name)
                
    return file_names

def return_checked_values(listView):
    checked_items=[]
    
    item_model = listView.model()
    for row in range(item_model.rowCount()):
        item = item_model.item(row)
        if item.checkState() == QtCore.Qt.Checked:
            checked_items.append(item.text())
    return checked_items

def test_func(event):
    print('testing')

class main_window(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)

        self.setupUi(self)
        
        fig1 = Figure()
        ax1f1 = fig1.add_subplot(111)
        self.canvas = FigureCanvas(fig1)
        self.layout_plot.addWidget(self.canvas)
        self.toolbar = NavigationToolbar(self.canvas, 
                self, coordinates=True)
#        self.addToolBar(self.toolbar)
#        self.axes=ax1f1
        self.layout_plot.addWidget(self.toolbar)
        self.plot_colors = itertools.cycle(['k', "r", "b", "g", "y", "c","m"])
        self.current_plots = []
        self.current_data = []
        self.current_data_files = []
        self.file_folder="."
        self.pop_list_views(self.file_folder)
        
        self.canvas.mpl_connect('motion_notify_event', lambda event: self.on_plot_hover(event, ax1f1))
        
        #Button functions
        self.pushButton_changeFolder.clicked.connect(self.change_folder)
        
        self.listView_files.clicked.connect(self.load_all_data)
        self.listView_files.clicked.connect(lambda: self.plot(ax1f1))
        
        self.comboBox_xaxis.activated.connect(lambda: self.plot(ax1f1))
        self.comboBox_yaxis.activated.connect(lambda: self.plot(ax1f1))


        
        self.battery={
        'V':14.8, #battery voltage
        'capacity':4800
        }
        
        self.atmosphere={
        'rho':1.20, #
        'mu':1.8e-5, #dynamic viscosity
        'Ta': 25, #Ambient temperature
        }
        
    def pop_list_views(self, folder):
        """
        Function to populate lists with the files found in the folders.
        """

        file_list = QtGui.QStandardItemModel(self.listView_files)
        for name in get_csv_names(folder):
            item = QtGui.QStandardItem(name)
            item.setCheckable(True)
            file_list.appendRow(item)
        self.listView_files.setModel(file_list)

    def pop_combo_box(self):
        """
        Function to populate combo box with keys in csv files.
        """
        existing_items=[self.comboBox_xaxis.itemText(i) for i in range(self.comboBox_xaxis.count())]
        try:
            for i in range(len(self.current_data)):
                for key in self.current_data[i].keys():
    #                print(self.current_data[0][key][0])
                    if not key == "note":
                        test_value=np.nanmax(self.current_data[i][key][0:20])
                        if (isinstance(test_value,numbers.Real) and test_value==test_value 
                            and key not in existing_items): #make sure its a real number and not nan
                            self.comboBox_xaxis.addItem(key)
                            self.comboBox_yaxis.addItem(key)

        except IndexError:
            return
        
    def change_folder(self):
        cwd = os.getcwd()
        new_folder = QtWidgets.QFileDialog.getExistingDirectory(None, 'Select folder for files to plot', 
         cwd, QtWidgets.QFileDialog.ShowDirsOnly)
        
        self.file_folder=new_folder
        self.pop_list_views(new_folder)
        
    def load_all_data(self):
        try:
            load_files=return_checked_values(self.listView_files)
        except Exception:
#            QtWidgets.QMessageBox.warning(self, 'Select a motor, propeller and plane.',
#                                            "The system of interest must be selected (different to being checked).",
#                                            QtWidgets.QMessageBox.Ok)
            return
        for file in load_files:
            if file in self.current_data_files:
                continue
            data_file=self.file_folder+"/" + file + ".csv"
            loaded_data=data_extraction.extract_data(data_file)
            self.current_data.append(loaded_data)
            self.current_data_files.append(file)
        self.pop_combo_box()
        return
            
    def plot(self, axes):
        """
        Function to plot all selected combinations. Please don't be silly and
        try to plot everything, there's better ways to waste your time.
        """
        
        try:
            plot_files=return_checked_values(self.listView_files)
        except Exception:
#            QtWidgets.QMessageBox.warning(self, 'Select a motor, propeller and plane.',
#                                            "The system of interest must be selected (different to being checked).",
#                                            QtWidgets.QMessageBox.Ok)
            return
        
#        no_to_plot=0
        plot_list=[]
        xkey=self.comboBox_xaxis.currentText()
        ykey=self.comboBox_yaxis.currentText()
        axes.clear()
        self.plot_colors = itertools.cycle(['k', "r", "b", "g", "y", "c","m"])
        for file in plot_files:
            c=next(self.plot_colors)

            try:
                data_key=self.current_data_files.index(file)
            except ValueError:
                QtWidgets.QMessageBox.warning(self, 'Data not loaded.',
                                                "For some reason the selected data has failed to load.",
                                                QtWidgets.QMessageBox.Ok)
                continue
            
            data=self.current_data[data_key]
            
            if xkey in data.keys():
                X=data[xkey]
            else:
                QtWidgets.QMessageBox.warning(self, "Error loading data",
                                                '{} in {} unable to be loaded, ensure the column exists in the data file.'.format(
                        xkey, file),
                                                QtWidgets.QMessageBox.Ok)
                continue
            
            
            if ykey in data.keys():
                Y=data[ykey]
            else:
                QtWidgets.QMessageBox.warning(self, "Error loading data",
                                                '{} in {} unable to be loaded, ensure the column exists in the data file.'.format(
                        ykey, file),
                                                QtWidgets.QMessageBox.Ok)
                continue
            

            y_data=[y for (x,y) in sorted(zip(X,Y))]
            x_data=sorted(X)
            axes.plot(x_data, y_data, label=file, color=c, marker='x', gid=data['note'])
        

        
        axes.legend(loc=4)
        
        axes.set_ylabel(ykey)
        axes.set_xlabel(xkey)
        
        self.canvas.draw() 
        self.pop_combo_box()
        return
        
    def on_plot_hover(self, event, axes):
        for curve in axes.get_lines():
            if curve.contains(event)[0]:
                self.label_notes.setText(curve.get_gid())
    
    def load_data(self, file):
        data_file=self.file_folder+file
        print(data_file)
        loaded_data=data_extraction.extract_data(data_file)
        return loaded_data

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = main_window()
    window.show()
    sys.exit(app.exec_())