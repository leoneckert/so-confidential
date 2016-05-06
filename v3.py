import mdb
from pprint import pprint
import msgs
import poetryout
import random

mdb.init()

SENT_sentences = mdb.getAllSentences(speaker=1, eng_filter=1)
RECEIVED_sentences = mdb.getAllSentences(speaker=0, eng_filter=1)


SENTdata = mdb.getTrendingWordsAndSentences(SENT_sentences, days_per_segment = 5, num_words = 2, max_sent_length = 40, blacklist_freq = 0.7)
# returns dict with these objects:
	# populated_indeces
	# word_index
	# index_date
	# index_word_sentence
	# index_num_sentences
RECEIVEDdata = mdb.getTrendingWordsAndSentences(RECEIVED_sentences, days_per_segment = 5, num_words = 2, max_sent_length = 40, blacklist_freq = 0.7)
# for s in SENTdata:
# 	print s

# commonIndeces = msgs.getCommonIndeces(RECEIVEDdata["populated_indeces"], SENTdata["populated_indeces"])
# pprint(commonIndeces)

poetryout.generateTimebasedPoetry(SENTdata, RECEIVEDdata, numPeriods = 3, numSentPerPersonPerPeriod = 2)



firstRun = True
while True:
	if firstRun == True or raw_input('\n\nPress enter for another poem...\n\n') == '':
		firstRun = False
		poetryout.generateTimebasedPoetry(SENTdata, RECEIVEDdata, numPeriods = random.choice(range(1,5)), numSentPerPersonPerPeriod = random.choice(range(1,5)))




# for i in range(100):
# 	poetryout.generateTimebasedPoetry(SENTdata, RECEIVEDdata, numPeriods = random.choice(range(1,5)), numSentPerPersonPerPeriod = random.choice(range(1,5)))


