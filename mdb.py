import sqlite3
from os import path
from textblob import TextBlob
import msgs
from pprint import pprint

db = list()

def init():
	CHAT_DB = path.expanduser("~/Library/Messages/chat.db")
	dbs = sqlite3.connect(CHAT_DB)
	cursor = dbs.cursor()
	rows = cursor.execute("""select text, is_from_me, handle_id, date from message;""")
	for row in rows:
		# some are None, others are weird objects (when sending photos etc.)
		if row[0] is not None and str(row)[:10] != "(u'\ufffc'": 
			db.append(row)

def getNumMessages():	
	return len(db)

def getStartEndDate():
	return [db[0][3], db[-1][3]]

def guessName():
	names = dict()
	for text_data in db:
		blob = TextBlob(text_data[0])
		for word, tag in blob.tags:
			if tag == "NNP":
				if word not in names:
					names[word] = 0
				names[word] += 1
	return msgs.orderTally(names)[0][0]

def getFilteredDb(sender_id = 2):
	filteredDB = list()
	if sender_id == 0 or sender_id == 1:
		for text_data in db:
			if text_data[1] == sender_id:
				filteredDB.append(text_data)
	else:
		filteredDB = db
	return filteredDB


def getTrendingwordsAndBlacklist(num_days = 2, num_words = 2, blacklist_limit = 0, sender_id = 2, printing=0, optimizing = 0):
	fdb = getFilteredDb(sender_id)
	segments = dict()
	dates = dict()
	blacklist = dict()

	interval = num_days*24*60*60
	
	current_segment_index = 0
	current_segment_time = int(fdb[0][3])

	segments[current_segment_index] = dict()
	dates[current_segment_index] = current_segment_time

	blacklist_checked_current_segment = set()

	for text_data in fdb:

		text = text_data[0]
		speaker = int(text_data[1])
		person = int(text_data[2])
		date = int(text_data[3])

		if date - current_segment_time > interval:
			# a new segments starts!
			current_segment_index += 1
			current_segment_time = date
			segments[current_segment_index] = dict()
			dates[current_segment_index] = current_segment_time
			blacklist_checked_current_segment = set()

		words = text.split()
		for word in words:
			if word not in segments[current_segment_index]:
				segments[current_segment_index][word] = 0
			segments[current_segment_index][word] += 1

			if word not in blacklist_checked_current_segment:
				blacklist_checked_current_segment.add(word)
				if word not in blacklist:
					blacklist[word] = 0
				blacklist[word] += 1


	# filter blacklist:
	
	num_segments = len(segments)
	to_delete = list()
	for black_word in blacklist:
		if num_segments - blacklist[black_word] >= blacklist_limit:
			to_delete.append(black_word)
	for black_word in to_delete:
		blacklist.pop(black_word, None)


	trendingwords = list()
	#print out stuff
	sum_top_words = 0
	sum_bottom_words = 0
	notWantedChars = set('!"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~')
	if printing: print "\there the trending words per segment:"
	for segment in segments:
		if printing: print "\t\t[", segment, "] segment:", msgs.returnDatetime(dates[segment])[:10]
		words = msgs.orderTally(segments[segment])
		c = 0
		for word_data in words:
			# print word_data[0]
			to_add = word_data[0]
			if len(to_add) > 1:
				while to_add[0] in notWantedChars:
					to_add = to_add[1:]
					if len(to_add) < 2: break
				while to_add[-1] in notWantedChars:
					to_add = to_add[:-1]
					if len(to_add) < 1: break

			if to_add not in blacklist and len(to_add) > 1 and len(set(to_add)) > 3:
				trendingwords.append(to_add)		
				if printing: print "\t\t\t\t\t", to_add, word_data[1]
				if c == 0:
					sum_top_words += word_data[1]
				c += 1
				if c >= num_words:
					sum_bottom_words += word_data[1]
					break


	average_top_words = sum_top_words/num_segments
	average_bottom_words = sum_bottom_words/num_segments

	if optimizing: return [num_segments, average_top_words, average_bottom_words, len(trendingwords), len(blacklist)]
	if not optimizing: return {"trending":trendingwords, "blacklist":blacklist}




def optimiseTrendingwordsAndBlacklist(segmenthook = 80, num_words = 2, bottom_average_hook = 4, sender_id = 2, printing=0):
	days_per_segement = 1
	returned_data = getTrendingwordsAndBlacklist(num_days = days_per_segement, num_words = num_words, sender_id = sender_id, optimizing = 1)
	
	while returned_data[0] > segmenthook:
		days_per_segement += 1
		returned_data = getTrendingwordsAndBlacklist(num_days = days_per_segement, num_words = num_words, sender_id = sender_id, optimizing = 1)

	# checking if we overshot the goal
	previous_data = getTrendingwordsAndBlacklist(num_days = days_per_segement - 1, num_words = num_words, sender_id = sender_id, optimizing = 1)
	if segmenthook - returned_data[0] > previous_data[0] - segmenthook:
		days_per_segement -= 1

	blacklist_limit = 0
	returned_data = getTrendingwordsAndBlacklist(num_days = days_per_segement, num_words = num_words, blacklist_limit = blacklist_limit, sender_id = sender_id, optimizing = 1)
	while returned_data[1] > bottom_average_hook:
		blacklist_limit += 1
		returned_data = getTrendingwordsAndBlacklist(num_days = days_per_segement, num_words = num_words, blacklist_limit = blacklist_limit, sender_id = sender_id, optimizing = 1)

	if sender_id == 1:
		print "[+] retrieved trending and blacklisted words for all SENT messages."
	elif sender_id == 0:
		print "[+] retrieved trending and blacklisted words for all RECEIVED messages."
	else:
		print "[+] retrieved trending and blacklisted words for all messages."

	print "[ ] parameters were optimised as follows:"
	print "\t", days_per_segement, "days per segment"
	print "\t", blacklist_limit, "segments without a specific word before it gets off the blacklist."
	print "\t", returned_data[3], "trending words returned"
	print "\t", returned_data[4], "blacklisted words returned"


	return getTrendingwordsAndBlacklist(num_days = days_per_segement, num_words = num_words, blacklist_limit = blacklist_limit, sender_id = sender_id, printing=printing, optimizing = 0)



def returnSentences(sender_id = 2):
	fdb = getFilteredDb(sender_id)
	sentences = list()
	
	for text_data in fdb:
		text = text_data[0]
		speaker = int(text_data[1])
		person = int(text_data[2])
		date = int(text_data[3])
		try:
			blob = TextBlob(text.decode('utf-8'))
		except:
			blob = TextBlob(text)
		for sentence in blob.sentences:
			tempList = list()
			
			sentence = sentence.replace("\n", " ")
			
			tempList.append(sentence)
			tempList.append(speaker)
			tempList.append(person)
			tempList.append(date)
			sentences.append(tempList)
	if sender_id == 1:
		print "[+] retrieved all SENT sentences."
	elif sender_id == 0:
		print "[+] retrieved all RECEIVED sentences."
	else:
		print "[+] retrieved all sentences."
	return sentences














