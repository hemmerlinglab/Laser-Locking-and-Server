import numpy as np
import visa
import pylab

class ScopeRead():

	def __init__(self):
		self.v = visa.ResourceManager()
		self.a = self.v.list_resources()
		k=0
		self.s = self.v.open_resource('USB0::0x0699::0x03A1::C030685::INSTR')
		#print(self.s.query('*IDN?'))
		#print('HORIZ SCALE >> ',end='')
		#print(self.s.query('HORizontal:SCAle?'))
		#print('STATE >> ',end='')
		#print(self.s.query('acquire:state?'))


	def read_data_1(self):
		self.ch1_scale = 0.02
		self.s.write("ch1:volts {0}".format(self.ch1_scale)) # Set the data source to the channel
		#print('CH1 STATUS >> ',end='')
		#print(self.s.query("ch1?")) # Set the data source to the channel

		channel = 1
		self.s.write("data:source ch%i" % channel) # Set the data source to the channel

		#print('DATA START >> ',end='')
		#print(self.s.query("data:start?")) #default is 1
		self.s.write("data:stop 1495") #sets last data point
		#print('DATA STOP >> ',end='')
		#print(self.s.query("data:stop?")) #default is 1500?
		#print('GETTING DATA...')

		#print('PREAMBLE >> ',end='')
		#print(self.s.query("wfmpre?"))

		#print('DATA -> ',end='')
		self.ch1_data = self.s.query("curve?")


	def read_data_2(self):
		self.ch2_scale = 2
		self.s.write("ch2:volts %i" % self.ch2_scale) # Set the data source to the channel
		#print('CH2 STATUS >> ',end='')
		#print(self.s.query("ch2?")) # Set the data source to the channel

		channel = 2
		self.s.write("data:source ch%i" % channel) # Set the data source to the channel

		#print('DATA START >> ',end='')
		#print(self.s.query("data:start?")) #default is 1
		self.s.write("data:stop 1495") #sets last data point
		#print('DATA STOP >> ',end='')
		#print(self.s.query("data:stop?")) #default is 1500?
		#print('GETTING DATA...')

		#print('PREAMBLE >> ',end='')
		#print(self.s.query("wfmpre?"))

		#print('DATA -> ',end='')
		self.ch2_data = self.s.query("curve?")


	def close_scope(self):
		self.s.close()


if __name__ =='__main__':
	test_read = ScopeRead()
	test_read.read_data_1()
	test_read.read_data_2()
	print(test_read.ch1_data,test_read.ch1_scale)
	print(test_read.ch2_data,test_read.ch2_scale)
	test_read.close_scope()
