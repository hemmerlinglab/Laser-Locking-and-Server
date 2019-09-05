import serial
import os
import datetime
import time
from simple_pid import PID
from wlm import *
from Fiber import *
import curses

n = 100
serial_port  = 'COM8'; #pid lock arduino port

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

wlm = WavelengthMeter()

fib1 = Fiber('COM1')
chans = [1,2]
setpoint_files = ['setpoint.txt','setpoint2.txt']
setpoints = [0,0]
act_values = [0,0]
ard_values = [0,0]
ard_mess = [20482,20481]

###
stdscr = curses.initscr()
curses.nodelay(True)
curses.noecho()
curses.cbreak()
stdscr.keypad(True)
curses.curs_set(0)

scrx = [5,105]
scry = 50
###

# print('-'*n)
# print('-'*n)
# print('        DUAL LASER LOCK')
# print('-'*n)
# print('        Setpoint files in Z:\\')

###
stdscr.addstr(0,0,'-'*n)
stdscr.addstr(1,10,'DUAL LASER LOCK')
stdscr.addstr(2,0,'-'*n)
stdscr.addstr(3,10,'Setpoint files in Z:\\')
###

for i in range(len(chans)):
    file = open("z:\\"+setpoint_files[i], "r")
    setpoints[i] = file.readline().strip()
    file.close()

pids = ['','']
Kps = [-1000,500]
Kis = [-20000,10000]
Kds = [0,0]

for i in range(len(chans)):
    #print('Ch {}    File: {}    P: {}   I: {}   D: {}'.format(chans[i],setpoint_files[i],Kps[i],Kis[i],Kds[i]))
    ###
    stdscr.addstr(i+5,10,'Ch {}    File: {}    P: {}   I: {}   D: {}'.format(chans[i],setpoint_files[i],Kps[i],Kis[i],Kds[i]))
    ###
    pid = PID(Kps[i],Kis[i],Kds[i],setpoints[i],sample_time = 0.01, output_limits = [-10, 10])
    pids[i] = pid
    fib1.setchan(chans[i])
#print('-'*n)
###
stdscr.addstr(10,0,'-'*n)
stdscr.refresh()
NO_KEY_PRESSED = -1
key_pressed = NO_KEY_PRESSED
###

while key_pressed != ord('q'):
    key_pressed = stdscr.getch()
        for l in range(len(chans)):
            
            newset = ''
            
            file = open("z:\\"+setpoint_files[l], "r")
            newset = file.readline().strip()
            file.close()
            try:
                    pids[l].setpoint = float(newset)
            except:
                    pass

            # obtains the actual frequency value
            fib1.setchan(chans[l-1])
            time.sleep(.03)
            try_trig = wlm.Trigger(3)
            time.sleep(.02) 
            new_freq = wlm.frequency
            time.sleep(.02)
            wlm.Trigger(1)

            if new_freq >= 0:
                act_values[l] = new_freq
                control = pids[l](act_values[l])
                ard_mess[l] =  int(4095.0/20 * control + 4095.0/2.0)*10+chans[l]
                mystr = '{:05d}'.format(ard_mess[l]).encode('utf-8')
                ser.write(mystr) # converts from unicode to bytes
                

            elif new_freq == -3.0:
                act_values[l] = 'UNDER     '
            elif new_freq == -4.0:
                act_values[l] = 'OVER      '
            else:
                act_values[l] = 'ERROR     '

        
            # for k in range(len(chans)):
            #     print('CTL {}:'.format(chans[k]),format(int((ard_mess[k]-chans[k])/10),'04d'),end='  ')
            #     print('SET {}:'.format(chans[k]),str(pids[k].setpoint)[:10],end='  ')
            #     print('ACT {}:'.format(chans[k]),str(act_values[k])[:10],end='  ')
            ###
            stdscr.addstr(scry,scrx[l],'CTL {}:'.format(chans[k]),format(int((ard_mess[k]-chans[k])/10),'04d'))
            stdscr.addstr(scry+1,scrx[l],'SET {}:'.format(chans[k]),str(pids[k].setpoint)[:10])
            stdscr.addstr(scry+2,scrx[l],'ACT {}:'.format(chans[k]),str(act_values[k])[:10])
            stdscr.refresh()
            ###

           #print('            \r',end='')
        time.sleep(0.01)
    
ser.close()
###
curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()
###
