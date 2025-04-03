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

#read from the microcontroller  (will run forever if there is nothing to read and no timout defined above)
#data = ser.read()


#SPLIT STRING
#stringlist = data.split(',')
#stringlist = "100,110,15,15,14,12,100,12,12,9,12,12,5,5,4,3,5,5,5,3,4,3,1,2,3,5,4,4,7,5,4,5,4,6,3,100" #delete
#floatlist = [float(x) for x in stringlist]
data = 100,110,15,15,14,12,100,12,12,9,12,12,5,5,4,3,5,5,5,3,4,3,1,2,3,5,4,4,7,5,4,5,4,6,3,100
contour_arr = (np.array(data))
contour_arr.reshape([6,6]) # change to 10 by 10

contour_arr = contour_arr[::-1]

#CONTOUR PLOT
x = np.arange(0,36,6) 
y=np.arange(0,36,6)
print(contour_arr)




#arr = np.array(data)
