
import mdb
import operator
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
	# print "start"
   
	# pprint(mdb.db())

	# print(len(mdb.db()))
	# starters = dict()
	# for person in msgs:
	# 	# pprint(person)
	# 	# pprint(msgs[person])
	# 	# pprint(msgs[person][0]) #print first convo
		
	# 	# print "**P" + str(person) + "**"
	# 	# pprint(msgs[person])
	# 	for convo in msgs[person]:
	# 		# print "\t- " + msgs[person][convo][0][0]
	# 		line = msgs[person][convo][0][0]
	# 		words = line.split()
	# 		for word in words:
	# 			if word not in starters:
	# 				starters[word] = 0
	# 			starters[word] += 1
	# # print starters

	# SortedwordsTally2 = sorted(starters.items(), key=lambda x: (-x[1], x[0]))
	# for i in range(100):
	# 	w = SortedwordsTally2[i][0] #+ " " + str(SortedwordsTally2[i][1])
	# 	print w, " ",





		# 	print "\t**C" + str(convo) + "**"
		# 	pprint(msgs[person][0][convo][0])

		# pprint(msgs[person][0][0][0]) #prints all convo openers 
		# pprint(msgs[person][0][len(msgs[person][0])-1][0]) #prints all convo enders

	# pprint(msgs)




