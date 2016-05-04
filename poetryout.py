from pprint import pprint
import enchant
from textblob import Word, TextBlob
import random



def wordUsable(word, trending, keeping_track, old_words):
	if word not in trending:
		return False

	# if word in keeping_track["words_used"]:
	# 	return False

	if word in old_words:
		return False

	notWantedVerbs = ('have', 'be', 'do', 'i', 'go', 'get', "don't", "it's")
	if Word(word).lemmatize('v').lower() in notWantedVerbs:
		return False

	notWantedNouns = ('i', 'u','you','ich','we','they', 'i\'m', 'i\u2019m', u'\xe5', 'that')
	if word.lower() in notWantedNouns:
		return False

	notWantedPenns = (u'DT', u'WDT', u'RB', u'WRB')
	if TextBlob(word).tags[0][1] in notWantedPenns:
		return False	

	return True


# notWantedChars = set('!"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~')
def updateWordCount(wordList, speaker, word_count, trending, keeping_track, old_words):
	notWantedChars = set('!"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~')
	d = enchant.Dict("en_US")
	
	for word in wordList:
		
		if len(word) > 1:
			while word[0] in notWantedChars:
				word = word[1:]
				if len(word) < 2: break
			while word[-1] in notWantedChars:
				word = word[:-1]
				if len(word) < 1: break

		# if word not in trending or word in keeping_track["words_used"]:
		# 	return word_count

		if not wordUsable(word, trending, keeping_track, old_words):
			return word_count

		# word = word.lower()

		used = set()
		if word not in used:
			if word not in word_count:
				word_count[word] = dict()
			if speaker not in word_count[word]:
				word_count[word][speaker] = 0
			word_count[word][speaker] += 1
			used.add(word)

	return word_count


