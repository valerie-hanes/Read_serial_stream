'''
Program: Temp Data Visualizer

Read in temperature data from a microcontroller, 
create and display a coolored contour plot, and 
save the data as a .csv file
'''

#import libraries
import numpy as np
import pandas as pd
import serial
from datetime import datetime
import time
import matplotlib.pyplot as plt
import re


# PYSERIAL READ

# use python -m serial.tools.list_ports in terminal to see available ports
# will only bee seen if microcontroller is plugged in
# Available ports will change depending on micorcontroller used:
'''
Available Ports:


# get properties from used port
ser = serial.Serial("/dev/cu.usbmodem0010502074221",
        baudrate=19200, 
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=20) 
'''
#initate time function
start = time.time()
#define variables
num_plots = 0
num_files = 0
#we will get characters we cannot use, re.compile will allow us to strip those from the data
ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

'''
Running the code:
1. (while-loop) For how long do we want it to run?
'''
while (time.time()< start+10):

    '''    
    #read from the microcontroller 
    trash_data = ser.readline() #read to the next endline to ensure data is not cut off
    data = ser.readline().decode('utf-8',errors = 'ignore').strip().split('\t') # read in the data, stop at an \n, take off junk at the end, split by tab
    t = datetime.time(datetime.now()) # store the time right after the data has been read (for the name of the csv file)
    

    # clean using re.compile from above and turn each entry into a float value
    data = [float(ansi_escape.sub('', x).strip()) for x in data ] 
    
    #check if any of the temp sensors have died/are not working
    for j in np.arange(0,len(data),1):
        if data[j] <= -666.00: #microcontroller is coded to send -666 if sensor is dead
            data[j] = np.nan
    print(data)        
    '''
    #CSV SAVE
    #data to work with while not hooked up to the micro controller
    data = [23,23,23,23,23,24,24,24,24,25,
            23,23,23,23,24,24,24,24,24,25,
            23,24,25,25,25,25,25,25,25,26,
            24,24,24,25,25,25,25,25,26,26,
            24,24,24,24,25,25,26,27,27,27,
            25,25,25,26,27,27,27,28,28,28,
            25,25,25,25,25,26,26,26,26,26,
            26,26,26,26,26,27,27,27,28,28,
            26,26,26,26,26,27,27,28,28.1,28,
            27,27,27,27,28,28,29,29,29,30]
    t = datetime.time(datetime.now())

    #do not allow too many files
    if(num_files<20):
        #store the data into an array for saving the csv file
        csv_arr = np.array(data) 
        df = pd.DataFrame(csv_arr) # turn to dataframe
        #save the data using the time at which it was read
        df.to_csv(str(t)+'.csv',index=False,header=False)
        num_files = num_files+1

    #CONTOUR PLOT
    plt.ion() #allow plots to be interactive

    x = np.arange(0,33+(1.0/3.0),(1.0/3.0)+3) #x values in 10 "rows" on a 30 cm board
    y=np.arange(0,33+(1.0/3.0),(1.0/3.0)+3) #y values in 10 "columns" on a 30 cm board
    #print(contour_arr)

    #create the plot once
    if num_plots == 0:
        fig, ax = plt.subplots() 
        ax.set_xlabel('$x$-Position (cm)')
        ax.set_ylabel('$y$-Position (cm)')
        num_plots += 1
        plt.show()

    #remove data from previous read
    for old_data in ax.collections:
        old_data.remove()

    #store the data into a 10 by 10 array corresponding to the plate for the contour plot
    contour_arr = (np.array(data)) 
    contour_arr = contour_arr.reshape([10,10]) 
    contour_arr = contour_arr[::-1] 
    
    #setting the contour/color of the plot
    c = ax.contourf(x,y,contour_arr,levels=1000,cmap='jet') 

    #add color bar to plot
    if num_plots == 1:
        plt.colorbar(c,label = 'Temperature ($ \degree$C)') 
        num_plots += 1

    #draw the updated plot immediatly
    fig.canvas.draw()
    fig.canvas.flush_events()
    


    
    

    
    
