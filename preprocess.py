import constants

def generateTrainData2(self):
	data = open(constants.DATA_PATH2)
	arr_data = [json.load(x) for x in data]
	for sent in arr_data:
		if not sent[u'Type']==u'Implicit':
			continue
		senses = sent[u'Sense']
		text1 = sent[u'Arg1'][u'RawText']
		text2 = sent[u'Arg2'][u'RawText']
		words1 = sent[u'Arg1'][u'Word']
		words2 = sent[u'Arg2'][u'Word']
		
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
	