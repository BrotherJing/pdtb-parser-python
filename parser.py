import json
import os
import math
from implicit import Implicit
import constants
import features
from features import Node
import preprocess

def cmpt(x,y):
	return -cmp(x[1],y[1])

class Parser:
	def __init__(self):
		pass

	def feature_selection(self):
		parse = open(constants.PARSE_PATH)
		data = open(constants.DATA_PATH)

		ptree_features = {}
		dtree_features = {}
		wp_features = {}

		ptree_cnt = 0
		dtree_cnt = 0
		wp_cnt = 0
		level2_cnts = {}
		for level2 in constants.Level_2_types_full:
			level2_cnts[level2]=0

		arr_parse = [json.loads(x) for x in parse][0]#only one line, the key is wsj_xxxx
		arr_data = [json.loads(x) for x in data]#each line is a sentence of arg1,arg2

		parse.close()
		data.close()

		##for all sentences in pdtb-data.json, find the parse tree, dependency tree of its arg1, arg2 in pdtb-parses.json
		for sent in arr_data:
			docID = sent[u'DocID']
			sentID = sent[u'ID']
			if not sent[u'Type']==u'Implicit':#only use implicit relation
				print sentID, docID, 'Not Implicit'
				continue
			parseDoc = arr_parse[docID]
			parseArg1 = None
			parseArg2 = None
			for parse in parseDoc[u'sentences']:
				words_of_parse = parse[u'words']
				pos=[]
				for word in words_of_parse:
					linkers = word[1][u'Linkers']
					if not len(linkers)==0:
						for linker in linkers:
							pos = linker.split('_')
							if pos[0]==u'arg1' and int(pos[1])==sentID:
								parseArg1=parse
							if pos[0]==u'arg2' and int(pos[1])==sentID:
								parseArg2=parse
					if not parseArg1==None and not parseArg2==None:
						break
			if parseArg1 == None or parseArg2 == None:
				print sentID, docID, 'No parse tree'
				continue
			#print sentID, parseArg1[u'words'][0],parseArg2[u'words'][0]
			print sentID, docID
			dtreeFeatures12 = features.getDependencyFeatures(parseArg1,parseArg2)
			pruleFeatures12 = features.getProductionRuleFeatures(parseArg1,parseArg2)
			wpFeatures = features.getWordPairFeatures(parseArg1,parseArg2)

			senses = sent[u'Sense']
			for sense in senses:
				if '.' in sense:
					level2_cnts[sense.split('.')[1]]+=1

			for k in set(pruleFeatures12[0]).union(set(pruleFeatures12[1])):
				feature = k
				if not feature in ptree_features:
					ptree_features[feature]={}
					ptree_cnt+=1
				for sense in senses:
					if '.' in sense:
						sense = sense.split('.')[1]
						if not sense in ptree_features[feature]:
							ptree_features[feature][sense]=0
						ptree_features[feature][sense]+=1

			for k in set(dtreeFeatures12[0]).union(set(dtreeFeatures12[1])):
				feature = k
				if not feature in dtree_features:
					dtree_features[feature]={}
					dtree_cnt+=1
				for sense in senses:
					if '.' in sense:
						sense = sense.split('.')[1]
						if not sense in dtree_features[feature]:
							dtree_features[feature][sense]=0
						dtree_features[feature][sense]+=1

			for k in set(wpFeatures):
				if k not in wp_features:
					wp_features[k]={}
					wp_cnt+=1
				for sense in senses:
					if '.' in sense:
						sense = sense.split('.')[1]
						if not sense in wp_features[k]:
							wp_features[k][sense]=0
						wp_features[k][sense]+=1

		#calculate MI
		total = 0
		ptree_list = []
		dtree_list = []
		wp_list = []
		for level2 in level2_cnts.keys():
			total+=level2_cnts[level2]

		for ptree in ptree_features.keys():
			mi = []
			total_appear=0
			for level2 in ptree_features[ptree].keys():
				total_appear+=ptree_features[ptree][level2]
			if total_appear < 5:# frequency filter
				continue
			for level2 in level2_cnts.keys():
				if not level2 in ptree_features[ptree]:
					continue
				n11 = ptree_features[ptree][level2]
				n01 = level2_cnts[level2]-n11
				n10 = total_appear-n11
				n00 = total-n11-n01-n10
				n1_ = n11+n10
				n0_ = n01+n00
				n_1 = n01+n11
				n_0 = n10+n00
				i=0
				if not n11==0:
					i+=n11*1.0/total*math.log(total*n11*1.0/(n1_*n_1),2)
				if not n01==0:
					i+=n01*1.0/total*math.log(total*n01*1.0/(n0_*n_1),2)
				if not n10==0:
					i+=n10*1.0/total*math.log(total*n10*1.0/(n1_*n_0),2)
				if not n00==0:
					i+=n00*1.0/total*math.log(total*n00*1.0/(n0_*n_0),2)
				mi.append((level2,i))
			
			mi_max = mi[0]
			for i in mi:
				if i[1]>mi_max[1]:
					mi_max=i
			ptree_list.append((ptree,mi_max[1],mi_max[0]))

		for dtree in dtree_features.keys():
			mi = []
			total_appear = 0
			for level2 in dtree_features[dtree].keys():
				total_appear+=dtree_features[dtree][level2]
			if total_appear < 5:# frequency filter
				continue
			for level2 in level2_cnts.keys():
				if not level2 in dtree_features[dtree]:
					continue
				n11 = dtree_features[dtree][level2]
				n01 = level2_cnts[level2]-n11
				n10 = total_appear-n11
				n00 = total-n11-n01-n10
				n1_ = n11+n10
				n0_ = n01+n00
				n_1 = n01+n11
				n_0 = n10+n00
				i=0
				if not n11==0:
					i+=n11*1.0/total*math.log(total*n11*1.0/(n1_*n_1),2)
				if not n01==0:
					i+=n01*1.0/total*math.log(total*n01*1.0/(n0_*n_1),2)
				if not n10==0:
					i+=n10*1.0/total*math.log(total*n10*1.0/(n1_*n_0),2)
				if not n00==0:
					i+=n00*1.0/total*math.log(total*n00*1.0/(n0_*n_0),2)
				mi.append((level2,i))
			
			mi_max = mi[0]
			for i in mi:
				if i[1]>mi_max[1]:
					mi_max=i
			dtree_list.append((dtree,mi_max[1],mi_max[0]))

		for wp in wp_features.keys():
			mi = []
			total_appear = 0
			for level2 in wp_features[wp].keys():
				total_appear+=wp_features[wp][level2]
			if total_appear < 10:# frequency filter
				continue
			for level2 in level2_cnts.keys():
				if not level2 in wp_features[wp]:
					continue
				n11 = wp_features[wp][level2]
				n01 = level2_cnts[level2]-n11
				n10 = total_appear-n11
				n00 = total-n11-n01-n10
				n1_ = n11+n10
				n0_ = n01+n00
				n_1 = n01+n11
				n_0 = n10+n00
				i=0
				if not n11==0:
					i+=n11*1.0/total*math.log(total*n11*1.0/(n1_*n_1),2)
				if not n01==0:
					i+=n01*1.0/total*math.log(total*n01*1.0/(n0_*n_1),2)
				if not n10==0:
					i+=n10*1.0/total*math.log(total*n10*1.0/(n1_*n_0),2)
				if not n00==0:
					i+=n00*1.0/total*math.log(total*n00*1.0/(n0_*n_0),2)
				mi.append((level2,i))

			mi_max = mi[0]
			for i in mi:
				if i[1]>mi_max[1]:
					mi_max=i
			wp_list.append((wp,mi_max[1],mi_max[0]))


		ptree_list.sort(cmpt)
		dtree_list.sort(cmpt)
		wp_list.sort(cmpt)

		ptree_file = open(constants.MI_PTREE_LIST,'w')
		dtree_file = open(constants.MI_DTREE_LIST,'w')
		wp_file = open(constants.MI_WP_LIST,'w')

		for i in range(min(1000,len(ptree_list),len(dtree_list),len(wp_list))):
			ptree_file.write(ptree_list[i][0]+' '+str(ptree_list[i][2])+' '+str(ptree_list[i][1])+'\n')
			dtree_file.write(dtree_list[i][0]+' '+str(dtree_list[i][2])+' '+str(dtree_list[i][1])+'\n')
			wp_file.write(wp_list[i][0]+' '+str(wp_list[i][2])+' '+str(wp_list[i][1])+'\n')

		ptree_file.close()
		dtree_file.close()
		wp_file.close()

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
	#parser.train()
	#parser.predict()
	parser.feature_selection()

