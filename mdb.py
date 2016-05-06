import sqlite3
from os import path
from textblob import TextBlob, Word
import enchant
import msgs
from pprint import pprint

db = list()

def init():
	CHAT_DB = path.expanduser("~/Library/Messages/chat.db")
	dbs = sqlite3.connect(CHAT_DB)
	cursor = dbs.cursor()
	rows = cursor.execute("""select text, is_from_me, date from message;""")
	for row in rows:
		# some are None, others are weird objects (when sending photos etc.)
		if row[0] is not None and str(row)[:10] != "(u'\ufffc'": 
			db.append(row)

def getNumMessages():	
	return len(db)

def getStartEndDate():
	return [db[0][3], db[-1][3]]

def getFilteredDb(speaker = 2):
	filteredDB = list()
	if speaker == 0 or speaker == 1:
		for text_data in db:
			if text_data[1] == speaker:
				filteredDB.append(text_data)
	else:
		filteredDB = db
	return filteredDB

eng_dict = enchant.Dict("en_US")

def isWordEnglish(word):
	return eng_dict.check(word)

def isSentenceEnglish(sentence, threshold = 0.5):
	num_w = len(sentence.words) * 1.0
	eng_w = 0.0
	if num_w > 0:
		for word in sentence.words:
			try:
				if isWordEnglish(word):
					eng_w += 1
			except:
				nevermind = 1

		if eng_w/num_w < threshold:
			return False
	return True

def getAllSentences(speaker=1, eng_filter=1):
	fdb = getFilteredDb(speaker)
	sentences = list()
	num_eng_sentences = 0
	num_not_eng_sentences = 0

	for text_data in fdb:
		text = text_data[0]
		speaker = int(text_data[1])
		date = int(text_data[2])
		# print text
		blob = TextBlob(text) # what was it again, better practise to do: .decode('utf-8')? 
		for sentence in blob.sentences:
			
			if eng_filter == 1 and isSentenceEnglish(sentence, threshold = 0.5) is False:
				num_not_eng_sentences += 1
				break
			elif eng_filter == 1:
				num_eng_sentences += 1

			tempList = list()
			sentence = sentence.replace("\n", " ")
			tempList.append(sentence)
			tempList.append(speaker)
			tempList.append(date)
			sentences.append(tempList)
	# if speaker == 1:
	# 	print "[+] retrieved all SENT sentences."
	# elif speaker == 0:
	# 	print "[+] retrieved all RECEIVED sentences."
	# else:
	# 	print "[+] retrieved all sentences."
	# print "english:", num_eng_sentences
	# print "not english:", num_not_eng_sentences
	return sentences



def getTrendingWordsAndSentences(sentence_list, days_per_segment = 5,  num_words = 2, max_sent_length = 1000, blacklist_freq = 0.5):
	segments = dict()
	dates = dict()
	blacklist = dict()
	sentences_by_segment = dict()


	interval = days_per_segment*24*60*60

	current_segment_index = 0
	currentTimeStamp = int(sentence_list[0][2])

	segments[current_segment_index] = dict()
	dates[current_segment_index] = currentTimeStamp
	sentences_by_segment[current_segment_index] = set()

	blacklist_checked_current_segment = set()

	notWantedChars = set('!"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~')

	for sentence_data in sentence_list:
		text = sentence_data[0]
		speaker = sentence_data[1]
		timeStamp = sentence_data[2]

		if timeStamp - currentTimeStamp > interval:
			# a new segment starts
			current_segment_index += 1
			currentTimeStamp = timeStamp
			segments[current_segment_index] = dict()
			dates[current_segment_index] = currentTimeStamp
			blacklist_checked_current_segment = set()

		for word in text.words:
			if word not in segments[current_segment_index]:
				segments[current_segment_index][word] = 0
			segments[current_segment_index][word] += 1

			if word not in blacklist_checked_current_segment:
				blacklist_checked_current_segment.add(word)
				if word not in blacklist:
					blacklist[word] = 0
				blacklist[word] += 1
		
		if current_segment_index not in sentences_by_segment:
			sentences_by_segment[current_segment_index] = set()
		if text not in sentences_by_segment[current_segment_index]:
			sentences_by_segment[current_segment_index].add(text)



	# pprint(sentences_by_segment)
	# filter blacklist:
	
	num_segments = len(segments) * 1.0
	to_delete = list()
	for black_word in blacklist:
		word_freq = blacklist[black_word] * 1.0
		if word_freq/num_segments < blacklist_freq:
			to_delete.append(black_word)
	for black_word in to_delete:
		blacklist.pop(black_word, None)


	trending_by_segment = dict()
	sum_top_words = 0
	sum_bottom_words = 0
	# find trending words for each segment
	for segment in segments:

		words = msgs.orderTally(segments[segment])
		# pprint(words)
		# print segment, "  -  ", msgs.returnDatetime(dates[segment])[:10]
		trending_by_segment[segment] = list()
		c = 0
		for word, freq in words:
			# print "\t\t", word, freq

			if word not in blacklist:
				trending_by_segment[segment].append([word, freq])
				if c == 0:
					sum_top_words += freq
				c += 1
				if c >= num_words:
					sum_bottom_words += freq
					break
	# pprint(trending_by_segment)

	index_word_sentence = dict()
	index_date = dict()
	populated_indeces = set()
	word_index = dict()
	index_num_sentences = dict()

	for segment in trending_by_segment:
		index_word_sentence[segment] = dict()
		index_date[segment] = dates[segment]
		
		# print segment, "  -  ", msgs.returnDatetime(dates[segment])[:10]
		for word, freq in trending_by_segment[segment]:
			index_word_sentence[segment][word] = list()
			if word not in word_index:
				word_index[word] = set()
			word_index[word].add(segment)
			# print "\t\t", word
			for s in sentences_by_segment[segment]:
				# print s.words
				for w in s.words:
					# print w
					if w == word:
						if len(s) <= max_sent_length:
							index_word_sentence[segment][word].append(s)
							populated_indeces.add(segment)
							if segment not in index_num_sentences:
								index_num_sentences[segment] = 0
							index_num_sentences[segment] += 1
							# print "\t\t\t\t", s
						break
	# pprint(index_word_sentence)
	# pprint(index_date)
	# pprint(populated_indeces)
	# pprint(word_index)
	# pprint(index_num_sentences)

	return {"index_word_sentence" : index_word_sentence, "index_date": index_date, "populated_indeces" : populated_indeces, "word_index": word_index, "index_num_sentences": index_num_sentences}






		
















