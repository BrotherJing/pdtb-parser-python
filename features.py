import string

class Node:
	def __init__(self,val):
		self.val=val
		self.children=[]

	def addChild(self,child):
		self.children.append(child)

def buildParseTree(treeStr):
	treeStr = treeStr[1:-1].strip()
	stack=[]
	i = 0
	while i < len(treeStr):
		if treeStr[i]=='(':
			l=treeStr.find(' ',i)-i
			if l<0:
				print 'parse error'
				return None
			stack.append(Node(treeStr[i+1:i+l]))
			i+=l+1
			continue
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

def getDependencyFeatures(parseArg1,parseArg2):
	
	depFeature1={}
	depFeature2={}

	for dependency in parseArg1[u'dependencies']:
		governor = dependency[1].split('-')[0]#the governor
		if governor == u'ROOT':#ignore ROOT dependency
			continue
		if not governor in depFeature1:
			depFeature1[governor]=[dependency[0]]
		else:
			depFeature1[governor].append(dependency[0])

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
	wordPairFeatures = []
	for word1 in parseArg1[u'words']:
		for word2 in parseArg2[u'words']:
			wordPairFeatures.append(word1[0]+'_'+word2[0])
	return wordPairFeatures