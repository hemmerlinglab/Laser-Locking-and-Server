import numpy as np
import visa
import pylab
import time

class BK_Function_Generator():

	def __init__(self):
            self.v = visa.ResourceManager()
            self.s = self.v.open_resource('USB0::0xF4EC::0xEE38::514L17165::INSTR')
            
	def trigger(self):
            # soft triggers the function generator
            self.s.write("C1:BTWV MTRIG")
		
	def close(self):
		self.s.close()


if __name__ =='__main__':
	test_read = BK_Function_Generator()
	
	#for k in range(10):
	while True:
		#print(k)
		test_read.trigger()
		time.sleep(1)

	test_read.close()
