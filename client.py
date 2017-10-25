# gestures = [Zin, Zout, Xin, XOut, Yin, Yout]

import serial, time, pickle
from numpy import array, std, mean, abs
from numpy.random import randint
from numpy import zeros, array, argmax
import matplotlib.pyplot as plt
import net, tqdm
import numpy as np

WINDOW = 10
MIDDLE = 10
WIDTH = 200

BATCH = 30
EPOCHS = 10000
topology = (90, 6)

def lone_send(data):
	ser = serial.Serial(port='COM5', baudrate=9600, parity=serial.PARITY_ODD, stopbits=serial.STOPBITS_TWO, bytesize=serial.SEVENBITS)
	time.sleep(1)
	ser.write(data)
	ser.close()

def listen(ser=None):
	if ser is None: ser = serial.Serial(port='COM5', baudrate=9600, parity=serial.PARITY_ODD, stopbits=serial.STOPBITS_TWO, bytesize=serial.SEVENBITS)
	_bin = [[], [], []]; data = 0;
	try:
		for j in xrange(0, WIDTH):
			raw = ser.readline()[:-2]
			if raw: 
				raw = raw.split(' ')
				_bin[0].append(float(raw[0]))
				_bin[1].append(float(raw[1]))
				_bin[2].append(float(raw[2]))
		return _bin
	except Exception as e:
		ser.close()
		print "pipe closed, accumulated: "+str(len(_bin[0]))+" "+str(data)

def listen1D(ser=None):
	if ser is None: ser = serial.Serial(port='COM5', baudrate=9600, parity=serial.PARITY_ODD, stopbits=serial.STOPBITS_TWO, bytesize=serial.SEVENBITS)
	bins = [[]]; data = 0;
	time.sleep(1)
	try:
		for j in xrange(0, WIDTH):
			raw = ser.readline()[:-2]
			if raw: bins[-1].append(float(raw))
		return bins[-1]
	except KeyboardInterrupt as e:
		ser.close()
		print "pipe closed, accumulated: "+str(len(bins[0]))+" "+str(data)

def search(dataset):
	dataset = array(dataset); samples = []
	_mean, _std = [mean(dataset), std(dataset)]
	hits = [abs(dataset[i] - _mean) > _std for i in range(0, len(dataset))]
	for j in xrange(0, len(dataset)):
		if hits[j]:
			if all(hits[j:j+WINDOW]): samples.append(j+MIDDLE)
			j = j + WINDOW
	return samples

def batches(size, data, num):
	for j in randint(1, len(data)-size, num): yield data[j:j+size]

def wrapper(data):
	NN = net.nn(topology) 
	b=list(batches(BATCH, data, EPOCHS))
	for batch in tqdm.tqdm(b, total=len((b))):
		dnet = [zeros((NN.topology[j], NN.topology[j+1])) for j in xrange(len(NN.topology)-1)]
		dnet.reverse(); dnet = array(dnet)
		dbias = ([zeros(j) for j in NN.topology])
		dbias.reverse(); dbias= array(dbias)	
		for sample in batch:
			outputs = NN.ff(sample[0])
			results = outputs[0]
			_dnet, _dbias = NN.bp(results - sample[1], outputs)
			dnet += _dnet; dbias += _dbias
		NN.update(np.array(dnet)/BATCH, (np.array(dbias)/BATCH))
	return NN

def arrayavg(samples): return int((search(samples)[-1] + search(samples)[0])/2.0)

def invector(samples): return samples[arrayavg(samples)-15:arrayavg(samples)+15]
	
def capture1D():
	ser = serial.Serial(port='COM5', baudrate=9600, parity=serial.PARITY_ODD, stopbits=serial.STOPBITS_TWO, bytesize=serial.SEVENBITS)
	data = []
	for j in xrange(0, 15):
		try:
			x = invector(listen1D(ser))
			data.append([x, [1, 0]])
			print x
		except Exception as e:
			return data
	pickle.dump(data, open("1_"+str(time.time()), mode='w'))
	return data

def capture3D():
	ser = serial.Serial(port='COM5', baudrate=9600, parity=serial.PARITY_ODD, stopbits=serial.STOPBITS_TWO, bytesize=serial.SEVENBITS)
	data = []
	for j in xrange(0, 30):
		try:
			point = []; av = []
			bins = listen(ser)
			for k in xrange(0, 3):
				q = search(bins[k])
				if len(q) > 0:
					av.append(int((q[-1] + q[0])/2.0))		
			average = int(mean(av))
			point.extend(bins[0][average-15:average+15])
			point.extend(bins[1][average-15:average+15])
			point.extend(bins[2][average-15:average+15])
			data.append([point, [0, 1, 0, 0, 0, 0]])
			print bins[0]
			print bins[1]
			print bins[2]
			time.sleep(1)
		except Exception as e:
			print e
			return data
	pickle.dump(data, open("1_"+str(time.time()), mode='w'))
	return data

def go():
	data = capture1D()	
	NN = wrapper(data)
	print "training done"
	while True:
		print "listen for one second"
		print NN.ff(invector(listen()))

def pretty(data):
	fdata = []
	for j in xrange(0, len(data)):
		try:
			print data[j][0][0:30]
			print data[j][0][30:60]
			print data[j][0][60:90]
			if raw_input('loun kya? ') == 'y':
				fdata.append(data[j])
				print 'le liya'
			print str(j+1) + " samples done"	
		except Exception as e:
			return fdata, j
	return fdata

def scan(tdata, NN=None):
	if NN is None: NN = wrapper(tdata)
	while True:
		try:
			print "scanning.."
			data = capture3D()
			print NN.ff(data)
		except Exception as e:
			print "some stupid shit happened. continue"
			continue