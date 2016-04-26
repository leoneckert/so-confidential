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

	patterns = dict()
	s = msgs.returnAllSentences(db)
	for e in s:
		blob = TextBlob(str(e[0]).decode('utf8'))
		p  = ""
		for word, pos in blob.tags:
			p = p + " " + str(pos)
		if p not in patterns:
			patterns[p] = 0
		patterns[p] += 1
	patterns = msgs.orderTally(patterns)
	pprint(patterns)
		# print e[0]
		# s = str(e[0])
		# s = parsetree(s) 
		# for sentence in s: 
		# 	# print "sentence is ", sentence
		# 	for chunk in sentence.chunks:
		# 		# print "chunk is ", chunk
		# 		for word in chunk.words:
		# 			print word,
		# print




