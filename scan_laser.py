import numpy as np
import time
import datetime
from wlm import *
from ScopeRead import ScopeRead
import csv
import serial
import random

from trigger_fg import *


k40_d2_line = 391.01617003
k40_d1_line = 389.28605716


def get_scan_array(offset, my_min, my_max, no_of_steps):
    # return array with laser frequencies
    # my_min and my_max in MHz
    # offset in THz

    step_size = np.int(np.abs((my_max-my_min))/np.float(no_of_steps))

    return np.array(range(my_min, my_max, step_size))*1e6/1e12 + offset

# parameters
mainpath = "Y:\\Data\\K_Tests\\"
setpoint_filename = 'setpoint.txt'


fg = BK_Function_Generator()

wlm = WavelengthMeter()

offset = k40_d2_line
scan_array = get_scan_array(offset, -1250, 1250, 25)

setpoint_file = open(setpoint_filename, "w")
setpoint_file.write(str(scan_array[0]))
setpoint_file.close()



ahora = datetime.datetime.today().strftime(mainpath+'%Y-%m-%d-%H-%M-%S')

# # file for channel 1
# f1 = open(ahora+'_1.csv','w')
# f1write = csv.writer(f1)

# # file for channel 2
# f2 = open(ahora+'_2.csv','w')
# f2write = csv.writer(f2)

# # file for setpoints
# fs = open(ahora+'_set.csv','w')
# fswrite = csv.writer(fs)

fswrite = open(ahora+'_s.csv','w')
f1write = open(ahora+'_1.csv','w')
f2write = open(ahora+'_2.csv','w')



no_of_averages = 1.0

test_read = ScopeRead()
#test_read.close_scope()



#scan_array = 

#print(scan_array)
random.shuffle(scan_array)
#print(scan_array)
#asd

for k in range(len(scan_array)):

	print("Scan: " + ahora)

	new_set = scan_array[k] 
	print("Set point: " + str(new_set) + " (" + str(k+1) + "/" + str(len(scan_array)) + ")")
	setpoint_file = open("setpoint.txt", "w")
	setpoint_file.write(str(new_set))
	setpoint_file.close()

	time.sleep(3.0)

	hlp1 = []
	hlp2 = []
	n = 0
	
	fswrite.write(str(new_set) + "\n")
	
	for n in range(int(no_of_averages)):
		# soft trigger function generator to fire yag
		print('Firing YAG ...')
		fg.trigger()

		time.sleep(1.0)
		print('Reading scope')
		
		print('Reading Channel 1')
		test_read.read_data_1()
		print('Reading Channel 2')
		test_read.read_data_2()
		print('... done')
		
		# if n == 0:
			# try:
				##print(test_read.ch1_data +'##')
				##print(test_read.ch1_data[:-7])
				# hlp1 = np.array(test_read.ch1_data[:-7].split(','), dtype = np.float)
				##hlp1 = np.array(test_read.ch1_data.split(','), dtype = np.float)
				# try:
					# hlp2 = np.array(test_read.ch2_data[:-7].split(','), dtype = np.float)
				# except:
					# print('Ch2 is a failure')
				# n += 1
			# except:
				# print('n ==0 Read failed... trying again')
		# else:	
			# try:
				# hlp1 = np.add(hlp1, np.array(test_read.ch1_data[:-7].split(','), dtype = np.float))
				# try:
					# hlp2 = np.add(hlp2, np.array(test_read.ch2_data[:-7].split(','), dtype = np.float))
				# except:
					# print('Ch2 is a failure')
				# n += 1
			# except:
				# print('Read failed... trying again')
	
		
			
	#d1 = np.divide(hlp1, no_of_averages)
	#d2 = np.divide(hlp2, no_of_averages)
	#print(d1)
	#print(d2)

		f1write.write(test_read.ch1_data)# + "\n")
		f2write.write(test_read.ch2_data)# + "\n")
			
	#f1write.writerow(d1)
	#f2write.writerow(d2)
	
	#fswrite.writerow([new_set,test_read.ch1_scale,test_read.ch2_scale])

	

	time.sleep(1.0)

test_read.close_scope()

f1write.close()
f2write.close()
fswrite.close()

setpoint_file = open(setpoint_filename, "w")
setpoint_file.write(str(k40_d2_line))
setpoint_file.close()


