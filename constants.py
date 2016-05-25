Level_2_types = ['Asynchronous', 'Synchrony',
        'Cause', 'Pragmatic cause', 
        'Contrast', 'Concession', 
        'Conjunction', 'Instantiation', 'Restatement', 'Alternative', 'List']

Level_2_types_full = ['Asynchronous', 'Synchrony',
        'Cause', 'Pragmatic cause', "Condition" ,"Pragmatic condition",
        'Contrast', 'Concession', "Pragmatic contrast", "Pragmatic concession",
        'Conjunction', 'Instantiation', 'Restatement', 'Alternative', 'List', "Exception"]

#data file
DATA_PATH = 'pdtb-data.json'
PARSE_PATH = 'pdtb-parses.json'
DEV_PATH = 'dev_pdtb.json'

#tmp file
MI_PTREE_LIST = 'tmp/mi_ptree'
MI_DTREE_LIST = 'tmp/mi_dtree'
MI_WP_LIST = 'tmp/mi_wp'
PTREE_DTREE_PATH = 'tmp/pdtb_ptree_dtree.json'
TRAIN_DATA_PATH = 'tmp/pdtb.train'
MODEL_PATH = 'tmp/pdtb.model'
TEST_DATA_PATH = 'tmp/pdtb.test'
EXPECT_DATA_PATH = 'tmp/pdtb.expect'

TMP_DIR = "/tmp/"

CLASSPATH   = ".:../lib/maxent-2.5.2/lib/trove.jar:../lib/maxent-2.5.2/output/maxent-2.5.2.jar:../lib/opennlp-tools-1.3.0/output/opennlp-tools-1.3.0.jar:../lib/opennlp-tools-1.3.0/lib/jwnl-1.3.3.jar"
STANFORD_PARSER = 'lib/stanford-parser-2010-08-20/'

DTREE_MI_PATH = 'data/dtree-mi-Freq5-adj-args-13type.txt'
PRULE_MI_PATH = 'data/rule-mi-Freq5-adj-args-13type-leaf.txt'
WP_MI_PATH = 'data/word-pair-mi-Freq5-adj-args-13type-stemmed.txt'
