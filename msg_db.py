def createMessageDataStructure():
	while True:
			msg_count = 0
			# print "trying handle_id: " + str(handle_id)
			
			currentConvo = 0;
			convoELem = 0
			for line in os_system('sqlite3 ~/Library/Messages/chat.db "select handle_id, is_from_me, date, text from message where handle_id='+ str(handle_id) + ';"'):
				line = line.strip()
				# prints lines like this: 0|1|451686174|yes, thanks of the quick reply
				elems = line.split("|")
				# prints data like this: ['0', '1', '451686174', 'yes, thanks of the quick reply']
			
				if len(elems) > 4:
					while len(elems) > 4:
						elems[len(elems) - 2] =  elems[len(elems) - 2] + "|" + elems[len(elems) - 1]
						elems.remove(elems[len(elems) - 1])

				if len(elems) == 4:
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
					convoELem += 1
				elif len(elems) == 1:
					msgs[person][currentConvo][convoELem - 1][0] = msgs[person][currentConvo][convoELem -1][0] + " " + elems[0]
				else:
					print "something is unexpected here. The lenght of this line list is: " + str(len(elems))
					print elems
					print "-"*40
				
				msg_count += 1
			
			# break
			if msg_count > 0:
				zeroSequence = 0
			elif msg_count == 0:
				zeroSequence += 1

			if zeroSequence > 20:
				print "reached handle_id " + str(handle_id) + " and counted 20 handle_id in a row with no messages. We must be done."
				break

			handle_id += 1
		print "done"