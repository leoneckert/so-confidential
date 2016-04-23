from subprocess import Popen, PIPE
import operator


# from: http://stackoverflow.com/a/32988831/6163933
def os_system(command):
    process = Popen(command, stdout=PIPE, shell=True)
    while True:
        line = process.stdout.readline()
        if not line:
            break
        yield line


msgs = dict()

if __name__ == "__main__":
   
 
	# wordsTally = dict()
	# for line in os_system('sqlite3 ~/Library/Messages/chat.db "select text from message where is_from_me=1;"'):
	# 	line = line.strip()
	# 	words = line.split()
	# 	# print words
	# 	for word in words:
	# 		if word not in wordsTally:
	# 			wordsTally[word] = 0
	# 		wordsTally[word] += 1


	# SortedwordsTally2 = sorted(wordsTally.items(), key=lambda x: (-x[1], x[0]))
	# for i in range(200):
	# 	w = SortedwordsTally2[i][0]
	# 	print w, " ",

	# print "\n"*5


	# wordsTally = dict()
	# for line in os_system('sqlite3 ~/Library/Messages/chat.db "select text from message;"'):
	# 	line = line.strip()
	# 	words = line.split()
	# 	# print words
	# 	for word in words:
	# 		if word not in wordsTally:
	# 			wordsTally[word] = 0
	# 		wordsTally[word] += 1


	# SortedwordsTally2 = sorted(wordsTally.items(), key=lambda x: (-x[1], x[0]))
	# for i in range(200):
	# 	w = SortedwordsTally2[i][0] + " " + str(SortedwordsTally2[i][1])
	# 	print w, " ",

	handle_id = 0;
	zeroSequence = 0
	while True:
		msg_count = 0
		# print "trying handle_id: " + str(handle_id)
		
		for line in os_system('sqlite3 ~/Library/Messages/chat.db "select handle_id, is_from_me, date, text from message where handle_id='+ str(handle_id) + ';"'):
			line = line.strip()
			# print line
			msg_count += 1;
		if msg_count > 0:
			zeroSequence = 0
		elif msg_count == 0:
			zeroSequence += 1
		if zeroSequence > 20:
			print "reached handle_id " + str(handle_id) + " and counted 20 handle_id in a row with no messages. We must be done."
			break


			
		# print str(handle_id) + " : " +  str(msg_count) + " messages"
		handle_id += 1



	print "done"




