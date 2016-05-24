Level_2_types = ['Asynchronous', 'Synchrony',
        'Cause', 'Pragmatic_cause', 
        'Contrast', 'Concession', 
        'Conjunction', 'Instantiation', 'Restatement', 'Alternative', 'List']

DATA_PATH = 'pdtb-data-small.json'
PARSE_PATH = 'pdtb-parses-small.json'
DEV_PATH = 'dev_pdtb.json'
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
