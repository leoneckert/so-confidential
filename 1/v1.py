# import msgs
import mdbv1

# from pprint import pprint
# import random
# import math


# # first deteremine the size of the dataset, 
# # then optimize the trending word algorithm

# print "[+] determining the trending words over time."
# print "[ ] this might take a momemt..."
# SENT = mdb.optimizeTrendingWords(num_segments = 110, min_avg_bottom = 2, sender_id = 1)
# print "[ ] thanks for the patience, your messages are full of wisdom..."
# RECEIVED = mdb.optimizeTrendingWords(num_segments = 110, min_avg_bottom = 2, sender_id = 0)
# # pprint(SENT)
# # pprint(RECEIVED)





# #                             _ _     
# #  _ __  _ __ ___ _ __     __| | |__  
# # | '_ \| '__/ _ \ '_ \   / _` | '_ \ 
# # | |_) | | |  __/ |_) | | (_| | |_) |
# # | .__/|_|  \___| .__/   \__,_|_.__/ 
# # |_|            |_|                  
# # convoInterval = 86400 #one day
# # mdb.init(convoInterval)
# mdb.init_chronological()


# if __name__ == "__main__" and len(mdb.db_chron()) > 0:
# # 	print "[+] program starts."
# 	db_chron = mdb.db_chron()
# 	# pprint(db)
# 	sentences = msgs.returnChronSentences(db_chron)

# 	tally = dict()
# 	tally["SENT"] = dict()
# 	tally["RECEIVED"] = dict()
	
# 	for s in sentences:
# 		text = s[0]
# 		length_text = len(text)
# 		speaker = int(s[1])
# 		if speaker == 1:
# 			if text not in tally["SENT"]:
# 				elems = text.split()
# 				tally["SENT"][text] = 0.0
# 				# print text,
# 				for e in elems:
# 					if e in SENT["trending"]:
# 						tally["SENT"][text] += 100.0 - 100.0/len(elems)
# 						# print " + " + str(100.0 - 100.0/len(elems)), 
# 					if e in SENT["blacklist"]:
# 						tally["SENT"][text] -= 100.0/len(elems)
# 						# print " - " + str(100.0/len(elems)),
# 				# print tally["SENT"][text]

# 		elif speaker == 0:
# 			if text not in tally["RECEIVED"]:
# 				elems = text.split()
# 				tally["RECEIVED"][text] = 0.0
# 				# print text,
# 				for e in elems:
# 					if e in RECEIVED["trending"]:
# 						tally["RECEIVED"][text] += 100.0 - 100.0/len(elems)
# 						# print " + " + str(100.0 - 100.0/len(elems)), 
# 					if e in RECEIVED["blacklist"]:
# 						tally["RECEIVED"][text] -= 100.0/len(elems)
# 						# print " - " + str(100.0/len(elems)),
# 				# print tally["RECEIVED"][text]


# 	t = msgs.orderTally(tally["SENT"])

# 	t2 = list()
# 	t2q = list()
# 	desired_length = 40
# 	for s in t:
# 		if len(s[0]) < desired_length:
# 			if s[0].endswith("?"):
# 				t2q.append(s)
# 			else:
# 				t2.append(s)


# 	p = msgs.orderTally(tally["RECEIVED"])

# 	p2 = list()
# 	p2q = list()
# 	for s in p:
# 		if len(s[0]) < desired_length:
# 			if s[0].endswith("?"):
# 				p2q.append(s)
# 			else:
# 				p2.append(s)



# 	for i in range(80):

# 		print "[...]\n"
# 		print random.sample(t2q, 1)[0][0]
# 		print "\t\t\t\t", random.sample(p2, 1)[0][0]
# 		print "\t\t\t\t", random.sample(p2q, 1)[0][0]
# 		print random.sample(t2, 1)[0][0]
# 		print "\t\t\t\t", random.sample(p2, 1)[0][0]
# 		print random.sample(t2, 1)[0][0]
# 		print random.sample(t2q, 1)[0][0]
# 		print "\t\t\t\t", random.sample(p2, 1)[0][0]
# 		print "\n[...]"

# 		print "\n\n" + "-"*50 + "\n\n"

# 	# for i in range(100):
# 	# 	if t2[i][0].endswith("?"):
# 	# 		print t2[i][0], t2[i][1] 
# 	# 	if p2[i][0].endswith("?"):
# 	# 		print "\t\t\t", p2[i][0], p2[i][1] 

mdbv1.trendingwords(30, 5, 10, sender_id = 1, printing=1, optimizing = 0)









