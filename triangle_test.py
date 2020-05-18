import serial
import os
import datetime
import time
from simple_pid import PID
from wlm import *
from Fiber import *
#import numpy

serial_port  = 'COM14'; #pid lock arduino port

baud_rate = 9600; #In arduino, Serial.begin(baud_rate)

#log_file_path = 'Z:\\Dewar_Temperatures\\'

#output_file = open(write_to_file_path, "w+");

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


#finds the difference between set point and actual point

#pid.proportional_on_measurement = True
#print(setpoint)
while True:
    for i in range(409):
        new_cont = "{:05d}".format(i*100+1).encode("utf-8")
        ser.write(new_cont)
        #time.sleep(.1)
        ardin = ser.read(4).decode()
        print('Computer: {}  Arduino: {}'.format(str(i*10),ardin))

#diff is proportional to the error signal
# which is then proportional to the voltage the pid needs to give out


# Ardunio Range takes in the numbers 0 to 4095 corresponding to the ranges 
# 0.55V to 3.3V, need to convert the difference in the frequency signal
# to a voltage that needs to be applied, this voltage then needs to be
# converted ot bits to send to an ardunio 


        
    
ser.close()
