import constants
import re
import os
import features

## deprecated
## use the command line version of stanford parser to generate ptree, dtree of one sentence
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

## generate a json file containing ptree, dtree, words of the sentences in the input file.
## use parserhelper.jar
def generatePtreeDtreeFile(input_file):
	if os.path.exists(constants.PTREE_DTREE_PATH):
		return
	
	output_file = '../'+constants.PTREE_DTREE_PATH
	input_file = '../'+input_file
	
	cmd = 'cd parserhelper; java -jar parserhelper.jar '+input_file+' '+output_file
	result = os.popen(cmd)
	while 1:
		line = result.readline()
		if not line: break
		print line
