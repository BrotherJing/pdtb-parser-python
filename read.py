import json
from dtree import *
from prule import *
from constants import *

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
	#getDependencyFeatures(sent,parseArg1,parseArg2)
	getProductionRuleFeatures(sent,parseArg1,parseArg2)
