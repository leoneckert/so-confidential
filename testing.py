import mdb
import msgs
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

	all_msgs = msgs.returnAllTexts(db)
	print all_msgs
	# for i in range(10):
	# 	print msgs.returnRandomText(db)
	# 	print "-"*50
	# for u in range(30):
	# 	text = " "
	# 	while text[-1] is not "?":
	# 		text = msgs.returnRandomText(db)
	# 		if len(text) < 1:
	# 			text = " "
	# 	print text
	# 	print "-"*50


	# r_convo = returnRandomConvo(db)
	# print r_convo


	# all_message_string = ""
	# for msg in all_msgs:
	# 	all_message_string = all_message_string + " " + msg
	# print all_message_string












