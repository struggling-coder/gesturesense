import serial, time, pickle
from numpy import array, std, mean, abs
from numpy.random import randint
from numpy import zeros, array, argmax
import matplotlib.pyplot as plt
import net

WINDOW = 20
MIDDLE = 10
WIDTH = 1000

BATCH = 0
EPOCHS = 0
topology = (29, 2)

def lone_send(data):
	ser = serial.Serial(port='COM5', baudrate=9600, parity=serial.PARITY_ODD, stopbits=serial.STOPBITS_TWO, bytesize=serial.SEVENBITS)
	time.sleep(1)
	ser.write(data)
	ser.close()

def listen(ser=None):
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
	for batch in b: #tqdm.tqdm(b, total=len((b))):
		dnet = [zeros((NN.topology[j], NN.topology[j+1])) for j in xrange(len(NN.topology)-1)]
		dnet.reverse(); dnet = array(dnet)
		dbias = ([zeros(j) for j in NN.topology])
		dbias.reverse(); dbias= array(dbias)	
		for sample in batch:
			outputs = NN.ff(sample[0])
			results = outputs[0]
			_dnet, _dbias = NN.bp((results - sample[1], outputs))
			dnet += _dnet; dbias += _dbias
		NN.update(np.array(dnet)/BATCH, (np.array(dbias)/BATCH))
	return NN

def arrayavg(samples):
	return int((search(samples)[-1] + search(samples)[0])/2.0)

def invector(samples):
	return samples[arrayavg(samples)-15:arrayavg(samples)+14]
	
def capture1D():
	ser = serial.Serial(port='COM5', baudrate=9600, parity=serial.PARITY_ODD, stopbits=serial.STOPBITS_TWO, bytesize=serial.SEVENBITS)
	data = []
	for j in xrange(0, 15):
		try:
			data.append([invector(listen(ser)), [1, 0]])
		except Exception as e:
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
