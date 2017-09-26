from numpy import dot, exp, array, zeros
from numpy.linalg import norm
from numpy.random import random , randn

eta = 0.22

class nn(object):
	"""docstring for NN"""
	def __init__(self, topology):
		self.topology = topology
		self.net = [randn(topology[j], topology[j+1]) for j in xrange(len(topology)-1)]
		self.bias = [zeros(j) for j in topology]
		self.net.reverse(); self.bias.reverse()
		self.net = array(self.net); self.bias = array(self.bias)

	def update(self, dnet, dbias):
		self.net += dnet
		self.bias += dbias

	def ff(self, inputs):
		_outputs = [inputs]; l = len(self.net)
		while l > 0:
			inputs = 1 / (1 + exp(-1*(dot(inputs, self.net[l-1]) + self.bias[l-1])))
			_outputs.append(inputs)
			l -= 1
		_outputs.reverse(); return _outputs

	def bp(self, differences, outputs):
		dnet = [zeros((self.topology[j], self.topology[j+1])) for j in xrange(len(self.topology)-1)]
		dbias = [zeros(j) for j in self.topology]
		dnet.reverse(); dnet = array(dnet);	dbias.reverse(); dbias=array(dbias)
		dstor = differences
		for k in xrange(len(self.net)):
			_l = len(self.net[k][0])
			for i in xrange(len(self.net[k])):
				for j in xrange(_l): dnet[k][i][j] -= eta * dstor[j] * outputs[k+1][i] * self.derivative(outputs[k][j])
			dstor = [sum([dstor[l] * self.net[k][j][l] * self.derivative(outputs[k][l]) for l in xrange(len(outputs[k]))]) for j in xrange(len(outputs[k+1]))]
		return dnet, dbias

	def derivative(self, o): return o * (1 - o)
