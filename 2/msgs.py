from datetime import datetime
from pprint import pprint
import random
import math
from textblob import TextBlob, Word
import enchant

def returnDatetime(mac_timestamp):
	return str(datetime.fromtimestamp(int(mac_timestamp) + 978307200))

def orderTally(tally):
	# turns a dict() tally into a ordered list() tally
	output = list()
	SortedwordsTally2 = sorted(tally.items(), key=lambda x: (-x[1], x[0]))
	for i in SortedwordsTally2:
		tempList = list()
		tempList.append(i[0])
		tempList.append(i[1])
		output.append(tempList)
	return output

def printHeadline():
	# print "                              _       _        "
	# print " _   _  ___  _   _ _ __    __| | __ _| |_ __ _ "
	# print "| | | |/ _ \| | | | '__|  / _` |/ _` | __/ _` |"
	# print "| |_| | (_) | |_| | |    | (_| | (_| | || (_| |"
	# print " \__, |\___/ \__,_|_|     \__,_|\__,_|\__\__,_|"
	# print " |___/                                         "


	# print " _                                            _ "
	# print "(_)___    __ _  ___ ___ ___  ___ ___  ___  __| |"
	# print "| / __|  / _` |/ __/ __/ _ \/ __/ __|/ _ \/ _` |"
	# print "| \__ \ | (_| | (_| (_|  __/\__ \__ \  __/ (_| |"
	# print "|_|___/  \__,_|\___\___\___||___/___/\___|\__,_|"

	print "                                                _     "
	print " _   _  ___  _   _ _ __  __      _____  _ __ __| |___ "
	print "| | | |/ _ \| | | | '__| \ \ /\ / / _ \| '__/ _` / __|"
	print "| |_| | (_) | |_| | |     \ V  V / (_) | | | (_| \__ \\"
	print " \__, |\___/ \__,_|_|      \_/\_/ \___/|_|  \__,_|___/"
	print " |___/                                                "


def rateSentences(sentences, trendingBlacklist, maxSentenceLength = 10000, minSentenceLength=0, sender_id = 2):
	rated = dict()
	metadata = dict()
	trending = trendingBlacklist["trending"]
	blacklist = trendingBlacklist["blacklist"]
	
	notWantedChars = set('!"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~')

	for sentence_data in sentences:
		
		sentence = sentence_data[0]
		speaker = int(sentence_data[1])
		person = int(sentence_data[2])
		date = int(sentence_data[3])
		temp_meta_list = [speaker, person, date]

		if sentence not in rated:
			words = sentence.split()
			rated[sentence] = 0.0
			metadata[sentence] = temp_meta_list
			# print sentence, 
			for word in words:

				if len(word) > 1:
					while word[0] in notWantedChars:
						word = word[1:]
						if len(word) < 2: break
					while word[-1] in notWantedChars:
						word = word[:-1]
						if len(word) < 1: break

				if word in trending:
					rated[sentence] += 100 - 100.0/len(words)
					# print " + " + str(100 - 100.0/len(words)), 

				if word in blacklist:
					rated[sentence] -= 100.0/len(words)
					# print " - " + str(100.0/len(words)),
			# print " ->", rated[sentence] 
	rated_ordered = orderTally(rated)

	aRated = list()
	bRated = list()
	c = 0
	for s in rated_ordered:
		score = s[1]
		sentence = s[0]
		if score > 0 and len(sentence) <= maxSentenceLength and len(sentence) >= minSentenceLength:
			temp_list = list()
			temp_list = [sentence, metadata[sentence][0], metadata[sentence][1], metadata[sentence][2] ]
			aRated.append(temp_list)
			# print c, "-", sentence, score
			c += 1
		elif score <= 0 and len(sentence) <= maxSentenceLength and len(sentence) >= minSentenceLength:

			words  = sentence.split()
			trend = False
			num = 0
			for word in words:
				if word in trending:
					trend = True
					num += 1
			if trend:
				# print "\t\t\t\t", c, "-", s[0], s[1], num
				temp_list = list()
				temp_list = [sentence, metadata[sentence][0], metadata[sentence][1], metadata[sentence][2] ]
				bRated.append(temp_list)
				c += 1

	if sender_id == 1:
		print "[+] rated all SENT sentences based on the trending and blacklisted words they contain."
	elif sender_id == 0:
		print "[+] rated all RECEIVED sentences based on the trending and blacklisted words they contain."
	else:
		print "[+] rated ALL sentences based on the trending and blacklisted words they contain."
	print "[ ] compiled two ordered lists:"
	print "\t> Only sentences with (as specified) up to", maxSentenceLength, " and at least", minSentenceLength, "characters are considered."
	print "\t> A-rated sentences:", len(aRated), "sentences (with a rating higher than 0)."
	print "\t> B-rated sentences:", len(bRated), "sentences (that contain trending words, yet still have a rating of 0 or lower)."

	return {"aRated":aRated, "bRated":bRated}


