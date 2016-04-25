import mdb
import msgs
from pprint import pprint
import random



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


	# c = 0
	# while c < 10:
	# 	s = msgs.returnRandomSentence(db)
	# 	if len(s) == 0:
	# 		s = " "
	# 	if s.endswith("?") or s.endswith(".") or s.endswith("!"):  
	# 		print "-"*50
	# 		print "-"*50
	# 		print s
	# 		print "-"*50
	# 		print "-"*50
	# 		c += 1

	# c = 0
	# while c < 5:
	# 	s = msgs.returnRandomSentence(db)
	# 	if len(s.split()) == 0:
	# 		s = " "
	# 	if s.endswith("."):  
	# 		print s
	# 		print "-"*50

	# 		c += 1

	tRange = msgs.getTimeRange(db)
	print tRange
	print tRange[0]
	print tRange[1]
	print msgs.getTimeRange(db)[0]



	# c = 0
	# while c < 10:
	# 	s = msgs.returnRandomSentence(db)
	# 	if len(s.split()) is c+1:
	# 		print s
	# 		print "-"*50
	# 		c += 1











