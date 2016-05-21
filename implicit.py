import json
from dtree import *
from prule import *
from constants import *

class Implicit:
	def __init__(self,num_prule,num_dtree,num_wp):

		self.features_prule={}
		self.features_dtree={}
		self.features_wp={}

		prule = open(PRULE_MI_PATH)
		count = 0
		for line in prule.readlines():
			if count >= num_prule: break
			tokens=line.strip().split(' ')
			rule=tokens[0]
			if not rule in self.features_prule:
				self.features_prule[rule]=float(tokens[-1])
				count += 1
		prule.close()

		dtree = open(DTREE_MI_PATH)
		count = 0
		for line in dtree.readlines():
			if count >= num_dtree: break
			tokens=line.strip().split(' ')
			rule=tokens[0]
			if not rule in self.features_dtree:
				self.features_dtree[rule]=float(tokens[-1])
				count += 1
		dtree.close()

		word_pair = open(WP_MI_PATH)
		count = 0
		for line in word_pair.readlines():
			if count >= num_wp: break
			tokens=line.strip().split(' ')
			rule=tokens[0]
			if not rule in self.features_wp:
				self.features_wp[rule]=float(tokens[-1])
				count += 1
		word_pair.close()

		#print self.features_prule
		#print self.features_dtree
		#print self.features_wp

	def generateTrainData(self):
		parse = open(PARSE_PATH)
		data = open(DATA_PATH)

		arr_parse = [json.loads(x) for x in parse][0]#only one line, the key is wsj_xxxx
		arr_data = [json.loads(x) for x in data]#each line is a sentence of arg1,arg2

		##for all sentences in pdtb-data.json, find the parse tree, dependency tree of its arg1, arg2 in pdtb-parse.json
		for sent in arr_data:
			if not sent[u'Type']==u'Implicit':#only use implicit relation
				continue
			docID = sent[u'DocID']
			sentID = sent[u'ID']
			parseDoc = arr_parse[docID]
			parseArg1 = None
			parseArg2 = None
			for parse in parseDoc[u'sentences']:
				words_of_parse = parse[u'words']
				pos=[]
				for word in words_of_parse:
					linkers = word[1][u'Linkers']
					if not len(linkers)==0:
						pos = linkers[0].split('_')
						break
				if len(pos)==0:
					break
				if pos[0]==u'arg1' and int(pos[1])==sentID:
					parseArg1=parse
				if pos[0]==u'arg2' and int(pos[1])==sentID:
					parseArg2=parse
			if parseArg1 == None:
				continue
			#print sentID, parseArg1[u'words'][0],parseArg2[u'words'][0]
			getDependencyFeatures(sent,parseArg1,parseArg2)
			getProductionRuleFeatures(sent,parseArg1,parseArg2)

if __name__ == '__main__':
	Implicit(10,10,10)