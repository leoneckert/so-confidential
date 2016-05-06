import msgs
from pprint import pprint
import random

def generateTimebasedPoetry(data1, data2, numPeriods = 3, numSentPerPersonPerPeriod = 2):
	# commonIndeces = msgs.getCommonIndeces(data1["populated_indeces"], data2["populated_indeces"])
	data = [("1", data1), ("2", data2)]
	# find indeces with more two or more sentences

	sets = dict()
	for index, d in data:
		# pprint(d["index_num_sentences"])
		for i in d["index_num_sentences"]:
			if d["index_num_sentences"][i] >= numSentPerPersonPerPeriod:
				if index not in sets:
					sets[index] = set()
				sets[index].add(i)

	available_indeces = list()
	for i in sets["1"]:
		if i in sets["2"]:
			available_indeces.append(i)

	if len(available_indeces) < numPeriods:
		print "could not find that many sentences for that many overlapping periods"
		return True

	indeces_picked = random.sample(available_indeces, numPeriods)
		
	# print indeces_picked 

	sentences_picked = dict()

	for i in indeces_picked:
		for index, d in data:
			# print index, i
			# pprint(d["index_word_sentence"][i])
			tmp_list = list()
			for word in d["index_word_sentence"][i]:
				for s in d["index_word_sentence"][i][word]:
					tmp_list.append(s)
			if index not in sentences_picked:
				sentences_picked[index] = list()
			for s in random.sample(tmp_list, numSentPerPersonPerPeriod):
				sentences_picked[index].append(s)
			# print "picked", sentences_picked[index]
			# print "-"
		# print "--"

	# pprint(sentences_picked)
	for index in sentences_picked:
		random.shuffle(sentences_picked[index])
	# pprint(sentences_picked)

	periods = set()
	for i in indeces_picked:
		for index, d in data:
			timestamp = d["index_date"][i]
			period = msgs.returnDatetime(timestamp)[:10]
			periods.add(period)

	title = "your words\n\n"

	print "-"*100
	print "\n\n", title
	print "points in time:",
	for p in periods:
		print p,
	print " "
	print "\n"

	for i in range((numPeriods * numSentPerPersonPerPeriod)):
		print sentences_picked["1"][i]
		print "\t\t\t", sentences_picked["2"][i]

	print "\n\n"
	print "-"*100


