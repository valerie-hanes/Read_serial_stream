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

'''
# get properties from used port
ser = serial.Serial("/dev/cu.usbmodem0010502074221",
        baudrate=19200, 
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=20) 

#initate time function
start = time.time()
i=0

#we will get characters we cannot use, re.compile will allow us to strip those from the data
ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

'''
Two options for running the code:
1. (while-loop) For how long do we want it to run?
2. (for-loop) How many times do we want it to run?
'''
while (time.time()< start+10):
#for i in np.arange(0,5,1): 



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

    #CSV SAVE

    #store the data into an array for saving the csv file
    csv_arr = np.array(data) 
    df = pd.DataFrame(csv_arr) # turn to dataframe
    #save the data using the time at which it was read
    df.to_csv(str(t)+'.csv',index=False,header=False)

    #CONTOUR PLOT

    if i==0: #only look at the first contour plot of the loop to save time
        
        contour_arr = (np.array(data)) #store the data into an array for the contour plot
        contour_arr = contour_arr.reshape([10,10]) # change to 10 by 10
        contour_arr = contour_arr[::-1] #flip contour plot array to make it correspond to the plate


        x = np.arange(0,33+(1.0/3.0),(1.0/3.0)+3) #x values in 10 "rows" on a 30 cm board
        y=np.arange(0,33+(1.0/3.0),(1.0/3.0)+3) #y values in 10 "columns" on a 30 cm board
        #print(contour_arr)

        fig, ax = plt.subplots() 
        c = ax.contourf(x,y,contour_arr,levels=1000,cmap='jet') #setting the contour/color of the plot
        plt.colorbar(c,label = 'Temperature ($ \degree$C)') #add color bar to plot
        ax.set_xlabel('$x$-Position (cm)')
        ax.set_ylabel('$y$-Position (cm)')
        plt.show()
        i=9
    

    
    