def generate(SENTshuffled_aRatedbRatedList, RECEIVEDshuffled_aRatedbRatedList, sentTrendingBlacklist, receivedTrendingBlacklist, keeping_track):

	trending = set(sentTrendingBlacklist["trending"] + receivedTrendingBlacklist["trending"])

	SENT_A = SENTshuffled_aRatedbRatedList["aRated"]
	SENT_B = SENTshuffled_aRatedbRatedList["bRated"]
	RECEIVED_A = RECEIVEDshuffled_aRatedbRatedList["aRated"]
	RECEIVED_B = RECEIVEDshuffled_aRatedbRatedList["bRated"]

	# short if statement: 
	# print "yes" if a > b else "no"

	looplength = len(SENT_A) if len(SENT_A) < len(RECEIVED_A) else len(RECEIVED_A) 

	

	
	
	title = ""
	selected = dict()
	selected["sent"] = list()
	selected["received"] = list()

	word_count = dict()
	word_found = False
	chosen_word = ""
	old_words = set()
	checked_sentences = dict()
	checked_sentences["sent"] = set()
	checked_sentences["received"] = set()
	for i in range(looplength):
		ss = SENT_A[i][0] if SENT_A[i][0] not in keeping_track["sentences_used"] else ""
		checked_sentences["sent"].add(ss)
		sr = RECEIVED_A[i][0] if RECEIVED_A[i][0] not in keeping_track["sentences_used"] else ""
		checked_sentences["received"].add(sr)


		ss_words = ss.split()
		sr_words = sr.split()

		word_count = updateWordCount(ss_words, "sent", word_count, trending, keeping_track, old_words)

		word_count = updateWordCount(sr_words, "received", word_count, trending, keeping_track, old_words)

		# print ss
		# print sr
		# print "+++++ one sentence at a time +++++"

		for word in word_count:
			# print len(word_count[word])
			if len(word_count[word]) == 2:
				# print "yeah both"
				# print word
				count = 0
				for speaker in word_count[word]:
					# print speaker, word_count[word][speaker]
					count += word_count[word][speaker]
				# print "->", count 
				if count > 3:
					# print "word", word, "appeared", count, "times!"
					word_found = True
					chosen_word = word


		if word_found:
			break

	# pprint(word_count)
	# print chosen_word
	title = title + chosen_word
	# pprint(checked_sentences)
	applicable_sentences = dict()
	applicable_sentences["sent"] = list()
	applicable_sentences["received"] = list()
	
	for s in checked_sentences["sent"]:
		words = s.split()
		if chosen_word in words:
			applicable_sentences["sent"].append(s)
	for s in checked_sentences["received"]:
		words = s.split()
		if chosen_word in words:
			applicable_sentences["received"].append(s)
	# pprint(applicable_sentences)

	sentSelected = random.choice(applicable_sentences["sent"])
	receivedSelected = random.choice(applicable_sentences["received"])
	selected["sent"].append(sentSelected)
	selected["received"].append(receivedSelected)
	# pprint(selected)
	keeping_track["words_used"].add(chosen_word)
	keeping_track["sentences_used"].add(sentSelected)
	keeping_track["sentences_used"].add(receivedSelected)
	
	# ---------------

	word_count = dict()
	word_found = False
	old_words.add(chosen_word)
	chosen_word = ""
	checked_sentences = dict()
	checked_sentences["sent"] = set()
	checked_sentences["received"] = set()
	for i in range(looplength):
		ss = SENT_A[i][0] if SENT_A[i][0] not in keeping_track["sentences_used"] else ""
		checked_sentences["sent"].add(ss)
		sr = RECEIVED_A[i][0] if RECEIVED_A[i][0] not in keeping_track["sentences_used"] else ""
		checked_sentences["received"].add(sr)


		ss_words = ss.split()
		sr_words = sr.split()

		word_count = updateWordCount(ss_words, "sent", word_count, trending, keeping_track, old_words)

		word_count = updateWordCount(sr_words, "received", word_count, trending, keeping_track, old_words)

		# print ss
		# print sr
		# print "+++++ one sentence at a time +++++"

		for word in word_count:
			# print len(word_count[word])
			if len(word_count[word]) == 2:
				# print "yeah both"
				# print word
				count = 0
				for speaker in word_count[word]:
					# print speaker, word_count[word][speaker]
					count += word_count[word][speaker]
				# print "->", count 
				if count > 3:
					# print "word", word, "appeared", count, "times!"
					word_found = True
					chosen_word = word


		if word_found:
			break

	# pprint(word_count)
	# print chosen_word
	title = title + " " + chosen_word
	# pprint(checked_sentences)
	applicable_sentences = dict()
	applicable_sentences["sent"] = list()
	applicable_sentences["received"] = list()
	
	for s in checked_sentences["sent"]:
		words = s.split()
		if chosen_word in words:
			applicable_sentences["sent"].append(s)
	for s in checked_sentences["received"]:
		words = s.split()
		if chosen_word in words:
			applicable_sentences["received"].append(s)
	# pprint(applicable_sentences)

	sentSelected = random.choice(applicable_sentences["sent"])
	receivedSelected = random.choice(applicable_sentences["received"])
	selected["sent"].append(sentSelected)
	selected["received"].append(receivedSelected)
	# pprint(selected)
	keeping_track["words_used"].add(chosen_word)
	keeping_track["sentences_used"].add(sentSelected)
	keeping_track["sentences_used"].add(receivedSelected)

	# ---------------

	word_count = dict()
	word_found = False
	old_words.add(chosen_word)
	chosen_word = ""
	checked_sentences = dict()
	checked_sentences["sent"] = set()
	checked_sentences["received"] = set()
	for i in range(looplength):
		ss = SENT_A[i][0] if SENT_A[i][0] not in keeping_track["sentences_used"] else ""
		checked_sentences["sent"].add(ss)
		sr = RECEIVED_A[i][0] if RECEIVED_A[i][0] not in keeping_track["sentences_used"] else ""
		checked_sentences["received"].add(sr)


		ss_words = ss.split()
		sr_words = sr.split()

		word_count = updateWordCount(ss_words, "sent", word_count, trending, keeping_track, old_words)

		word_count = updateWordCount(sr_words, "received", word_count, trending, keeping_track, old_words)

		# print ss
		# print sr
		# print "+++++ one sentence at a time +++++"

		for word in word_count:
			# print len(word_count[word])
			if len(word_count[word]) == 2:
				# print "yeah both"
				# print word
				count = 0
				for speaker in word_count[word]:
					# print speaker, word_count[word][speaker]
					count += word_count[word][speaker]
				# print "->", count 
				if count > 3:
					# print "word", word, "appeared", count, "times!"
					word_found = True
					chosen_word = word


		if word_found:
			break

	# pprint(word_count)
	# print chosen_word
	title = title + " " + chosen_word
	# pprint(checked_sentences)
	applicable_sentences = dict()
	applicable_sentences["sent"] = list()
	applicable_sentences["received"] = list()
	
	for s in checked_sentences["sent"]:
		words = s.split()
		if chosen_word in words:
			applicable_sentences["sent"].append(s)
	for s in checked_sentences["received"]:
		words = s.split()
		if chosen_word in words:
			applicable_sentences["received"].append(s)
	# pprint(applicable_sentences)

	sentSelected = random.choice(applicable_sentences["sent"])
	receivedSelected = random.choice(applicable_sentences["received"])
	selected["sent"].append(sentSelected)
	selected["received"].append(receivedSelected)
	# pprint(selected)
	keeping_track["words_used"].add(chosen_word)
	keeping_track["sentences_used"].add(sentSelected)
	keeping_track["sentences_used"].add(receivedSelected)

	# ------------------
	print "-"*10, "\n"
	print "~", title, "~\n"
	# pprint(selected)
	for i in range(3):
		random_s = random.choice(selected["sent"]) 
		print random_s
		selected["sent"].remove(random_s);

		random_s = random.choice(selected["received"]) 
		print "\t\t\t\t", random_s
		selected["received"].remove(random_s);
	print "\n", "-"*10, "\n"



	return keeping_track










