
# import mdb
# import msgs
from pprint import pprint



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
	# pprint(db)
	
	word_tally = msgs.wordTally(db)
	pprint(word_tally)
	for i in range(500):
		print word_tally[i][0]
   
	