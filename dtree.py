def getDependencyFeatures(sentence,parseArg1,parseArg2):
	depFeature1={}
	depFeature2={}
	for dependency in parseArg1[u'dependencies']:
		governor = dependency[1].split('-')[0]#the governor
		if governor == u'ROOT':
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
	print sentence[u'ID']
	print depFeature1
	print depFeature2
