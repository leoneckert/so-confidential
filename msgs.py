import operator
from textblob import TextBlob, Word

def wordTally(db):
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
	output = list()
	SortedwordsTally2 = sorted(tally.items(), key=lambda x: (-x[1], x[0]))
	for i in SortedwordsTally2:
		tempList = list()
		tempList.append(i[0])
		tempList.append(i[1])
		output.append(tempList)
	
	return output
		
