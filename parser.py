import json
import os
from implicit import Implicit
import constants

class Parser:
	def __init__(self):
		pass

	def train(self):
		obj = Implicit(100,100,500)
		obj.generateTrainData()
		cmd = 'cd eval; java -cp '+constants.CLASSPATH+' CreateModel -real ../'+constants.TRAIN_DATA_PATH
		#print 'Training...'
		print cmd
		result = os.popen(cmd)
		while 1:
			line = result.readline()
			print line
			if not line: break

	def predict(self):
		obj = Implicit(100,100,500)
		obj.generateTestData()
		cmd = 'cd /eval; java -cp '+constants.CLASSPATH+' Predict -real ../'+constants.TEST_DATA_PATH+'../'+constants.MODEL_PATH
        print cmd
        result = os.popen(cmd)
		while 1:
			line = result.readline()
			print line
			if not line: break
			

if __name__=='__main__':
	#Parser().train()
	Parser().predict()