import serial
import os
import datetime
import time
from simple_pid import PID
from wlm import *
from Fiber import *
import curses

def main(stdscr):
    ###
    stdscr.nodelay(True)
    curses.noecho()
    stdscr.keypad(True)
    curses.curs_set(0)
    scrx = [5,35,55]
    scry = 15
    if curses.has_colors:
        curses.start_color()
        curses.init_pair(1,curses.COLOR_WHITE,curses.COLOR_BLUE)
        curses.init_pair(2,curses.COLOR_WHITE,curses.COLOR_RED)
        curses.init_pair(3,curses.COLOR_BLACK,curses.COLOR_GREEN)
    stdscr.addstr(0,0,'Starting...',curses.color_pair(1))
    stdscr.refresh()
   # time.sleep(2)
    ###

    n = 80
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
    time.sleep(2)
    fib1 = Fiber('COM1')
    fib1.setchan(1)
    time.sleep(0.005)
    #chan_chk = fib1.getchan()
    #stdscr.addstr(scry+4,(scrx[1]+scrx[0])//2,chan_chk)
    chans = [1,2,3]
    setpoint_files = ['setpoint.txt','setpoint2.txt','setpoint3.txt']
    setpoints = [0,0,0]
    act_values = [0,0,0]
    ard_values = [0,0,0]
    ard_mess = [20481,20482,20483]
    names = ['DAVOS','ARYA','A LASER']



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
    stdscr.refresh()
    ###

    for i in range(len(chans)):
        file = open("z:\\"+setpoint_files[i], "r")
        setpoints[i] = file.readline().strip()
        file.close()
    pids = ['','','']
    Kps = [100,100,100]
    Kis = [1000,1000,1000]
    Kds = [0,0,0]

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
    stdscr.addstr(scry+10,0,"Press q to quit")
    stdscr.addstr(scry+11,0,"Press 1 for Ch 1")
    stdscr.addstr(scry+12,0,"Press 2 for Ch 2")
    stdscr.addstr(scry+13,0,"Press a for All Chs")
    stdscr.refresh()
    NO_KEY_PRESSED = -1
    key_pressed = NO_KEY_PRESSED
    chan_mode = 0
    stdscr.addstr(scry+5,scrx[1],'ENABLED ',curses.color_pair(3))
    stdscr.addstr(scry+5,scrx[0],'ENABLED ',curses.color_pair(3))
    stdscr.addstr(scry+5,scrx[2],'DISABLED',curses.color_pair(3))

    ###

    try_trig = wlm.Trigger(3)
    #time.sleep(.01)
    new_freq = wlm.frequency

    while key_pressed != ord('q'):
        stdscr.refresh()
        key_pressed = stdscr.getch()
        if key_pressed == ord('1'):
            fib1.setchan(1)
            time.sleep(.1)
            wlm.Trigger(0)
            chan_mode = 1
            stdscr.addstr(scry+5,scrx[0],'ENABLED ',curses.color_pair(3))
            stdscr.addstr(scry+5,scrx[1],'DISABLED',curses.color_pair(2))
            stdscr.addstr(scry+5,scrx[2],'DISABLED',curses.color_pair(2))

        elif key_pressed == ord('2'):
            fib1.setchan(2)
            time.sleep(.1)
            wlm.Trigger(0)
            chan_mode = 2
            stdscr.addstr(scry+5,scrx[1],'ENABLED ',curses.color_pair(3))
            stdscr.addstr(scry+5,scrx[0],'DISABLED',curses.color_pair(2))            
            stdscr.addstr(scry+5,scrx[2],'DISABLED',curses.color_pair(2))

        elif key_pressed == ord('3'):
            fib1.setchan(3)
            time.sleep(.1)
            wlm.Trigger(0)
            chan_mode = 3
            stdscr.addstr(scry+5,scrx[1],'DISABLED',curses.color_pair(2))
            stdscr.addstr(scry+5,scrx[0],'DISABLED',curses.color_pair(2))
            stdscr.addstr(scry+5,scrx[2],'ENABLED ',curses.color_pair(3))


        elif key_pressed == ord('a'):
            chan_mode = 0
            stdscr.addstr(scry+5,scrx[1],'ENABLED ',curses.color_pair(3))
            stdscr.addstr(scry+5,scrx[0],'ENABLED ',curses.color_pair(3))
            stdscr.addstr(scry+5,scrx[2],'ENABLED ',curses.color_pair(3))
        else:
            pass

        if chan_mode == 0:
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
                fib1.setchan(chans[l])
                d = 0
                time.sleep(0.005)
                rawch = fib1.getchan()
                while int(rawch) != chans[l]:
                    #stdscr.addstr(scry+4,(scrx[1]+scrx[0])//2,'Raw: '+str(rawch)+' ')
                    #stdscr.refresh()
                    if d == 1000:
                        break
                    time.sleep(0.001)
                    d += 1
                    rawch = fib1.getchan()

                time.sleep(.03)
                try_trig = wlm.Trigger(3)
                #time.sleep(.01)
                new_freq = wlm.frequency               
                #time.sleep(.01)
                #wlm.Trigger(1)
                #stdscr.addstr(scry+5,(scrx[1]+scrx[0])//2,'Last Delay: '+str(d)+'   ')
                time.sleep(1)

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
                stdscr.addstr(scry-1,scrx[l],names[l],curses.color_pair(1))
                stdscr.addstr(scry,scrx[l],'CTL: '+str(format(int((ard_mess[l]-chans[l])/10),'04d')))
                stdscr.addstr(scry+1,scrx[l],'SET: '+str(pids[l].setpoint)[:10])
                stdscr.addstr(scry+2,scrx[l],'ACT: '+str(act_values[l])[:10])
                stdscr.refresh()
                ###
        else:
            newset = ''
            l = chan_mode-1
            file = open("z:\\"+setpoint_files[l], "r")
            newset = file.readline().strip()
            file.close()
            try:
                    pids[l].setpoint = float(newset)
            except:
                    pass

            # obtains the actual frequency value
            #fib1.setchan(chans[l-1])
            #time.sleep(.01)
            #try_trig = wlm.Trigger(3)
            #time.sleep(.01) 
            new_freq = wlm.frequency
            #time.sleep(.01)
            #wlm.Trigger(1)

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
            stdscr.addstr(scry-1,scrx[l],names[l],curses.color_pair(1))
            stdscr.addstr(scry,scrx[l],'CTL: '+str(format(int((ard_mess[l]-chans[l])/10),'04d')))
            stdscr.addstr(scry+1,scrx[l],'SET: '+str(pids[l].setpoint)[:10])
            stdscr.addstr(scry+2,scrx[l],'ACT: '+str(act_values[l])[:10])
            stdscr.refresh()

               #print('            \r',end='')
        time.sleep(0.001)
        
    wlm.Trigger(0)
    ser.close()


curses.wrapper(main)