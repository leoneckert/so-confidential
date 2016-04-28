import msgs
import mdb

from pprint import pprint
import random
import math


# analysises:
trending = mdb.trendingwords(1, 10, 150, 1)
# print trending


#                             _ _     
#  _ __  _ __ ___ _ __     __| | |__  
# | '_ \| '__/ _ \ '_ \   / _` | '_ \ 
# | |_) | | |  __/ |_) | | (_| | |_) |
# | .__/|_|  \___| .__/   \__,_|_.__/ 
# |_|            |_|                  
# convoInterval = 86400 #one day
# mdb.init(convoInterval)
mdb.init_chronological()


if __name__ == "__main__" and len(mdb.db_chron()) > 0:
	print "[+] program starts."
	db = mdb.db_chron()

	tally = dict()
	
	for s in db:
		text = s[0]
		speaker = int(s[1])
		if text not in tally and speaker == 1:
			elems = text.split()
			tally[text] = 0
			for e in elems:
				if e in trending:
					tally[text] += 1

	# print tally
	t = msgs.orderTally(tally)
	# print t

	trendWordSentences = dict()
	chosenWord = ""
	got_it = False
	for sentence in t:
		if len(sentence[0]) < 45 and len(sentence[0]) > 30:
			# print sentence[0], sentence[1]
			elems = sentence[0].split()
			checked = set()
			for e in elems:
				if e in trending and e not in checked and got_it is not True:
					checked.add(e)
					if e not in trendWordSentences:
						trendWordSentences[e] = list()
					trendWordSentences[e].append(sentence[0])
					if len(trendWordSentences[e]) > 5:
						chosenWord = e
						got_it = True

	for s in trendWordSentences[chosenWord]:
		print s




	# ------------------------------------------------
	# ------------------------------------------------
	# ------------------------------------------------
	# ------------------------------------------------

	##  Pattern analysis!!!
	# patterns = dict()
	# s = msgs.returnAllSentences(db)
	# for e in s:
	# 	blob = TextBlob(str(e[0]).decode('utf8'))
	# 	p  = ""
	# 	for word, pos in blob.tags:
	# 		p = p + " " + str(pos)
	# 	if p not in patterns:
	# 		patterns[p] = 0
	# 	patterns[p] += 1
	# patterns = msgs.orderTally(patterns)
	# # pprint(patterns)
	# print len(patterns)

	# for i in range(200, 500):
	# 	print str(i) + ". " + str(patterns[i][0]) + " : "
	# 	p_set = dict()
	# 	for e in s:
	# 		blob = TextBlob(str(e[0]).decode('utf8'))
	# 		p  = ""
	# 		for word, pos in blob.tags:
	# 			p = p + " " + str(pos)
	# 		if p == str(patterns[i][0]):
	# 			if e[0] not in p_set:
	# 				p_set[e[0]] = 0
	# 			p_set[e[0]] += 1

	# 			# print "\t" + str(e[0])
	# 	p_set = msgs.orderTally(p_set)
	# 	for i in p_set:
	# 		print "\t" + str(i[0]) + " --- " + str(i[1])
			











	# ------------------------------------------------
	# ------------------------------------------------
	# ------------------------------------------------
	# ------------------------------------------------
	# ------------------------------------------------
	# ------------------------------------------------
	# ------------------------------------------------
	# ------------------------------------------------

	# from pattern.en import parsetree
	# from pattern.search import search, Pattern
	# from pattern.search import Pattern, search

	# s = msgs.returnAllSentences(db)
	# for e in s:
	# 	try:
	# 		t = parsetree(str(e[0]).decode('utf8'), lemmata=True)
	# 		p = Pattern.fromstring('{WRB} * {PRP*} * \?')
	# 		m = p.match(t)
	# 		print str(e[0])
	# 		print "\t"*10 + m.string[:-2] + m.string[-1]			
	# 	except:
	# 		leon = 1



	# thinks = list()

	# for e in s:
	# 	try:
	# 		t = parsetree(str(e[0]).decode('utf8'), lemmata=True)
	# 		# p = Pattern.fromstring('NNP NN IN DT NP')
	# 		p = Pattern.fromstring('I think * about')
	# 		m = p.match(t)
	# 		print str(e[0])
	# 		print "\t"*10 + m.string
	# 		thinks.append(m.string)
	# 	except:
	# 		leon = 1

	

	# things = list()
	# for e in s:
	# 	try:
	# 		t = parsetree(str(e[0]).decode('utf8'), lemmata=True)
	# 		# p = Pattern.fromstring('NNP NN IN DT NP')
	# 		p = Pattern.fromstring('{JJ} {NNS}')
	# 		m = p.match(t)
	# 		# print str(e[0])
	# 		# print "\t"*10 + m.string
	# 		things.append(m.string)

	# 	except:
	# 		leon = 1

	# for i in range(10):
	# 	print random.sample(thinks, 1)[0]
	# 	print random.sample(things, 1)[0]
	# 	print ""
	# 	print "-"*50


	# ------------------------------------------------
	# ------------------------------------------------
	# ------------------------------------------------
	# ------------------------------------------------