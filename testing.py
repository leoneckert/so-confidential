import mdb
import msgs
from pprint import pprint
import random
import math



#                             _ _     
#  _ __  _ __ ___ _ __     __| | |__  
# | '_ \| '__/ _ \ '_ \   / _` | '_ \ 
# | |_) | | |  __/ |_) | | (_| | |_) |
# | .__/|_|  \___| .__/   \__,_|_.__/ 
# |_|            |_|                  
convoInterval = 86400 #one day
mdb.init(convoInterval)



if __name__ == "__main__" and len(mdb.db()) > 0:
	
	print "[+] actual program starts.\n"
	db = mdb.db()

	# all_msgs = msgs.returnAllTexts(db)
	# print all_msgs
	# tRange = msgs.getTimeRange(db)
	# print tRange
	# print tRange[0]
	# print tRange[1]
	# print msgs.getTimeRange(db)[0]

	# pprint(msgs.returnAllSentences(db))
	# print msgs.returnRandomSentence(db)
	


	# avgTimeNormal = 0
	# for i in range(1,100):
	# 	s = msgs.returnRandomSentence(db)
	# 	avgTimeNormal = ((avgTimeNormal*(i-1)) + int(s[2]))/i

		
	# print msgs.returnDatetime(avgTimeNormal)
	
	# avgTimeRecent = 0
	# for i in range(1,100):
	# 	s = msgs.returnRandomRecentSentence(db, 4)
	# 	# print s[0], datetime.fromtimestamp(float(s[2]))
	# 	# print msgs.returnDatetime(s[2]) + " - " + str(s[0])
	# 	avgTimeRecent = ((avgTimeRecent*(i-1)) + int(s[2]))/i
		
	# print msgs.returnDatetime(avgTimeRecent)


	# for i in range(20):
	# 	rc = msgs.returnRandomConvo(db)
	# 	# pprint(rc)
	# 	# print "-"*30
	# 	print len(rc)
	# 	print "-"*30
	# 	for s in rc:
	# 		print "- " + str(s[0])
	# 	print "-"*100
	# 	print "-"*100

	from textblob import TextBlob, Word
	# for i in range(10):
	# 	c = 0
	# 	while c < 10:
	# 		s = msgs.returnRandomRecentSentence(db, 10)
	# 		if(len(str(s[0]).split()) > 4):
	# 			blob = TextBlob(str(s[0]).decode('utf8'))
	# 			for word, pos in blob.tags:
	# 				print word, pos
	# 			print "-"*100
	# 			c += 1

	from pattern.en import parsetree
	# for i in range(10):
	# 	c = 0
	# 	while c < 10:
	# 		s = msgs.returnRandomRecentSentence(db, 10)
	# 		if(len(str(s[0]).split()) > 4):
	# 			print s[0]
				 
	# 			s = str(s[0])
	# 			s = parsetree(s) 
	# 			for sentence in s: 
	# 				print "sentence is ", sentence
	# 				for chunk in sentence.chunks:
	# 					print "chunk is ", chunk
	# 					for word in chunk.words:
	# 						print word,
	# 					print

	# 			print "-"*100
	# 			c += 1



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
			


	# from pattern.en import parsetree
	# # from pattern.search import search, Pattern
	# from pattern.search import Pattern, search

	# s = msgs.returnAllSentences(db)
	# for e in s:
	# 	# t = parsetree(str(e[0]))
	# 	# print search('NP', t) # all noun phrases
	# 	try:
	# 		# t = parsetree(str(e[0]).decode('utf8'), lemmata=True)
	# 		# p = Pattern.fromstring('{NP} be * than {NP}')
	# 		# m = p.match(t)
	# 		# print str(e[0])
	# 		# print m.group(1)
	# 		# print m.group(2)
	# 		# print m.group(1).string


	# 		t = parsetree(str(e[0]).decode('utf8'), lemmata=True)
	# 		# p = Pattern.fromstring('{PRP*} {JJ} {NN*} {be} {JJ}')
	# 		p = Pattern.fromstring('{WRB} * {PRP*} * \?')
	# 		m = p.match(t)
	# 		print str(e[0])
	# 		# print m
	# 		print "\t"*10 + m.string[:-2] + m.string[-1]
	# 		# print str(e[0])

	# 		# print m.group(1)
	# 		# print m.group(2)
	# 		# print m.group(3)
	# 		# print str(e[0])
	# 		# print m.start
	# 		# print m.group(3).start
	# 		# print "I " + m.group(1).string + " " + m.group(2).string + " " + m.group(3).string

	# 		# print "-"*50
	# 		# print m.group(1).string

	# 		# t = parsetree(str(e[0]).decode('utf8'))
	# 		# se = search('JJ', t)
	# 		# # print len(se)
	# 		# # print len(se[0])
	# 		# if len(se) > 0:
	# 		# 	# print se
	# 		# 	for el in se:
	# 		# 		print el.string,
	# 		# 	print "-"*50

	# 		# print str(e[0])[m.group(1).start:m.group(2).start]
			
	# 	except:
	# 		leon = 1


	from pattern.en import parsetree
	# from pattern.search import search, Pattern
	from pattern.search import Pattern, search

	s = msgs.returnAllSentences(db)
	# for e in s:
	# 	try:
	# 		t = parsetree(str(e[0]).decode('utf8'), lemmata=True)
	# 		p = Pattern.fromstring('{WRB} * {PRP*} * \?')
	# 		m = p.match(t)
	# 		print str(e[0])
	# 		print "\t"*10 + m.string[:-2] + m.string[-1]			
	# 	except:
	# 		leon = 1

	thinks = list()

	for e in s:
		try:
			t = parsetree(str(e[0]).decode('utf8'), lemmata=True)
			# p = Pattern.fromstring('NNP NN IN DT NP')
			p = Pattern.fromstring('I think * about')
			m = p.match(t)
			print str(e[0])
			print "\t"*10 + m.string
			thinks.append(m.string)
		except:
			leon = 1

	

	things = list()
	for e in s:
		try:
			t = parsetree(str(e[0]).decode('utf8'), lemmata=True)
			# p = Pattern.fromstring('NNP NN IN DT NP')
			p = Pattern.fromstring('{JJ} {NNS}')
			m = p.match(t)
			# print str(e[0])
			# print "\t"*10 + m.string
			things.append(m.string)

		except:
			leon = 1

	for i in range(10):
		print random.sample(thinks, 1)[0]
		print random.sample(things, 1)[0]
		print ""
		print "-"*50


	# for i in range(10):

	# 	rrs = msgs.returnRandomSentence(db)
	# 	# print rrs[0]
	# 	blob = TextBlob(str(rrs[0]).decode('utf8'))
	# 	# print blob.tags
	# 	# np = " "
	# 	print len(blob.noun_phrases)
	# 	np = " "
	# 	if len(blob.noun_phrases) > 0:
	# 		np = blob.noun_phrases[0]

	# 	# while len(np) < 10:
	# 	# 	print "loop"
	# 	# 	rrs = msgs.returnRandomSentence(db)
	# 	# 	# print rrs[0]
	# 	# 	blob = TextBlob(str(rrs[0]).decode('utf8'))
	# 	# 	# print blob.tags
	# 	# 	np = blob.noun_phrases[0]
	# 	print np

		# if t == "NP":
		# 	print w


 
# s = 'The mobile web is more important than mobile apps.'
# s = parsetree(s, relations=True, lemmata=True)
# for match in search('NP be RB?+ important than NP', s):
#     print match.constituents()[-1], '=>', \
#           match.constituents()[0]




