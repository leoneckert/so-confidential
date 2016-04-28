from subprocess import Popen, PIPE

messages = dict()

# from: http://stackoverflow.com/a/32988831/6163933
def os_system(command):
    process = Popen(command, stdout=PIPE, shell=True)
    while True:
        line = process.stdout.readline()
        if not line:
            break
        yield line

def init(convoInterval):
	print "[+] parsing messages..."
	handle_id = 0
	zeroSequence = 0
	num_messages = 0

	while True:
		msg_count = 0
		# print "trying handle_id: " + str(handle_id)
		
		currentConvo = 0;
		convoELem = 0
		for line in os_system('sqlite3 ~/Library/Messages/chat.db "select handle_id, is_from_me, date, text from message where handle_id='+ str(handle_id) + ';"'):
			line = line.strip()

			elems = line.split("|")
			# prints data like this: ['0', '1', '451686174', 'yes, thanks of the quick reply']
		
			if len(elems) > 4: # that means that there were "|" symbols in the text message
				while len(elems) > 4:
					elems[len(elems) - 2] =  elems[len(elems) - 2] + "|" + elems[len(elems) - 1]
					elems.remove(elems[len(elems) - 1])


			if len(elems) == 4: #that's what we expect
				person = elems[0]
				speaker = elems[1]
				time = elems[2]
				text = elems[3]

				if person not in messages:
					messages[person] = dict()

				if currentConvo not in messages[person]:
					messages[person][currentConvo] = list()
				elif int(time) - int(messages[person][currentConvo][convoELem - 1][2]) > convoInterval:
					currentConvo += 1
					convoELem = 0
					messages[person][currentConvo] = list()
					# print "NEW CONVO"

				tempData = list()
				tempData.append(text)
				tempData.append(speaker)
				tempData.append(time)

				messages[person][currentConvo].append(tempData)
				# print messages[person][currentConvo][convoELem ][2]
				num_messages += 1
				convoELem += 1
			elif len(elems) == 1: #that means there was only text because the text message was printed in several lines
				messages[person][currentConvo][convoELem - 1][0] = messages[person][currentConvo][convoELem -1][0] + " " + elems[0]
			else:
				print "-"*20 + "\n" + "[!] something went wrong with this line" + "\n" + "its elements are in this array:"
				print elems
				print "-"*20
			
			msg_count += 1
		
		if msg_count > 0:
			zeroSequence = 0
		elif msg_count == 0:
			zeroSequence += 1

		if zeroSequence > 20:
			# print "[+] reached handle_id " + str(handle_id) + ".\n[+] previous 20 handle_id's had no messages.\n[+] I declare the message data structure complete."
			if len(messages) < 1:
				print "[-] no messages found."
			else:
				print "[+] data structure complete."
				print "[ ] \tincludes " + str(num_messages) + " messages.\n"
				# print "[+] return data with 'mdb.db()'\n"
			break

		handle_id += 1
	
	return messages

def db():
	return messages



messages_chronological = list()
def db_chron():
	return messages_chronological

def init_chronological():
	print "[+] parsing messages..."
	m_count = 0
	for line in os_system('sqlite3 ~/Library/Messages/chat.db "select handle_id, is_from_me, date, text from message"'):
		line = line.strip()

		elems = line.split("|")
		# prints data like this: ['0', '1', '451686174', 'yes, thanks of the quick reply']
	
		if len(elems) > 4: # that means that there were "|" symbols in the text message
			while len(elems) > 4:
				elems[len(elems) - 2] =  elems[len(elems) - 2] + "|" + elems[len(elems) - 1]
				elems.remove(elems[len(elems) - 1])


		if len(elems) == 4: #that's what we expect
			person = elems[0]
			speaker = elems[1]
			time = elems[2]
			text = elems[3]
			temp_list = list()
			temp_list.append(text)
			temp_list.append(speaker)
			temp_list.append(person)
			temp_list.append(time)
			messages_chronological.append(temp_list)
			m_count += 1


		elif len(elems) == 1: #that means there was only text because the text message was printed in several lines
			messages_chronological[len(messages_chronological) - 1][0] += " " + elems[0] 
		else:
			print "-"*20 + "\n" + "[!] something went wrong with this line" + "\n" + "its elements are in this array:"
			print elems
			print "-"*20
	print "[+] prepared " + str(m_count) + " messages."
	return messages_chronological




#### ANOTHER SOLUTION WOULD BE SOMETHING LIK THIS USINF PYTHON SQLITE3 library. Is this better?
## from here: https://gist.github.com/nslater/b3cbc894ad2c2516dd02


# import sqlite3
# from os import path
# # conn = sqlite3.connect('/Users/leoneckert/Library/Messages/chat.db')

# if __name__ == "__main__":

# 	CHAT_DB = path.expanduser("~/Library/Messages/chat.db")

