import msgs
import mdb

from pprint import pprint
import random
import math


# bigger analysises
# mdb.trendingwords(15, 5, 4, 1)
# mdb.trendingwords(2, 5, 150, 0)
# mdb.trendingwords(2, 10, 150, 0)
trending = mdb.trendingwords(2, 10, 150, 0)








#                             _ _     
#  _ __  _ __ ___ _ __     __| | |__  
# | '_ \| '__/ _ \ '_ \   / _` | '_ \ 
# | |_) | | |  __/ |_) | | (_| | |_) |
# | .__/|_|  \___| .__/   \__,_|_.__/ 
# |_|            |_|                  
convoInterval = 86400 #one day
mdb.init(convoInterval)



if __name__ == "__main__" and len(mdb.db()) > 0:
	
# 	print "[+] actual program starts.\n"
	db = mdb.db()


	sent = msgs.returnAllSentences(db)

	tally = dict()
	
	for s in sent:
		# print s
		text = s[0]
		# print s[0]
		# print text
		if text in tally:
			nothing = 1
		else:
			elems = text.split()
			tally[text] = 0
			for e in elems:
				if e in trending:
					tally[text] += 1
	# pprint(msgs.orderTally(tally))
	t = msgs.orderTally(tally)
	for sentence in t:
		if len(sentence[0]) < 40:
			print sentence[0], sentence[1]


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



