import json
import os
from implicit import Implicit
import constants

class Parser:
	def __init__(self):
		pass

	def train(self):
		if os.path.exists(constants.MODEL_PATH):
			return
		Implicit(100,100,500).generateTrainData()
		cmd = 'cd eval; java -cp '+constants.CLASSPATH+' CreateModel -real ../'+constants.TRAIN_DATA_PATH
		#print 'Training...'
		print cmd
		os.system(cmd)

	def predict(self):

		correct = 0
		total = 0
		
		Implicit(100,100,500).generateTestData(0)
		
		file_expect = open(constants.EXPECT_DATA_PATH)
		
		cmd = 'cd eval; java -cp '+constants.CLASSPATH+' Predict -real ../'+constants.TEST_DATA_PATH+' ../'+constants.MODEL_PATH
		print cmd
		result = os.popen(cmd)

		while 1:
			line = result.readline()
			line2 = file_expect.readline()
			if not line or not line2: break
			total+=1
			
			predict = line.strip().split(' ')[-1]#level 2 type
			if '.' in predict:
				predict=predict.split('.')[1]
			answers = line2.split(' ')

			for answer in answers:
				if '.' in answer:
					level2 = answer.strip().split('.')[1]
				else:
					level2 = answer.strip()
				print predict,'\t',level2,
				if predict==level2:
					print "\tcorrect!"
					correct+=1
					break
				else:
					print ""
		print "F1 measure(Micro Avg.) = ",(correct*100.0/total),'%'

if __name__=='__main__':
	parser = Parser()
	parser.train()
	parser.predict()

