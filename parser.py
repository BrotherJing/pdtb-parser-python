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
		preprocess.generatePtreeDtreeFile(constants.TRAIN_PATH,constants.TRAIN_PTREE_DTREE_PATH)
		data = open(constants.TRAIN_PTREE_DTREE_PATH)

		ptree_features = {}
		dtree_features = {}
		wp_features = {}
		firstlast_features = {}

		ptree_cnt = 0
		dtree_cnt = 0
		wp_cnt = 0
		fl_cnt = 0

		level2_cnts = {}
		for level2 in constants.Level_2_types_full:
			level2_cnts[level2]=0

		arr_data = [json.loads(x) for x in data]
		for sent in arr_data:
			sid = sent[u'ID']
			print 'process sentence#'+sid+'\r',
			ptree1 = features.getProductionRuleFeaturesFromStr(sent[u'Arg1'][u'ParseTree'])
			dtree1 = features.getDependencyFeaturesFromStr(sent[u'Arg1'][u'Dependency'])
			ptree2 = features.getProductionRuleFeaturesFromStr(sent[u'Arg2'][u'ParseTree'])
			dtree2 = features.getDependencyFeaturesFromStr(sent[u'Arg2'][u'Dependency'])
			wpFeatures = features.getWordPairFeaturesSimple2(sent[u'Arg1'][u'Lemma'],sent[u'Arg2'][u'Lemma'])

			senses = sent[u'Sense']
			for sense in senses:
				if '.' in sense:
					level2_cnts[sense.split('.')[1]]+=1

			for k in set(ptree1).union(set(ptree2)):
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

			for k in set(dtree1).union(set(dtree2)):
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

			#first-last-first3
			fl_features = []
			if len(sent[u'Arg1'][u'Lemma'])>=3:
				fl_features.append('first31_'+'_'.join(sent[u'Arg1'][u'Lemma'][:3]))
			if len(sent[u'Arg2'][u'Lemma'])>=3:
				fl_features.append('first32_'+'_'.join(sent[u'Arg2'][u'Lemma'][:3]))
			fl_features.append('first1_'+sent[u'Arg1'][u'Lemma'][0])
			fl_features.append('first2_'+sent[u'Arg2'][u'Lemma'][0])
			fl_features.append('first12_'+sent[u'Arg1'][u'Lemma'][0]+'_'+sent[u'Arg2'][u'Lemma'][0])
			fl_features.append('last1_'+sent[u'Arg1'][u'Lemma'][-1])
			fl_features.append('last2_'+sent[u'Arg2'][u'Lemma'][-1])
			fl_features.append('last12_'+sent[u'Arg1'][u'Lemma'][-1]+'_'+sent[u'Arg2'][u'Lemma'][-1])

			for k in fl_features:
				if not k in firstlast_features:
					firstlast_features[k]={}
					fl_cnt+=1
				for sense in senses:
					if '.' in sense:
						sense = sense.split('.')[1]
						if not sense in firstlast_features[k]:
							firstlast_features[k][sense]=0
						firstlast_features[k][sense]+=1

		#calculate MI
		total = 0
		ptree_list = []
		dtree_list = []
		wp_list = []
		fl_list = []

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
			if total_appear < 5:# frequency filter
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

		for fl in firstlast_features.keys():
			mi = []
			total_appear = 0
			for level2 in firstlast_features[fl].keys():
				total_appear+=firstlast_features[fl][level2]
			if total_appear < 5:# frequency filter
				continue
			for level2 in level2_cnts.keys():
				if not level2 in firstlast_features[fl]:
					continue
				n11 = firstlast_features[fl][level2]
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
			fl_list.append((fl,mi_max[1],mi_max[0]))

		ptree_list.sort(cmpt)
		ptree_file = open(constants.MI_PTREE_LIST,'w')
		for i in range(min(1000,len(ptree_list))):
			ptree_file.write(ptree_list[i][0]+' '+str(ptree_list[i][2])+' '+str(ptree_list[i][1])+'\n')
		ptree_file.close()

		dtree_list.sort(cmpt)
		dtree_file = open(constants.MI_DTREE_LIST,'w')
		for i in range(min(1000,len(dtree_list))):
			dtree_file.write(dtree_list[i][0]+' '+str(dtree_list[i][2])+' '+str(dtree_list[i][1])+'\n')
		dtree_file.close()

		wp_list.sort(cmpt)
		wp_file = open(constants.MI_WP_LIST,'w')
		for i in range(min(1000,len(wp_list))):
			wp_file.write(wp_list[i][0]+' '+str(wp_list[i][2])+' '+str(wp_list[i][1])+'\n')
		wp_file.close()

		fl_list.sort(cmpt)
		fl_file = open(constants.MI_FL_LIST,'w')
		for i in range(min(1000,len(fl_list))):
			fl_file.write(fl_list[i][0]+' '+str(fl_list[i][2])+' '+str(fl_list[i][1])+'\n')
		fl_file.close()

		print '\n'

	def train(self):
		if os.path.exists(constants.MODEL_PATH):
			return
		Implicit(250,150,600,200).generateTrainData()
		cmd = 'cd eval; java -cp '+constants.CLASSPATH+' CreateModel -real ../'+constants.TRAIN_DATA_PATH+' 200'
		#print 'Training...'
		print cmd
		os.system(cmd)

	def predict(self):

		correct = 0
		total = 0
		
		Implicit(250,150,600,200).generateTestData()
		
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
	#parser.feature_selection()

