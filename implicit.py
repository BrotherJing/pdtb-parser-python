import json
import os
import features
import constants
from features import Node
import preprocess

class Implicit:

	def __init__(self,num_prule,num_dtree,num_wp,num_fl):

		self.features_prule={}
		self.features_dtree={}
		self.features_wp={}
		self.features_fl={}

		prule = open(constants.PRULE_MI_PATH)
		count = 0
		for line in prule.readlines():
			if count >= num_prule: break
			tokens=line.strip().split(' ')
			rule=tokens[0]
			if not rule in self.features_prule:
				self.features_prule[rule]=float(tokens[-1])
				count += 1
		prule.close()

		dtree = open(constants.DTREE_MI_PATH)
		count = 0
		for line in dtree.readlines():
			if count >= num_dtree: break
			tokens=line.strip().split(' ')
			rule=tokens[0]
			if not rule in self.features_dtree:
				self.features_dtree[rule]=float(tokens[-1])
				count += 1
		dtree.close()

		word_pair = open(constants.WP_MI_PATH)
		count = 0
		for line in word_pair.readlines():
			if count >= num_wp: break
			tokens=line.strip().split(' ')
			rule=tokens[0]
			if not rule in self.features_wp:
				self.features_wp[rule]=float(tokens[-1])
				count += 1
		word_pair.close()

		fl = open(constants.FL_MI_PATH)
		count = 0
		for line in fl.readlines():
			if count >= num_fl: break
			tokens=line.strip().split(' ')
			rule=tokens[0]
			if not rule in self.features_fl:
				self.features_fl[rule]=float(tokens[-1])
				count += 1
		fl.close()

	#generate training data from the file of sentences, which contains ptree, dtree and word.
	def generateTrainData(self,train_file):
		#preprocess.generatePtreeDtreeFile(constants.TRAIN_PATH,constants.TRAIN_PTREE_DTREE_PATH)
		preprocess.generatePtreeDtreeFile(train_file,constants.TRAIN_PTREE_DTREE_PATH)
		data = open(constants.TRAIN_PTREE_DTREE_PATH)
		
		if os.path.exists(constants.TRAIN_DATA_PATH):
			return

		train_data = open(constants.TRAIN_DATA_PATH,'w')

		arr_data = [json.loads(x) for x in data]
		for sent in arr_data:
			sid = sent[u'ID']
			print "generate train data for sentence#",sid+'\r',
			senses = sent[u'Sense']
			if not sent[u'Type']=='Implicit':
				continue
			ptree1 = features.getProductionRuleFeaturesFromStr(sent[u'Arg1'][u'ParseTree'])
			dtree1 = features.getDependencyFeaturesFromStr(sent[u'Arg1'][u'Dependency'])
			ptree2 = features.getProductionRuleFeaturesFromStr(sent[u'Arg2'][u'ParseTree'])
			dtree2 = features.getDependencyFeaturesFromStr(sent[u'Arg2'][u'Dependency'])
			wpFeatures = features.getWordPairFeaturesSimple2(sent[u'Arg1'][u'Lemma'],sent[u'Arg2'][u'Lemma'])

			line = ''
			for k in self.features_prule:
				a1 = k in ptree1
				a2 = k in ptree2
				if a1:
					line += k+':1 '
				if a2:
					line += k+':2 '
				if a1 and a2:
					line += k+':12 '

			for k in self.features_dtree:
				a1 = k in dtree1
				a2 = k in dtree2
				if a1:
					line += k+':1 '
				if a2:
					line += k+':2 '
				if a1 and a2:
					line += k+':12 '

			for k in self.features_wp:
				if k in wpFeatures:
					line += k+' '

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

			for k in self.features_fl:
				if k in fl_features:
					line += k+' '

			#print line
			for sense in senses:
				train_data.write(line+sense.replace(' ','_')+'\n')#'pragmatic cause' contains space!! replace with '_', recover it later..

		train_data.close()
		print ' '

	#first generate the ptree, dtree of all sentences into a file, then use this file to generate test data
	def generateTestData(self,test_file_path,expect_file_path=''):
		generate_expect_file = not expect_file_path==''
		#preprocess.generatePtreeDtreeFile(constants.DEV_PATH,constants.DEV_PTREE_DTREE_PATH)
		preprocess.generatePtreeDtreeFile(test_file_path,constants.DEV_PTREE_DTREE_PATH)
		data = open(constants.DEV_PTREE_DTREE_PATH)
		
		if os.path.exists(constants.TEST_DATA_PATH) and os.path.exists(constants.EXPECT_DATA_PATH):
			return
		test_data = open(constants.TEST_DATA_PATH,'w')
		if generate_expect_file:
			expect_data = open(constants.EXPECT_DATA_PATH,'w')

		arr_data = [json.loads(x) for x in data]
		for sent in arr_data:
			sid = sent[u'ID']
			print "generate test data for sentence#",sid,'\r',
			senses = sent[u'Sense']
			if not sent[u'Type']=='Implicit':
				continue
			ptree1 = features.getProductionRuleFeaturesFromStr(sent[u'Arg1'][u'ParseTree'])
			dtree1 = features.getDependencyFeaturesFromStr(sent[u'Arg1'][u'Dependency'])
			ptree2 = features.getProductionRuleFeaturesFromStr(sent[u'Arg2'][u'ParseTree'])
			dtree2 = features.getDependencyFeaturesFromStr(sent[u'Arg2'][u'Dependency'])
			wpFeatures = features.getWordPairFeaturesSimple(sent[u'Arg1'][u'Lemma'],sent[u'Arg2'][u'Lemma'])
			
			line = ''
			for k in self.features_prule:
				a1 = k in ptree1
				a2 = k in ptree2
				if a1:
					line += k+':1 '
				if a2:
					line += k+':2 '
				if a1 and a2:
					line += k+':12 '

			for k in self.features_dtree:
				a1 = k in dtree1
				a2 = k in dtree2
				if a1:
					line += k+':1 '
				if a2:
					line += k+':2 '
				if a1 and a2:
					line += k+':12 '

			for k in self.features_wp:
				if k in wpFeatures:
					line += k+' '

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

			for k in self.features_fl:
				if k in fl_features:
					line += k+' '

			test_data.write(line+'\n')
			
			if generate_expect_file:
				expect = ''
				for sense in senses:
					expect+=sense.replace(' ','_')+' '
				expect_data.write(expect[:-1]+'\n')

		test_data.close()

		if generate_expect_file:
			expect_data.close()
		print ''

if __name__ == '__main__':
	implicit = Implicit(100,100,500,100)
	implicit.generateTestData(constants.DEV_PATH)
