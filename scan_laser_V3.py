import serial
import os
import datetime
import numpy as np
import time
from wlm import *

# serial port location of the second arduino to control the YAG
serial_port = 'COM9';
baud_rate = 9600; #In arduino, Serial.begin(baud_rate)

try:
    ser = serial.Serial(serial_port, baud_rate, 
                        bytesize=serial.SEVENBITS, 
                        parity=serial.PARITY_ODD, 
                        stopbits=serial.STOPBITS_ONE, 
                        timeout=1)
except:
    try:
        ser.close()
    except:
        print ("Serial port already closed" )
    ser = serial.Serial(serial_port, baud_rate, 
                        bytesize=serial.SEVENBITS, 
                        parity=serial.PARITY_ODD, 
                        stopbits=serial.STOPBITS_ONE, 
                        timeout=1)


# need the wavemeter data, include this class
wlm = WavelengthMeter()

offset = wlm.frequency
scan_array = np.array(range(0,100,10))*1e6/1e12 + offset

for k in range(len(scan_array)):
	print(scan_array[k])
	file = open("setpoint.txt", "w")
	file.write(str(scan_array[k]))
	file.close()
	time.sleep(2.0)
	#time.sleep(2.0)



