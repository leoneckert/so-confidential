from datetime import datetime
from pprint import pprint

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







