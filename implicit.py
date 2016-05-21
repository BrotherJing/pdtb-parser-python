import json
import features
import constants
from features import Node
import preprocess

class Implicit:
	def __init__(self,num_prule,num_dtree,num_wp):

		self.features_prule={}
		self.features_dtree={}
		self.features_wp={}

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

	def generateTrainData(self):
		parse = open(constants.PARSE_PATH)
		data = open(constants.DATA_PATH)
		train_data = open(constants.TRAIN_DATA_PATH,'w')

		arr_parse = [json.loads(x) for x in parse][0]#only one line, the key is wsj_xxxx
		arr_data = [json.loads(x) for x in data]#each line is a sentence of arg1,arg2

		##for all sentences in pdtb-data.json, find the parse tree, dependency tree of its arg1, arg2 in pdtb-parse.json
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

			line = ''
			for k in self.features_prule:
				a1 = k in pruleFeatures12[0]
				a2 = k in pruleFeatures12[1]
				if a1:
					line += k+':1 '
				if a2:
					line += k+':2 '
				if a1 and a2:
					line += k+':12 '

			for k in self.features_dtree:
				a1 = k in dtreeFeatures12[0]
				a2 = k in dtreeFeatures12[1]
				if a1:
					line += k+':1 '
				if a2:
					line += k+':2 '
				if a1 and a2:
					line += k+':12 '

			for k in self.features_wp:
				if k in wpFeatures:
					line += k+' '

			senses = sent[u'Sense']
			for sense in senses:
				train_data.write(line+sense+'\n')

		train_data.close()

	def generateTestData(self,size=10):
		cnt=0
		data = open(constants.DEV_PATH)
		test_data = open(constants.TEST_DATA_PATH,'w')
		expect_data = open(constants.EXPECT_DATA_PATH,'w')

		arr_data = [json.loads(x) for x in data]
		for sent in arr_data:
			sid = sent[u'ID']
			if not sent[u'Type']==u'Implicit':
				print sid, 'not implicit'
				continue
			print sid
			if cnt>=size:
				break
			cnt+=1
			senses = sent[u'Sense']
			text1 = sent[u'Arg1'][u'RawText']
			text2 = sent[u'Arg2'][u'RawText']
			words1 = sent[u'Arg1'][u'Word']
			words2 = sent[u'Arg2'][u'Word']
			ptree1,dtree1 = preprocess.parsePtreeDtree(text1)
			ptree2,dtree2 = preprocess.parsePtreeDtree(text2)
			wpFeatures = features.getWordPairFeaturesSimple(words1,words2)

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

			test_data.write(line+'\n')
			print line
			
			expect = ''
			for sense in senses:
				expect+=sense+' '
			expect_data.write(expect[:-1]+'\n')

		test_data.close()
		expect_data.close()

if __name__ == '__main__':
	implicit = Implicit(100,100,500)
	implicit.generateTestData()