def getEarliestLatestDate(sentenceDataList):
	earliestDate = 0
	latestDate = 0
	first = True
	for sentence_data in sentenceDataList:
		date = sentence_data[3]
		if first == True:
			first = False
			earliestDate = date
		if date < earliestDate:
			earliestDate = date
		
		if date > latestDate:
			latestDate = date
	return [earliestDate, latestDate]


def shuffleWithDateAndRating(aRatedbRatedList):
	# only the arated list is gonna be shuffled here
	aRatedbRatedListCOPY = dict()
	
	data_list = list()
	for elem in aRatedbRatedList["aRated"]:
		data_list.append(elem)

	shuffled = list()
	
	while len(data_list) > 0:
		
		realEarliestDate = getEarliestLatestDate(data_list)[0] * 1.0
		realLatestDate = getEarliestLatestDate(data_list)[1] * 1.0
		maxDate = realLatestDate - realEarliestDate
		count = 0.0
		to_delete = list()
		
		for sentence_data in data_list:
			realDate = sentence_data[3]
			date = realDate - realEarliestDate
			# print date/maxDate
			if date == 0: date = 1
			if maxDate == 0: maxDate = date
			# if random() < 0.833 - count/(len(data_list)*1.2) and random() < (math.pow(date/maxDate, 3)):
			# if random() < 1:
			if random.random() < (math.pow(date/maxDate, 2)):
				shuffled.append(sentence_data)
				to_delete.append(sentence_data)
			count += 1


		#delete here:
		for used in to_delete:
			data_list.remove(used)


	return {"aRated":shuffled, "bRated":aRatedbRatedList["bRated"]}


# def generatePoem(SENTshuffled_aRatedbRatedList, RECEIVEDshuffled_aRatedbRatedList):
# 	SENT_A = SENTshuffled_aRatedbRatedList["aRated"]
# 	SENT_B = SENTshuffled_aRatedbRatedList["bRated"]
# 	RECEIVED_A = RECEIVEDshuffled_aRatedbRatedList["aRated"]
# 	RECEIVED_B = RECEIVEDshuffled_aRatedbRatedList["bRated"]

# 	# wordCollections = dict()
# 	nouns = dict()
# 	verbs = dict()
# 	adjectives = dict()

# 	for sentence_data in SENT_A:

# 		text = sentence_data[0]

# 		for word, tag in text.tags:
# 			if tag.startswith("NN"): 
# 				if word not in nouns:
# 					nouns[word] = dict()
# 					nouns[word]["sent"] = dict()
# 					nouns[word]["received"] = dict() 
# 				if text not in nouns[word]["sent"]:
# 					nouns[word]["sent"][text] = 0
# 				nouns[word]["sent"][text] += 1

# 			if tag.startswith("VB"): 
# 				if word not in verbs:
# 					verbs[word] = dict()
# 					verbs[word]["sent"] = dict()
# 					verbs[word]["received"] = dict() 
# 				if text not in verbs[word]["sent"]:
# 					verbs[word]["sent"][text] = 0
# 				verbs[word]["sent"][text] += 1

