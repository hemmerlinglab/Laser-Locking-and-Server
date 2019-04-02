import numpy as np
import time
from wlm import *

wlm = WavelengthMeter()

offset = wlm.frequency
scan_array = np.array(range(0,100,10))*1e6/1e12 + offset

for k in range(len(scan_array)):
	print(scan_array[k])
	file = open("setpoint.txt", "w")
	file.write(str(scan_array[k]))
	file.close()
	time.sleep(2.0)
	#time.sleep(2.0)



