import string
import re

class Node:
	def __init__(self,val):
		self.val=val
		self.children=[]

	def addChild(self,child):
		self.children.append(child)

def buildParseTree(treeStr):
	treeStr = treeStr[1:-1].strip()
	if treeStr[0]=='X':#bad parse!!!
		#print 'bad parse!'
		return None
	stack=[]
	i = 0
	while i < len(treeStr):
		if treeStr[i]=='(':
			l=treeStr.find(' ',i)-i
			if l<0:
				l=treeStr.find(')',i)-i-1
				if l==0:
					return Node("")# an empty node!
				print 'parse error'
				return None
			stack.append(Node(treeStr[i+1:i+l]))
			i+=l+1
			continue
		elif treeStr[i]==' ':
			i+=1
		else:# a word
			l=treeStr.find(')',i)-i
			if l<0:
				print 'parse error'
				return None
			top = stack.pop()
			top.addChild(Node(treeStr[i:i+l]))
			stack.append(top)
			i=i+l
			while i<len(treeStr) and treeStr[i]==')':
				i+=1
				if len(stack)==1:
					return stack[0]
				child=stack.pop()
				parent=stack.pop()
				parent.addChild(child)
				stack.append(parent)
			i+=1

def getPruleFeatures(node):
	features=[]
	if node==None:
		return []
	feature=node.val+'_->'
	if len(node.children)==0:
		return []
	for child in node.children:
		feature=feature+'_'+child.val
		features.extend(getPruleFeatures(child))
	features.append(feature)
	return features

def getProductionRuleFeatures(parseArg1,parseArg2):
	return (getPruleFeatures(buildParseTree(parseArg1[u'parsetree'])),
		getPruleFeatures(buildParseTree(parseArg2[u'parsetree'])))

def getProductionRuleFeaturesFromStr(prule):
	return getPruleFeatures(buildParseTree(prule))

##input:
#nsubj(love-2, I-1)
#dobj(love-2, you-3)
def getDependencyFeaturesFromStr(arr):
	depFeature = {}

	for dep in arr:
		search=re.search(r'(.*)\((.*)\,\s*(.*)\)',dep)
		d = search.group(1)
		governor = search.group(2).split('-')[0]
		dependent = search.group(3).split('-')[0]
		#print d,governor,dependent
		if governor == u'ROOT':#ignore ROOT dependency
			continue
		if not governor in depFeature:
			depFeature[governor]=[d]
		else:
			depFeature[governor].append(d)

	arrDepFeature = []

	for k in depFeature.keys():
		feature = k+'_<-'
		for dependency in depFeature[k]:
			feature=feature+'_<'+dependency+'>'
		arrDepFeature.append(feature)

	return arrDepFeature

def getDependencyFeatures(parseArg1,parseArg2):
	
	depFeature1={}
	depFeature2={}

	if u'dependencies' in parseArg1:
		for dependency in parseArg1[u'dependencies']:
			governor = dependency[1].split('-')[0]#the governor
			if governor == u'ROOT':#ignore ROOT dependency
				continue
			if not governor in depFeature1:
				depFeature1[governor]=[dependency[0]]
			else:
				depFeature1[governor].append(dependency[0])

	if u'dependencies' in parseArg2:
		for dependency in parseArg2[u'dependencies']:
			governor = dependency[1].split('-')[0]#the governor
			if governor == u'ROOT':
				continue
			if not governor in depFeature2:
				depFeature2[governor]=[dependency[0]]
			else:
				depFeature2[governor].append(dependency[0])
	
	arrDepFeature1 = []
	arrDepFeature2 = []

	for k in depFeature1.keys():
		feature = k+'_<-'
		for dependency in depFeature1[k]:
			feature=feature+'_<'+dependency+'>'
		arrDepFeature1.append(feature)

	for k in depFeature2.keys():
		feature = k+'_<-'
		for dependency in depFeature2[k]:
			feature=feature+'_<'+dependency+'>'
		arrDepFeature2.append(feature)

	return (arrDepFeature1,arrDepFeature2)

def getWordPairFeatures(parseArg1,parseArg2):
	'''wordPairFeatures = []
	for word1 in parseArg1[u'words']:
		for word2 in parseArg2[u'words']:
			wordPairFeatures.append(word1[0]+'_'+word2[0])
	return wordPairFeatures'''
	return getWordPairFeaturesSimple(parseArg1[u'words'],parseArg2[u'words'])

def getWordPairFeaturesSimple(words1,words2):
	wordPairFeatures = []
	for word1 in words1:
		for word2 in words2:
			wordPairFeatures.append(word1[0]+'_'+word2[0])
	return wordPairFeatures

def getWordPairFeaturesSimple2(words1,words2):
	wordPairFeatures = []
	for word1 in words1:
		for word2 in words2:
			wordPairFeatures.append(word1+'_'+word2)
	return wordPairFeatures
