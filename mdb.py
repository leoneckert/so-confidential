from subprocess import Popen, PIPE

msgs = dict()

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
	num_msgs = 0

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

				if person not in msgs:
					msgs[person] = dict()

				if currentConvo not in msgs[person]:
					msgs[person][currentConvo] = list()
				elif int(time) - int(msgs[person][currentConvo][convoELem - 1][2]) > convoInterval:
					currentConvo += 1
					convoELem = 0
					msgs[person][currentConvo] = list()
					# print "NEW CONVO"

				tempData = list()
				tempData.append(text)
				tempData.append(speaker)
				tempData.append(time)

				msgs[person][currentConvo].append(tempData)
				# print msgs[person][currentConvo][convoELem ][2]
				num_msgs += 1
				convoELem += 1
			elif len(elems) == 1: #that means there was only text because the text message was printed in several lines
				msgs[person][currentConvo][convoELem - 1][0] = msgs[person][currentConvo][convoELem -1][0] + " " + elems[0]
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
			if len(msgs) < 1:
				print "[-] no messages found."
			else:
				print "[+] data structure complete."
				print "[ ] \tincludes " + str(num_msgs) + " messages.\n"
				# print "[+] return data with 'mdb.db()'\n"
			break

		handle_id += 1
	
	return msgs

def db():
	return msgs




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
