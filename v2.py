import mdb
import msgs

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

