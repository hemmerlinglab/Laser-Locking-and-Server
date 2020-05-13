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




# wlm.frequency is our frequency variable, and therefore the actual frequency that needs to be changed according to the PID
wlm = WavelengthMeter()

#path = "C:\\Users\\user\\Desktop\\laserlock\\"

#initialize the fiber switcher
fib1 = Fiber('COM1')
chans = [1]
setpoint_files = ['setpoint.txt']
setpoints = [0]
act_values = [0]
ard_values = [0]

print('Setpoint files in Z:\\')
for i in range(len(chans)):
    print('Channel {} is being set off file {}'.format(chans[i],setpoint_files[i]))


#obtaining the setpoints
for i in range(len(chans)):
    file = open("z:\\"+setpoint_files[i], "r")
    setpoints[i] = file.readline().strip()
    file.close()





#finds the difference between set point and actual point

#diff = abs(pid.setpoint - wlm.frequency)
pids = ['']
Kps = [-100]
Kis = [-1000]
time.sleep(.1)

for i in range(len(chans)):
    pid = PID(Kps[i],Kis[i],0.0,setpoints[i],sample_time = 0.01, output_limits = [-10, 10])
    pids[i] = pid
    time.sleep(.2)
#pid.proportional_on_measurement = True
#print(setpoint)


#for k in range(4095):
while True:
        for i in range(len(chans)):
            fib1.setchan(chans[i])
            # Kp and Ki need to be updated live as to ensure the PID does not run out of range


            # reads the setpoint.txt file 
            #file = open("setpoint.txt", "r")
            file = open("z:\\"+setpoint_files[i], "r")
            newset = file.readline().strip()
            file.close()
            try:
                    pids[i].setpoint = float(newset)
            except:
                    print(newset)
            
            
            # obtains the actual frequency value 
            act_values[i] = wlm.frequency
            control = pids[i](act_values[i])
            #if abs(control) >= 9.9:
            #       pid.Kp = pid.Kp/2
            #       pid.Ki = pid.Ki/2
            
            # converts into a value that the ardunio can actually read (reads in int bits in a range of 0 to 4095)
            ##ard_values[i] = int(4095.0/20 * control + 4095.0/2.0)
            ard_mess =  int(4095.0/20 * control + 4095.0/2.0)
            ##for j in range(len(chans)):
            ##    ard_mess = ard_mess + ' ' + str(ard_values[j])
            # ard_value is between 0 and 4095
            #ard_value = 0
            #ard_value = k
            # feeds converted arduino file to the port
            mystr = '{:04d}'.format(ard_mess).encode('utf-8')
            
            ser.write(mystr) # converts from unicode to bytes

        #print("asdasd")
        #print(control)
            for k in range(len(chans)):
                #print('CNTL {}:'.format(chans[k]),ard_values[k],end='  ')
                print('CNTL {}:'.format(chans[k]),ard_mess,end='  ')
        #print("{0:2.6f}".format(act_value))
        #print(control)
        #print(ard_value)
                print('SET {}:'.format(chans[k]),str(pids[k].setpoint)[:10],end='  ')
                print('ACT {}:'.format(chans[k]),str(act_values[k])[:10],end='  ')
        #print()
            print('            \r',end='')
            time.sleep(0.01)
        time.sleep(0.01)
        


#diff is proportional to the error signal
# which is then proportional to the voltage the pid needs to give out


# Ardunio Range takes in the numbers 0 to 4095 corresponding to the ranges 
# 0.55V to 3.3V, need to convert the difference in the frequency signal
# to a voltage that needs to be applied, this voltage then needs to be
# converted ot bits to send to an ardunio 


        
    
ser.close()
