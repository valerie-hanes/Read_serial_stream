# Program: Temp Data Visualizer

**Author:**  Valerie Hanes

**Completed:** May, 2025

**Purpose:**
Read in temperature data from a microcontroller, create and display a coolored contour plot, and save the data as a .csv file. The contour plot will be updated each time new data is read in and will match the physical board. The .csv file will be labeled with the time stamp of the data-read.

## Configuration

**Imported Libraries:**

* numpy 
  * Used to access arrays, nan, and other opperations
* pandas
  * Used to access data frames
* serial
  * Used for serial communication to a microcontroller
* datetime
  * Used to capture the time at which data is read-in
* time
  * Used to run the program for a specified duration of time
* matplotlib.pyplot
  * Used to construct contour plots
* re
  * Used to strip unwanted characters attached to the incoming string of data



