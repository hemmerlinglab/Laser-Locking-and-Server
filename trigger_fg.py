import numpy as np
import visa
import pylab
import time

class BK():

	def __init__(self):
		self.v = visa.ResourceManager()
		
		self.s = self.v.open_resource('USB0::0xF4EC::0xEE38::514L17165::INSTR')

		print(self.s.query('*IDN?'))
		#print('HORIZ SCALE >> ',end='')
		#print(self.s.query('HORizontal:SCAle?'))
		#print('STATE >> ',end='')
		#print(self.s.query('acquire:state?'))


	def trigger(self):
		
		#self.s.write("C1:BTWV STATE,OFF")

		self.s.write("C1:BTWV MTRIG")
		

	def close_scope(self):
		self.s.close()


if __name__ =='__main__':
	test_read = BK()
	
	for k in range(10):
		print(k)
		test_read.trigger()
		time.sleep(1)

	test_read.close_scope()