# 			if tag.startswith("JJ"): 
# 				if word not in adjectives:
# 					adjectives[word] = dict()
# 					adjectives[word]["sent"] = dict()
# 					adjectives[word]["received"] = dict() 
# 				if text not in adjectives[word]["sent"]:
# 					adjectives[word]["sent"][text] = 0
# 				adjectives[word]["sent"][text] += 1

# 		# or tag.startswith("VB") or tag.startswith("JJ"):

# 	for sentence_data in RECEIVED_A:

# 		text = sentence_data[0]

# 		for word, tag in text.tags:
# 			if tag.startswith("NN"): 
# 				if word not in nouns:
# 					nouns[word] = dict()
# 					nouns[word]["received"] = dict()
# 					nouns[word]["sent"] = dict()
# 				if text not in nouns[word]["received"]:
# 					nouns[word]["received"][text] = 0
# 				nouns[word]["received"][text] += 1

# 			if tag.startswith("VB"): 
# 				if word not in verbs:
# 					verbs[word] = dict()
# 					verbs[word]["received"] = dict()
# 					verbs[word]["sent"] = dict()
# 				if text not in verbs[word]["received"]:
# 					verbs[word]["received"][text] = 0
# 				verbs[word]["received"][text] += 1

# 			if tag.startswith("JJ"): 
# 				if word not in adjectives:
# 					adjectives[word] = dict()
# 					adjectives[word]["received"] = dict()
# 					adjectives[word]["sent"] = dict()
# 				if text not in adjectives[word]["received"]:
# 					adjectives[word]["received"][text] = 0
# 				adjectives[word]["received"][text] += 1




# 	# pprint(nouns)
# 	available_nouns = list()
# 	available_verbs = list()
# 	available_adjectives = list()


# 	print "-"*400
# 	for w in nouns:
# 		if len(nouns[w]["sent"]) > 0 and len(nouns[w]["received"]) > 0 and len(nouns[w]["sent"]) + len(nouns[w]["received"]) > 3:
# 			# print w
# 			# pprint(nouns[w])
# 			# print "-"*40 
# 			available_nouns.append(w)

# 	for w in verbs:
# 		if len(verbs[w]["sent"]) > 0 and len(verbs[w]["received"]) > 0 and len(verbs[w]["sent"]) + len(verbs[w]["received"]) > 3:
# 			# print w
# 			# pprint(verbs[w])
# 			# print "-"*40 
# 			available_verbs.append(w)

# 	for w in adjectives:
# 		if len(adjectives[w]["sent"]) > 0 and len(adjectives[w]["received"]) > 0 and len(adjectives[w]["sent"]) + len(adjectives[w]["received"]) > 3:
# 			# print w
# 			# pprint(adjectives[w])
# 			# print "-"*40 
# 			available_adjectives.append(w)

# 	# print available_nouns
# 	# print available_verbs
# 	# print available_adjectives

# 	sent_needed = 10
# 	received_needed = 10

# 	notWantedNouns = ('i', 'u','you','ich','we','they', 'i\'m', 'i\u2019m', '\xe5')
# 	notWantedVerbs = ('have', 'be', 'do', 'i', 'go', 'get')

# 	d = enchant.Dict("en_US")
# 	while sent_needed > 0 or received_needed > 0:
# 		sent_needed = 10
# 		received_needed = 10

# 		random_noun = random.choice(available_nouns)
# 		# while random_noun.lower() in notWantedNouns:
# 		# 	random_noun = random.choice(available_nouns)
# 		try:
# 			while d.check(random_noun) is False or random_noun.lower() in notWantedNouns:
# 				# print random_noun, "is not english"
# 				random_noun = random.choice(available_nouns)
# 		except:
# 			nevermind = 1
		
# 		random_verb = random.choice(available_verbs)
# 		try:
# 			while d.check(random_verb) is False or Word(random_verb).lemmatize('v') in notWantedVerbs:
# 				# print random_verb, "is not english"
# 				random_verb = random.choice(available_verbs)
# 		except:
# 			nevermind = 1
		
# 		random_adjective = random.choice(available_adjectives)
# 		try:
# 			while d.check(random_adjective) is False:
# 				# print random_adjective, "is not english"
# 				random_adjective = random.choice(available_adjectives)
# 		except:
# 			nevermind = 1

		

