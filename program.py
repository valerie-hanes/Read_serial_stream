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
Available Ports
/dev/cu.Bluetooth-Incoming-Port
/dev/cu.usbmodem0010502074221
/dev/cu.usbmodem0010502074223
'''
# get properties from used port
ser = serial.Serial("/dev/cu.usbmodem0010502074221",
        baudrate=19200, 
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=20) 

start = time.time()
i=0
ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
while (time.time()< start+10): #for how long do we want it to run?
#for i  in np.arange(0,5,1): #how many times do we want it to run?



    #read from the microcontroller  (will run forever if there is nothing to read and no timout defined above)
    trash_data = ser.readline()
    data = ser.readline().decode('utf-8',errors = 'ignore').strip().split('\t') # read in the data, stop at an \n, take off junk at the end, split by tab
    t = datetime.time(datetime.now()) # store the time right after the data has been read (for the name of the csv file)
    

    #data = [float(x) for x in data] #turn each string into a float value
    data = [float(ansi_escape.sub('', x).strip()) for x in data ] # clean and turn to floats
    
    for j in np.arange(0,len(data),1):
        if data[j] <= -666.00: #account for a sensor that has died
            data[j] = np.nan
    print(data)        


    #SAVE CSV
    csv_arr = np.array(data) #store the data into an array for saving the csv file
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
    

    
    
