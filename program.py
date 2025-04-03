import numpy as np
import pandas as pd
import serial
from datetime import datetime
import time
import matplotlib.pyplot as plt


# PYSERIAL READ

# use python -m serial.tools.list_ports in terminal to see available ports
# will only bee seen if microcontroller is plugged in
# Available ports:
# /dev/cu.Bluetooth-Incoming-Port
# /dev/cu.usbmodem0010502595781
# /dev/cu.usbmodem0010502595783
ser = serial.Serial("/dev/tty.usbmodem0010502595781") # can add timeout = argument 

for i  in np.arange(0,5,1):
    #read from the microcontroller  (will run forever if there is nothing to read and no timout defined above)
    #data = ser.read()
    t = datetime.time(datetime.now())
    


    #SPLIT STRING
    data = "100,110,15,15,14,12,100,12,12,9,12,12,5,5,4,3,5,5,5,3,4,3,1,2,3,5,4,4,7,5,4,5,4,6,3,100" #delete
    data = data.split(',')
    data = [float(x) for x in data]
    contour_arr = (np.array(data))
    contour_arr = contour_arr.reshape([6,6]) # change to 10 by 10

    contour_arr = contour_arr[::-1]

    #CONTOUR PLOT
    x = np.arange(0,36,6) 
    y=np.arange(0,36,6)
    #print(contour_arr)

    fig, ax = plt.subplots()
    c = ax.contourf(x,y,contour_arr,levels=1000,cmap='jet')
    plt.colorbar(c,label = 'Temperature ($ \degree$C)')
    ax.set_xlabel('$x$-Position (cm)')
    ax.set_ylabel('$y$-Position (cm)')
    

    #SAVE CSV
    arr = np.array(data)
    df = pd.DataFrame(arr) # turn to dataframe
    df.to_csv(str(t)+'.csv')
    plt.show(block = False)
    time.sleep(2)
    plt.close()
    
    