# 		sent_needed -= len(nouns[random_noun]["sent"])

# 		sent_needed -= len(verbs[random_verb]["sent"])

# 		sent_needed -= len(adjectives[random_adjective]["sent"])

# 		received_needed -= len(nouns[random_noun]["received"])

# 		received_needed -= len(verbs[random_verb]["received"])

# 		received_needed -= len(adjectives[random_adjective]["received"])

# 	print "---\nTitle:"
# 	print random_noun, random_verb,random_adjective
# 	print "---\n"

	
# 	all_sentences = dict()
# 	all_sentences[random_noun] = nouns[random_noun]
# 	all_sentences[random_verb] = verbs[random_verb]
# 	all_sentences[random_adjective] = adjectives[random_adjective]

# 	pprint(all_sentences)

	
# 	# currentWord = random.choice([random_noun, random_adjective, random_adjective])
# 	currentWord = random.choice([random_noun])
	
# 	used = set()

# 	print "currentword is >", currentWord

# 	temp_list = [s for s in all_sentences[currentWord]["sent"]]
# 	print temp_list

# 	sentence1 = random.choice(temp_list)
# 	used.add(sentence1)
# 	print "\t\t\t\t",sentence1

# 	def pickSameWord(string, currentWord):
# 		print "right now:", string, "in pickSameWord()"
# 		print "currentword is >", currentWord
# 		temp_list = [s for s in all_sentences[currentWord][string] if s not in used]
# 		# what if the array is empty!
# 		if len(temp_list) < 1:
# 			print "in pickSameWord() but directing to pickDifferentWord()"
# 			sentence2 = pickDifferentWord(string, currentWord)
# 		#
# 		else:
# 			sentence2 = random.choice(temp_list)
# 		return [sentence2, currentWord]

# 	def pickDifferentWord(string, currentWord):
# 		print "right now:", string, "in pickDifferentWord()"
# 		print "currentword is >", currentWord
# 		old_word = currentWord
# 		while currentWord == old_word:
# 			currentWord = random.choice([random_noun, random_adjective, random_adjective])
# 		print "NEW currentword is >", currentWord
# 		temp_list = [s for s in all_sentences[currentWord][string] if s not in used]
# 		# what if the array is empty! cal this function again
# 		if len(temp_list) < 1:
# 			print "in pickDifferentWord() but running it again"
# 			sentence2 = pickDifferentWord(string, currentWord)
# 		#
# 		else:
# 			sentence2 = random.choice(temp_list)
# 		return [sentence2, currentWord]

# 	def letThemSpeak(string, currentWord):
# 		if random.random() < 0.8:
# 			if random.random() < 0.7:
# 				sentence2 = pickSameWord(string, currentWord)
			
# 			else:
# 				sentence2 = pickDifferentWord(string, currentWord)
				
# 			used.add(sentence2[0])
# 			if string == "received": print "\t\t\t\t\t\t\t",
# 			else: print "\t\t\t\t",
# 			print sentence2[0]
# 			return sentence2[1]
# 		else: 
# 			if random.random() < 0.7:
# 				sentence2 = pickSameWord(string, currentWord)
			
# 			else:
# 				sentence2 = pickDifferentWord(string, currentWord)
				
# 			used.add(sentence2[0])
# 			if string == "received": print "\t\t\t\t\t\t\t",
# 			else: print "\t\t\t\t",
# 			print sentence2[0]
# 			if random.random() < 0.7:
# 				sentence2 = pickSameWord(string, sentence2[1])
			
# 			else:
# 				sentence2 = pickDifferentWord(string, sentence2[1])
				
# 			used.add(sentence2[0])
# 			if string == "received": print "\t\t\t\t\t\t\t",
# 			else: print "\t\t\t\t",
# 			print sentence2[0]
# 			return sentence2[1]

# 	currentWord = letThemSpeak("received", currentWord)
# 	currentWord = letThemSpeak("sent", currentWord)
# 	currentWord = letThemSpeak("received", currentWord)
# 	currentWord = letThemSpeak("sent", currentWord)




























