import numpy as np
import pandas as pd
import serial
from datetime import datetime
import time
import matplotlib.pyplot as plt


# PYSERIAL READ

# use python -m serial.tools.list_ports in terminal to see available ports
# will only bee seen if microcontroller is plugged in
# Available ports will change depending on micorcontroller used:
# /dev/cu.Bluetooth-Incoming-Port
# /dev/cu.usbmodem0010502595781
# /dev/cu.usbmodem0010502595783
ser = serial.Serial("/dev/cu.usbmodem0010502332261",baudrate=115200, 
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1) 

for i  in np.arange(0,5,1):
    #read from the microcontroller  (will run forever if there is nothing to read and no timout defined above)
    data = ser.readline().decode('utf-8').strip().split('\t') # read in the data, stop at an \n, take off junk at the end, split by tab
    t = datetime.time(datetime.now()) # store the time right after the data has been read (for the name of the csv file)
    


    #SPLIT STRING
    #data = "100,110,15,15,14,12,100,12,12,9,12,12,5,5,4,3,5,5,5,3,4,3,1,2,3,5,4,4,7,5,4,5,4,6,3,100" #delete
    #data = data.split(',') #split the string at each comma #delete
    data = [float(x) for x in data] #turn each string into a float value
    
    contour_arr = (np.array(data)) #store the data into an array for the contour plot
    contour_arr = contour_arr.reshape([10,10]) # change to 10 by 10
    contour_arr = contour_arr[::-1] #flip contour plot array to make it correspond to the plate

    #CONTOUR PLOT
    x = np.arange(0,36,6) #x values in intervals of 5 stopping at 30
    y=np.arange(0,36,6) #y values in intervals of 5 stopping at 30
    #print(contour_arr)

    fig, ax = plt.subplots() 
    c = ax.contourf(x,y,contour_arr,levels=1000,cmap='jet') #setting the contour/color of the plot
    plt.colorbar(c,label = 'Temperature ($ \degree$C)') #add color bar to plot
    ax.set_xlabel('$x$-Position (cm)')
    ax.set_ylabel('$y$-Position (cm)')
    

    #SAVE CSV
    csv_arr = np.array(data) #store the data into an array for saving the csv file
    df = pd.DataFrame(csv_arr) # turn to dataframe
    df.to_csv(str(t)+'.csv') #save the data using the time at which it was read
    plt.show()
    time.sleep(2) 
    #plt.close()
    
    
