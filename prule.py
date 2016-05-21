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

def getProductionRuleFeatures(sentence,parseArg1,parseArg2):
	print getPruleFeatures(buildParseTree(parseArg1[u'parsetree']))
	print getPruleFeatures(buildParseTree(parseArg2[u'parsetree']))
