import mdb
from pprint import pprint
import msgs
import poetryout
import random

mdb.init()

SENT_sentences = mdb.getAllSentences(speaker=1, eng_filter=1)
RECEIVED_sentences = mdb.getAllSentences(speaker=0, eng_filter=1)


SENTdata = mdb.getTrendingWordsAndSentences(SENT_sentences, days_per_segment = 5, num_words = 2, max_sent_length = 40, blacklist_freq = 0.7)
RECEIVEDdata = mdb.getTrendingWordsAndSentences(RECEIVED_sentences, days_per_segment = 5, num_words = 2, max_sent_length = 40, blacklist_freq = 0.7)
# returns dict with these objects:
	# populated_indeces
	# word_index
	# index_date
	# index_word_sentence
	# index_num_sentences




firstRun = True
while True:
	if firstRun == True or raw_input('\n\nPress enter for another poem...\n\n') == '':
		firstRun = False
		np = random.choice(range(1,3))
		nspppp = random.choice(range(1,3))
		poetryout.generateTimebasedPoetry(SENTdata, RECEIVEDdata, numPeriods = np, numSentPerPersonPerPeriod = nspppp)


