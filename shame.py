import client, pickle, time
from sklearn.linear_model import SGDClassifier, SGDRegressor#, RandomForestClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn import svm

def do():
	dat = pickle.load(open('./train3'))
	x = [e[0] for e in dat]
	y = [(e[1].index(1) + 1) for e in dat]
	clf = SGDClassifier(loss="hinge", penalty="l2")
	#clf = RandomForestClassifier(max_depth=2, random_state=0)
	#clf = GaussianProcessClassifier(kernel=1.0 * RBF(length_scale=1.,optimizer=None)
	#clf = svm.SVC()
	model = None
	try:
		while True:
			acc = 0.; acc2 = 0.
			model = clf.fit(x, y)
			print "fit done"
			for e in range(0, len(dat)):
				if (model.predict([dat[e][0]]) == y[e]): 
					acc += 1
					if e in range(185, 270):
						acc2 += 1
			print str(acc)+"/"+str(len(dat)) + " samples accurate"
			print str(acc2)+"/"+str(len(range(185, 270))) + " samples accurate X"
			time.sleep(3)
	except KeyboardInterrupt as e:
		return model