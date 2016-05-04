import mdb
import msgs
from pprint import pprint
import poetryout

# msgs.printHeadline();

mdb.init()

# determine size of db
print "\n[+] accessing your chat database."
print "[+] found " + str(mdb.getNumMessages()) + " messages."
# print range of dates
time_range = mdb.getStartEndDate()
print "[+] time range:", msgs.returnDatetime(time_range[0])[:10], "to", msgs.returnDatetime(time_range[1])[:10]
# print "[+] just for fun let me know what your name is..."
# print "[ ] ...", mdb.guessName(), "!"


# find trending words for sent and received
print "[ ] ..."
printTrendingWords = 0
sentTrendingBlacklist = mdb.optimiseTrendingwordsAndBlacklist(sender_id = 1, printing=printTrendingWords)
print "[ ] ..."
receivedTrendingBlacklist = mdb.optimiseTrendingwordsAndBlacklist(sender_id = 0, printing=printTrendingWords)
# print sentTrendingBlacklist['trending']
# print receivedTrendingBlacklist['trending']


# fetch all sentences and text, speaker, person, time
sentSentences = mdb.returnSentences(sender_id = 1)
receivedSentences = mdb.returnSentences(sender_id = 0)

# rate the sentences and bring in order
sentRatedSentences = msgs.rateSentences(sentSentences, sentTrendingBlacklist, maxSentenceLength = 40, sender_id = 1)
receivedRatedSentences = msgs.rateSentences(receivedSentences, receivedTrendingBlacklist, maxSentenceLength = 40, sender_id = 0)
# for i in range(100):
# 	print "SENT:", sentRatedSentences["aRated"][i][0]
# 	# print "RECEIVED:", receivedRatedSentences["aRated"][i][0]
# 	print "-"*50


keeping_track = dict()
keeping_track["words_used"] = set()
keeping_track["sentences_used"] = set()

firstRun = True
while True:
	if firstRun == True or raw_input('\nPress enter for another poem...') == '':
		firstRun = False
		print "\n"
		sentShuffled = msgs.shuffleWithDateAndRating(sentRatedSentences)
		receivedShuffled = msgs.shuffleWithDateAndRating(receivedRatedSentences)
		
		keeping_track = poetryout.generate(sentShuffled, receivedShuffled, sentTrendingBlacklist, receivedTrendingBlacklist, keeping_track)
		# pprint(keeping_track)








