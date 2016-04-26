import operator
from textblob import TextBlob, Word
import math
from datetime import datetime
def wordTally(db):
	# use like this: word_tally = msgs.wordTally(db)
	allwords = dict()

	for person in db:
		for convo in db[person]:
			for text_data in db[person][convo]:
				sentence = text_data[0].decode('utf8')
				blob = TextBlob(sentence)
				sent = blob.sentences
				for s in sent:
					for word in s.words:
						if word.lower() not in allwords:
							allwords[word.lower()] = 0
						allwords[word.lower()] += 1 
	return allwords

def orderTally(tally):
	""" use like this:
	word_tally = msgs.wordTally(db)
	word_tally = msgs.orderTally(word_tally) """

	output = list()
	SortedwordsTally2 = sorted(tally.items(), key=lambda x: (-x[1], x[0]))
	for i in SortedwordsTally2:
		tempList = list()
		tempList.append(i[0])
		tempList.append(i[1])
		output.append(tempList)
	
	return output
		
def returnAllTexts(db):
	all_texts = list()
 	for person in db:
		for convo in db[person]:
			for text_data in db[person][convo]:
				if(len(text_data[0]) > 0):
					all_texts.append(text_data[0])
	return all_texts	


# --


def returnAllSentences(db):
	all_sentences = list()
	for person in db:
		for convo in db[person]:
			for text_data in db[person][convo]:
				if(len(text_data[0]) > 0):
					blob = TextBlob(text_data[0].decode('utf8'))
					speaker = text_data[1]
					time = text_data[2]
					for sentence in blob.sentences:
						tempList = list()
						tempList.append(sentence)
						tempList.append(speaker)
						tempList.append(time)
						all_sentences.append(tempList)
	return all_sentences


def getTimeRange(db):
	latest = 0
	earliest = 0
	first = True
	for person in db:
		for convo in db[person]:
			for text_data in db[person][convo]:
				if first:
					first = False
					earliest = text_data[2]
					earliesttext = text_data[0]
				if text_data[2] > latest:
					latest = text_data[2]
					latesttext = text_data[0]
				if text_data[2] < earliest:
					earliest = text_data[2]
					earliesttext = text_data[0]	
	tempList = list()
	tempList.append(int(earliest))
	tempList.append(int(latest))
	return tuple(tempList)

def returnRandomSentence(db):
	ss = returnAllSentences(db)
	return random.sample(ss, 1)[0]

def returnRandomRecentSentence(db, recent_factor):
	factor = recent_factor # the higher the higher the probability for recent sentences
	topTime = float(getTimeRange(db)[1] - getTimeRange(db)[0]) 

	ss = returnAllSentences(db)
	random_sentence = random.sample(ss, 1)[0]
	random_sentence_time = float(random_sentence[2]) - float(getTimeRange(db)[0])

	c = 0
	while random.random() < 1 - (math.pow((random_sentence_time / topTime), factor)):
		# print c
		c += 1
		random_sentence = random.sample(ss, 1)[0]
		random_sentence_time = float(random_sentence[2]) - float(getTimeRange(db)[0])
	return random_sentence


def returnRandomRecentConvo(db, recent_factor):
	factor = recent_factor
	topTime = float(getTimeRange(db)[1] - getTimeRange(db)[0]) 

	randomPerson = random.sample(db, 1)
	# print "random person: " + str(randomPerson)
	randomConvo = random.sample(db[randomPerson[0]], 1)
	# print "random convo: " + str(randomConvo) 
	# print db[randomPerson[0]][randomConvo[0]]

	random_sentence_time = float(db[randomPerson[0]][randomConvo[0]][0][2]) - float(getTimeRange(db)[0])
	
	c = 0
	while random.random() < 1 - (math.pow((random_sentence_time / topTime), factor)):

		c += 1
		randomPerson = random.sample(db, 1)
		# print "random person: " + str(randomPerson)
		randomConvo = random.sample(db[randomPerson[0]], 1)
		random_sentence_time = float(db[randomPerson[0]][randomConvo[0]][0][2]) - float(getTimeRange(db)[0])
	# pprint(db[randomPerson[0]][randomConvo[0]])

	return db[randomPerson[0]][randomConvo[0]]






def returnRandomConvo(db):
	output = list()
	randomPerson = random.sample(db, 1)
	# print "random person: " + str(randomPerson)
	randomConvo = random.sample(db[randomPerson[0]], 1)
	# print "random convo: " + str(randomConvo) 
	for elem in db[randomPerson[0]][randomConvo[0]]:
		output.append(elem)
	return output




def returnRandomText(db):
	outputLines = ""
	randomPerson = random.sample(db, 1)
	# print "random person: " + str(randomPerson)
	randomConvo = random.sample(db[randomPerson[0]], 1)
	# print "random convo: " + str(randomConvo) 
	randomElem = random.sample(db[randomPerson[0]][randomConvo[0]], 1)
	return randomElem[0][0]












#from here: https://github.com/aparrish/rwet-examples/blob/master/ngrams/ngramcount.py
def count_ngrams(tokens, n):
	"""Returns a dictionary mapping tuples of n-grams with order n to the number
		of times that n-gram occurred in list tokens."""
	ngrams = dict()
	if len(tokens) < n:
		return ngrams
	for i in range(len(tokens) - n + 1):
		ngram = tuple(tokens[i:i+n])
		if ngram not in ngrams:
			ngrams[ngram] = 0
		ngrams[ngram] += 1
	return ngrams

#from here: https://github.com/aparrish/rwet-examples/blob/master/ngrams/ngramcount.py
def build_model(tokens, n):
	"Builds a Markov model from the list of tokens, using n-grams of length n."
	model = dict()
	if len(tokens) < n:
		return model
	for i in range(len(tokens) - n):
		gram = tuple(tokens[i:i+n])
		next_token = tokens[i+n]
		if gram in model:
			model[gram].append(next_token)
		else:
			model[gram] = [next_token]
	final_gram = tuple(tokens[len(tokens)-n:])
	if final_gram in model:
		model[final_gram].append(None)
	else:
		model[final_gram] = [None]
	return model

import random
def generate(model, n, seed=None, max_iterations=100):
	"""Generates a list of tokens from information in model, using n as the
		length of n-grams in the model. Starts the generation with the n-gram
		given as seed. If more than max_iteration iterations are reached, the
		process is stopped. (This is to prevent infinite loops)""" 
	if seed is None:
		seed = random.choice(model.keys())
	output = list(seed)
	current = tuple(seed)
	for i in range(max_iterations):
		if current in model:
			possible_next_tokens = model[current]
			next_token = random.choice(possible_next_tokens)
			if next_token is None: break
			output.append(next_token)
			current = tuple(output[-n:])
		else:
			break
	return output


def returnDatetime(mac_timestamp):
	return str(datetime.fromtimestamp(int(mac_timestamp) + 978307205))



