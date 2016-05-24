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
		
		file_expect = open(constants.EXPECT_DATA_PATH)
		
		cmd = 'cd eval; java -cp '+constants.CLASSPATH+' Predict -real ../'+constants.TEST_DATA_PATH+' ../'+constants.MODEL_PATH
		print cmd
		result = os.popen(cmd)
		while 1:
			line = result.readline()
			line2 = file_expect.readline()
			if not line or not line2: break
			predict = line.split(' ')[-1].split('.')[1]
			answers = line2.split(' ')
			for answer in answers:
				if predict==answer:
					print "correct!"
			

if __name__=='__main__':
	#Parser().train()
	Parser().predict()
