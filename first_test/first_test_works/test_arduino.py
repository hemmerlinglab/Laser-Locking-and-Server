import serial
import os
import datetime
import time

serial_port = 'COM8';
baud_rate = 9600; #In arduino, Serial.begin(baud_rate)

    
#log_file_path = 'Z:\\Dewar_Temperatures\\'

#output_file = open(write_to_file_path, "w+");
#
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




#import numpy as np

for k in range(0,4000,125):
	mystr = '{:04d}'.format(k).encode('utf-8')
	
	print(mystr)
	ser.write(mystr)
	#for kk in range(7):
	#	mystr = ser.readline()
	#	print(mystr)
	#print("")
	time.sleep(0.1)

# for k in range(0,4000,500):
	# mystr = "{:04d}".format(k).encode('utf-8')
	
	# ser.write(mystr) # converts from unicode to bytes
	
	#ser.write('100'.encode('utf-8'))
	#time.sleep(0.5)
	#ser.write('900'.encode('utf-8'))
	#time.sleep(0.5)
	#ser.write(k)
	
	# print(mystr)
	# print("No of bytes = " + str(len(mystr)))
	# time.sleep(1.0)
	
#line = line.decode("utf-8") #ser.readline returns a binary, convert to string
    
ser.close()