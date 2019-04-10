import numpy as np
import time
import datetime
from wlm import *
from ScopeRead import ScopeRead
import csv
import serial

from trigger_fg import *


fg = BK_Function_Generator()

wlm = WavelengthMeter()

offset = 391.016000 - 0.5e-3
scan_array = np.array(range(0,1000,100))*1e6/1e12 + offset

mainpath = "Y:\\Data\\K_Tests\\"

ahora = datetime.datetime.today().strftime(mainpath+'%Y-%m-%d-%H-%M-%S')

# file for channel 1
f1 = open(ahora+'_1.csv','w')
f1write = csv.writer(f1)

# file for channel 2
f2 = open(ahora+'_2.csv','w')
f2write = csv.writer(f2)

# file for setpoints
fs = open(ahora+'_set.csv','w')
fswrite = csv.writer(fs)

for k in range(len(scan_array)):
	new_set = scan_array[k] 
	print(new_set)
	setpoint_file = open("setpoint.txt", "w")
	setpoint_file.write(str(new_set))
	setpoint_file.close()

	time.sleep(3.0)

	# soft trigger function generator to fire yag
	fg.trigger()

	time.sleep(.05)
	print('Reading scope')
	test_read = ScopeRead()
	test_read.read_data_1()
	test_read.read_data_2()
	print('... done')
	d1 = test_read.ch1_data
	d2 = test_read.ch2_data
	#print(d1)
	#print(d2)

	f1write.writerow(d1[:-7].split(','))
	f2write.writerow(d2[:-7].split(','))
	fswrite.writerow([new_set,test_read.ch1_scale,test_read.ch2_scale])

	test_read.close_scope()

	time.sleep(1.0)

f1.close()
f2.close()
fs.close()


