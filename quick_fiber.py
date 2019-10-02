import time
import serial

ts = []
t0 = time.time()
#ts.append(t0)

ser = serial.Serial('COM1',baudrate=115200,timeout=1.0,parity=serial.PARITY_NONE,stopbits = serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS)
t1 = time.time()
ts.append(t1-t0)

ser.write('I1 1\r'.encode('ascii'))
t2 = time.time()
ts.append(t2-t1)

time.sleep(0.001)
t3 = time.time()
ts.append(t3-t2)

ser.write('I1 2\r'.encode('ascii'))
t4 = time.time()
ts.append(t4-t3)

time.sleep(0.001)
t5 = time.time()
ts.append(t5-t4)

ser.write('I1 1\r'.encode('ascii'))
t6 = time.time()
ts.append(t6-t5)

for i in range(len(ts)):
	print("{0:.5f}".format(ts[i]*1000),end=' ')
