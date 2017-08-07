# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 12:24:10 2017

@author: lis-15-15
"""
from collections import defaultdict
import csv
from itertools import islice
import numpy as np
import matplotlib.pyplot as plt

def extract_data(data_file):
    """
    Function to extract the data from a given data file, assumed to be in the RCbenchmark format.
    TO ADD: Check data that it makes sense
    """
    n=0
    data = defaultdict(list)
    with open(data_file, "r", encoding='utf-8') as csvfile:
        '''Pass preamble'''
        data['note']=next(csvfile)
        
        csvfile = islice(csvfile, n, None) #reopen
        reader = csv.DictReader(csvfile, delimiter=',')
        headers = reader.fieldnames
        
        for column in headers:
            data[column]=[]
        for row in reader:
            for column in headers:
                try:
                    data[column].append(float(row[column]))
                except ValueError:
                    data[column].append(float('Nan'))
    
    return data

def on_plot_hover(event):
    for curve in plot.get_lines():
        if curve.contains(event)[0]:
            print ("over %s" % curve.get_gid())

if __name__ == "__main__":
#    fig = plt.figure()
#    plot = fig.add_subplot(111)
#    
#    data_file="../StepsTest_2017-05-23_154333.csv"
#    data=extract_data(data_file)
#    plt.plot(data['Thrust (kgf)'],data['Electrical Power (W)'], label='Aerostar 40A', gid=data['note'])
#    
#    print(data['note'])
#    fig.canvas.mpl_connect('motion_notify_event', on_plot_hover)  
#    plt.show()