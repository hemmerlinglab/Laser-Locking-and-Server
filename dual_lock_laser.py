import serial
import os
import datetime
import time
from simple_pid import PID
from wlm import *
from Fiber import *
#import matplotlib.pyplot as plt
#import numpy as np
#import numpy
n = 100
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

#initialize the fiber switcher
fib1 = Fiber('COM1')
chans = [1,2]
setpoint_files = ['setpoint.txt','setpoint2.txt']
setpoints = [0,0]
act_values = [0,0]
ard_values = [0,0]
ard_mess = [20482,20481]
print('-'*n)
print('-'*n)
print('        DUAL LASER LOCK')
print('-'*n)
print('        Setpoint files in Z:\\')


#obtaining the setpoints
for i in range(len(chans)):
    file = open("z:\\"+setpoint_files[i], "r")
    setpoints[i] = file.readline().strip()
    file.close()

#offsets = [0,0]
#for i in range(len(chans)):
#    offsets[i] = float(setpoints[i])



#finds the difference between set point and actual point

#diff = abs(pid.setpoint - wlm.frequency)
pids = ['','']
Kps = [-1000,500]
Kis = [-20000,10000]
Kds = [0,0]
#time.sleep(.1)
for i in range(len(chans)):
    print('Ch {}    File: {}    P: {}   I: {}   D: {}'.format(chans[i],setpoint_files[i],Kps[i],Kis[i],Kds[i]))
    pid = PID(Kps[i],Kis[i],Kds[i],setpoints[i],sample_time = 0.01, output_limits = [-10, 10])
    pids[i] = pid
    fib1.setchan(chans[i])
print('-'*n)

### setvars
#freq_mod = 100
    #time.sleep(.2)
#pid.proportional_on_measurement = True
#print(setpoint)
#wlm.Trigger(1)
#time.sleep(.5)
#z = [0,0]
#freqs = [[0]*freq_mod,[0]*freq_mod]
#plt.ion()
#fig = plt.figure(1)
#ax1 = fig.add_subplot(211)
#ax2 = fig.add_subplot(212)
#lin1, = ax1.plot(freqs[0])
#lin2, = ax2.plot(freqs[1])
#lins = [lin1,lin2]
#axs = [ax1,ax2]
#axs[0].set_ylim([offsets[0]-0.01,offsets[0]+0.01])
#axs[1].set_ylim([offsets[1]-0.01,offsets[1]+0.01])
#for k in range(4095):
while True:
#    if j < 1:
        for l in range(len(chans)):
            
            newset = ''
            
            #time.sleep(.1)
            #print(fib1.getchan())
            #time.sleep(.01)
            # m = 0
            # n = 0
            # while n != chans[i]:
            #     try:
            #         n = int(fib1.getchan().split('\r\n')[0].split('>\n')[1])
            #         #print(n.encode())
            #         #n = int(n)

            #     except:
            #         print(n)
            #     if m > 100:
            #         break
            #     #time.sleep(.01)
            #     m += 1
            # Kp and Ki need to be updated live as to ensure the PID does not run out of range
            #time.sleep(.02)

            # reads the setpoint.txt file 
            #file = open("setpoint.txt", "r")
            file = open("z:\\"+setpoint_files[l], "r")
            newset = file.readline().strip()
            file.close()
            try:
                    pids[l].setpoint = float(newset)
            except:
                    pass
                    #print(newset)
            
            
            # obtains the actual frequency value
            fib1.setchan(chans[l-1])
            time.sleep(.03)
            try_trig = wlm.Trigger(3)
            time.sleep(.02) 
            new_freq = wlm.frequency
            time.sleep(.02)
            wlm.Trigger(1)
 #           freqs[l][z[l]] = new_freq
            #time.sleep(.01)
            if new_freq >= 0:
                act_values[l] = new_freq
                control = pids[l](act_values[l])
                #if abs(control) >= 9.9:
                #       pid.Kp = pid.Kp/2
                #       pid.Ki = pid.Ki/2
                
                # converts into a value that the ardunio can actually read (reads in int bits in a range of 0 to 4095)
                ##ard_values[i] = int(4095.0/20 * control + 4095.0/2.0)
                ard_mess[l] =  int(4095.0/20 * control + 4095.0/2.0)*10+chans[l]
                ##for j in range(len(chans)):
                ##    ard_mess = ard_mess + ' ' + str(ard_values[j])
                # ard_value is between 0 and 4095
                #ard_value = 0
                #ard_value = k
                # feeds converted arduino file to the port
                mystr = '{:05d}'.format(ard_mess[l]).encode('utf-8')
                ser.write(mystr) # converts from unicode to bytes
                # fdb = open('debug.txt','w')
                # fdb.write('{} {} {} {}'.format(act_values[0],act_values[1],ard_mess[0],ard_mess[1]))
                # fdb.close()

            elif new_freq == -3.0:
                act_values[l] = 'UNDER     '
            elif new_freq == -4.0:
                act_values[l] = 'OVER      '
            else:
                act_values[l] = 'ERROR     '

        #print("asdasd")
        #print(control)
            for k in range(len(chans)):
                #print('CNTL {}:'.format(chans[k]),ard_values[k],end='  ')
                print('CTL {}:'.format(chans[k]),format(int((ard_mess[k]-chans[k])/10),'04d'),end='  ')
        #print("{0:2.6f}".format(act_value))
        #print(control)
        #print(ard_value)
                print('SET {}:'.format(chans[k]),str(pids[k].setpoint)[:10],end='  ')
                print('ACT {}:'.format(chans[k]),str(act_values[k])[:10],end='  ')
        #print()
            print('            \r',end='')
  #          lins[l].set_ydata(freqs[l])
   #         fig.canvas.draw()
    #        z[l] = (z[l] + 1)%freq_mod
            #time.sleep(0.02)
        time.sleep(0.01)
   # j += 1    

#diff is proportional to the error signal
# which is then proportional to the voltage the pid needs to give out


# Ardunio Range takes in the numbers 0 to 4095 corresponding to the ranges 
# 0.55V to 3.3V, need to convert the difference in the frequency signal
# to a voltage that needs to be applied, this voltage then needs to be
# converted ot bits to send to an ardunio 


        
    
ser.close()
