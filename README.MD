# Plotting tool
This tool is intended to allow the quick and easy comparison of logs from the RC Benchmark Dynamometer. 

## Installation:
To install, simply download the codes and run main.py. You will need python3, I use the Anaconda distribution. The code has been developed on windows but should run on linux as well.

If this is your first time with python, I recommend downloading the newest version of Anaconda with python 3.6 from here [here](https://www.continuum.io/downloads). It should include pyqt5 by default. No extra packages are required when using the Anaconda distribution.

If you don't use Anaconda you will have to install all of the required libraries by hand, which may be annoying.


It requires the following libraries:

pyqt4

scipy

numpy (ensure it is the most recent version)

matplotlib .

## First Use:
The main window shows the power consumption of selected combinations. To plot the power consumption (or efficiency), simply select a motor from the list (new motors can be added if you can't find the one you want), a propeller (currently the only propellers selectable are onces for which the data is available) and an aircraft, then click 'Plot'. Multiple motors, propellers and aircraft can be selected for comparison, the plot is cleared by clicking clear plot in the lower right. The aircraft is defined by its drag polar (the drag as a quadratic function of lift), which can be calculated from exported XFLR5 results. To use XFLR5 results, a type 2 analysis must be run (fixed lift) and the resulting polar exported to a csv file. This file can then be read by PropPy. More details on defining an aircraft can be found in the aircraft section.

Battery and atmosphere settings are changed in the settings drop down menu.