# 	# Apple's epoch starts on January 1st, 2001 for some reason...
# 	# cf. http://apple.stackexchange.com/questions/114168
# 	EPOCH=978307200

# 	def list_chats():
# 	    db = sqlite3.connect(CHAT_DB)
# 	    cursor = db.cursor()
# 	    rows = cursor.execute("""
# 	        select text from message where is_from_me=1;
# 	    """)
# 	    for row in rows:
# 	        print(row[0])

# 	list_chats()




# --------------------------------------------------------------------------
import msgs # named twice !
from pprint import pprint


def trendingwords(num_days, num_words, blacklist_limit, sender_id = 2):
	# num_days > amount of days of one time segment
	# num_words > amount of words printed out per time segment
	# black_list_parameter >
	#   modifies how often a word has to not appear in a segment in order to 
	#	get off the blacklist (the higher, the more words end up 
	#	on the black list if it's 0, then the blacklist will be empty)
	# sender_id > if not specified then all messages are analysed.
	#	else, if its 0, only the messages received are anlysed and 
	#	if its 1, only the messages sent

	first = True
	all_data = dict()
	sectionCount = 0
	interval = num_days*24*60*60
	currentTime = 0

	first_section = True	
	blacklist = dict()

	loop_count = 0

	date_by_section_count = dict()
	
	if sender_id is 0 or sender_id is 1:
		command = 'sqlite3 ~/Library/Messages/chat.db "select handle_id, is_from_me, date, text from message where is_from_me = ' + str(sender_id) + ';"'
	else:
		command = 'sqlite3 ~/Library/Messages/chat.db "select handle_id, is_from_me, date, text from message"'

	for line in os_system(command):

		line = line.strip()
		
		elems = line.split("|")
		
		if len(elems) > 4: # that means that there were "|" symbols in the text message
			while len(elems) > 4:
				elems[len(elems) - 2] =  elems[len(elems) - 2] + "|" + elems[len(elems) - 1]
				elems.remove(elems[len(elems) - 1])


		if len(elems) == 4: #that's what we expect
			person = elems[0]
			speaker = elems[1]
			time = elems[2]
			text = elems[3]

			if first is True:
				# print msgs.returnDatetime(time)
				currentTime = int(time)
				all_data[sectionCount] = dict()

				date_by_section_count[sectionCount] = msgs.returnDatetime(time)[:10]
			first = False

			words = text.split()


			if int(time) - currentTime <= interval:
				for word in words:
					if word not in all_data[sectionCount]:
						all_data[sectionCount][word] = 0
					all_data[sectionCount][word] += 1
					if first_section is True and blacklist_limit is not 0:
						# print "added loop " + str(loop_count)
						blacklist[word] = 0
					elif loop_count < blacklist_limit:   #makes sense?
						if word not in blacklist:
							# print "added loop " + str(loop_count)
							blacklist[word] = 0

			

			elif int(time) - currentTime > interval:
				loop_count += 1
				first_section = False
				to_delete = list()
				for black_word in blacklist:
					if black_word not in all_data[sectionCount]:
						blacklist[black_word] += 1
						if blacklist[black_word] >= blacklist_limit:
							to_delete.append(black_word)
				for delete_this in to_delete:
					blacklist.pop(delete_this, None)
				currentTime = int(time)
				sectionCount += 1
				col_words = dict()
				all_data[sectionCount] = dict()
				date_by_section_count[sectionCount] = msgs.returnDatetime(time)[:10]
				for word in words:
					if word not in all_data[sectionCount]:
						all_data[sectionCount][word] = 0
					all_data[sectionCount][word] += 1



		elif len(elems) == 1: #that means there was only text because the text message was printed in several lines
			text = elems[0]
			words = text.split()
			for word in words:
				if word not in all_data[sectionCount]:
					all_data[sectionCount][word] = 0
				all_data[sectionCount][word] += 1
		else:
			print "-"*20 + "\n" + "[!] something went wrong with this line" + "\n" + "its elements are in this array:"
			print elems
			print "-"*20

	# print "\nSettings:\n\tmessages analysed:",
	# if sender_id is 0:
	# 	print "only received messages"
	# elif sender_id is 1:
	# 	print "only sent messages"
	# else:
	# 	print "both received and sent messages"
	# print "\tlength of each segment: " + str(num_days) + " days\n\tblacklist parameter: " + str(blacklist_limit) + "\n\n-----\n"
	
	output = dict()
	for segment in all_data:
		ordered_tally = msgs.orderTally(all_data[segment])
		# print str(segment + 1) + ". Segment (" + str(date_by_section_count[segment]) + "):"
		
		if len(ordered_tally) <= num_words:
			for word, tally in ordered_tally:
				# print "\t", word, tally
				output[word] = 0
		else:
			c = 0
			for word, tally in ordered_tally:
				if c >= num_words:
					break
				if word not in blacklist:
					# print "\t", word, tally
					output[word] = 0
					c += 1
	return output








