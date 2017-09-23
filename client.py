import serial, time
from numpy import array, std, mean, abs
import matplotlib.pyplot as plt

WINDOW = 10
MIDDLE = 5
WIDTH = 1000

def lone_send(data):
	ser = serial.Serial(port='COM5', baudrate=9600, parity=serial.PARITY_ODD, stopbits=serial.STOPBITS_TWO, bytesize=serial.SEVENBITS)
	time.sleep(1)
	ser.write(data)

def listen():
	ser = serial.Serial(port='COM5', baudrate=9600, parity=serial.PARITY_ODD, stopbits=serial.STOPBITS_TWO, bytesize=serial.SEVENBITS)
	bins = [[]]; data = 0;
	time.sleep(1)
	try:
		for j in xrange(0, WIDTH):
			raw = ser.readline()[:-2]
			if raw:
				bins[-1].append(float(raw))
		return bins
	except KeyboardInterrupt as e:
		ser.close()
		print "pipe closed, accumulated: "+str(len(bins[0]))+" "+str(data)

def search(dataset):
	dataset = array(dataset), samples = []
	_mean, _std = [mean(dataset), std(dataset)]
	hits = [abs(dataset[i] - _mean) > _std for i in xrange(0, WIDTH)]
	for j in xrange(0, WIDTH):
		if hits(j):
			if all(hits[j:j+WINDOW]): samples.append(hits[j+MIDDLE])
	return samples
