import serial
import os
import datetime
import time
from simple_pid import PID
from wlm import *
#import numpy

serial_port  = 'COM8'; #pid lock arduino port

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




# wlm.frequency is our frequency variable, and therefore the actual frequency that needs to be changed according to the PID
wlm = WavelengthMeter()

#path = "C:\\Users\\user\\Desktop\\laserlock\\"

#obtaining the setpoint
file = open("setpoint.txt", "r")
setpoint = file.readline().strip()
file.close()





#finds the difference between set point and actual point

#diff = abs(pid.setpoint - wlm.frequency)
Kp = 1000.0
Ki = 40000

time.sleep(.1)
pid = PID(Kp,Ki,0.0,setpoint,sample_time = 0.01, output_limits = [-10, 10])
time.sleep(.2)
#pid.proportional_on_measurement = True
print(setpoint)



#for k in range(4095):
while True:

	# Kp and Ki need to be updated live as to ensure the PID does not run out of range


	# reads the setpoint.txt file 
	file = open("setpoint.txt", "r")
	newset = file.readline().strip()
	file.close()
	try:
		pid.setpoint = float(newset)
	except:
		print(newset)
	
	
	# obtains the actual frequency value 
	act_value = wlm.frequency
	control = pid(act_value)
	#if abs(control) >= 9.9:
	#	pid.Kp = pid.Kp/2
	#	pid.Ki = pid.Ki/2
	
	# converts into a value that the ardunio can actually read (reads in int bits in a range of 0 to 4095)
	ard_value = int(4095.0/20 * control + 4095.0/2.0)

	
	# ard_value is between 0 and 4095
	#ard_value = 0
	#ard_value = k
	# feeds converted arduino file to the port
	mystr = "{:04d}".format(ard_value).encode('utf-8')
	
	ser.write(mystr) # converts from unicode to bytes

	#print("asdasd")
	#print(control)
	print(ard_value)
	#print("{0:2.6f}".format(act_value))
	#print(control)
	#print(ard_value)
	print(pid.setpoint)
	print(act_value)
	print()
	time.sleep(0.01)
	


#diff is proportional to the error signal
# which is then proportional to the voltage the pid needs to give out


# Ardunio Range takes in the numbers 0 to 4095 corresponding to the ranges 
# 0.55V to 3.3V, need to convert the difference in the frequency signal
# to a voltage that needs to be applied, this voltage then needs to be
# converted ot bits to send to an ardunio 


	
    
ser.close()