import constants
import re
import os
import features

def parsePtreeDtree(text):
	filename = constants.TMP_DIR+"temp"
	file_tmp = open(filename,'w')
	file_tmp.write(text)
	file_tmp.close()

	cmd = 'java -cp '+constants.STANFORD_PARSER+'/stanford-parser.jar \
        edu.stanford.nlp.parser.lexparser.LexicalizedParser -sentences newline -retainTmpSubcategories -outputFormat "penn,typedDependencies" \
        -outputFormatOptions "basicDependencies" '+constants.STANFORD_PARSER+'/englishPCFG.ser.gz '+filename+' 2>&1'

	lines=''
	result = os.popen(cmd)
	while 1:
		line = result.readline()
		lines+=line
		if not line: break

	text = re.search(r'Parsing \[.*\n([\s\S]*?)Parsed file:',lines).group(1)
	arr = text.strip().split('\n\n')
	ptree = re.sub(r'\(ROOT\n +','(',arr[0])
	ptree = re.sub(r'\n','',ptree)
	dtree = arr[1].split('\n')
	return (features.getProductionRuleFeaturesFromStr(ptree),features.getDependencyFeaturesFromStr(dtree))

