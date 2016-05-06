from datetime import datetime

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

def getCommonIndeces(indexSet1, indexSet2):
	output = set()
	for n in indexSet1:
		if n in indexSet2:
			output.add(n)
	return output