import serial
import os
import datetime
import time
from wlm import *

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





wlm = WavelengthMeter()

#print(wlm.frequency)


#!/usr/bin/python
#
# This file is part of IvPID.
# Copyright (C) 2015 Ivmech Mechatronics Ltd. <bilgi@ivmech.com>
#
# IvPID is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# IvPID is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# title           :PID.py
# description     :python pid controller
# author          :Caner Durmusoglu
# date            :20151218
# version         :0.1
# notes           :
# python_version  :2.7
# ==============================================================================

"""Ivmech PID Controller is simple implementation of a Proportional-Integral-Derivative (PID) Controller in the Python Programming Language.
More information about PID Controller: http://en.wikipedia.org/wiki/PID_controller
"""
import time

class PID:
    """PID Controller
    """

    def __init__(self, P=0.0, I=0.0, D=0.0):

        self.Kp = P
        self.Ki = I
        self.Kd = D

        self.sample_time = 0.01
        self.current_time = time.time()
        self.last_time = self.current_time

        self.clear()

    def clear(self):
        """Clears PID computations and coefficients"""
        self.SetPoint = 375.763266

        self.PTerm = 0.0
        self.ITerm = 0.0
        self.DTerm = 0.0
        self.last_error = 0.0

        # Windup Guard
        self.int_error = 0.0
        self.windup_guard = 20.0

        self.output = 0.0

    def update(self, feedback_value):
        """Calculates PID value for given reference feedback
        .. math::
            u(t) = K_p e(t) + K_i \int_{0}^{t} e(t)dt + K_d {de}/{dt}
        .. figure:: images/pid_1.png
           :align:   center
           Test PID with Kp=1.2, Ki=1, Kd=0.001 (test_pid.py)
        """
        error = self.SetPoint - feedback_value

        self.current_time = time.time()
        delta_time = self.current_time - self.last_time
        delta_error = error - self.last_error

        if (delta_time >= self.sample_time):
            self.PTerm = self.Kp * error
            self.ITerm += error * delta_time

            if (self.ITerm < -self.windup_guard):
                self.ITerm = -self.windup_guard
            elif (self.ITerm > self.windup_guard):
                self.ITerm = self.windup_guard

            self.DTerm = 0.0
            if delta_time > 0:
                self.DTerm = delta_error / delta_time

            # Remember last time and last error for next calculation
            self.last_time = self.current_time
            self.last_error = error

            self.output = self.PTerm + (self.Ki * self.ITerm) + (self.Kd * self.DTerm)

    def setKp(self, proportional_gain):
        """Determines how aggressively the PID reacts to the current error with setting Proportional Gain"""
        self.Kp = proportional_gain

    def setKi(self, integral_gain):
        """Determines how aggressively the PID reacts to the current error with setting Integral Gain"""
        self.Ki = integral_gain

    def setKd(self, derivative_gain):
        """Determines how aggressively the PID reacts to the current error with setting Derivative Gain"""
        self.Kd = derivative_gain

    def setWindup(self, windup):
        """Integral windup, also known as integrator windup or reset windup,
        refers to the situation in a PID feedback controller where
        a large change in setpoint occurs (say a positive change)
        and the integral terms accumulates a significant error
        during the rise (windup), thus overshooting and continuing
        to increase as this accumulated error is unwound
        (offset by errors in the other direction).
        The specific problem is the excess overshooting.
        """
        self.windup_guard = windup

    def setSampleTime(self, sample_time):
        """PID that should be updated at a regular interval.
        Based on a pre-determined sampe time, the PID decides if it should compute or return immediately.
        """
self.sample_time = sample_time



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