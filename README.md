# so confidential
#in progress

included alternative approach using python's sqlite3 library. the approach is commented out in mdb.py. I commented it out because right now the other one works well and I am not yet sure as to what the advantage of sqlite library over a subprocess call is. 

---

current plan:
find trending SENT words over time > list
find trending RECEIVED words over time > list

go through all SENT sentences tallying by how many trend words they contain
go through all RECEIVED sentences tallying by how many trend words they contain

order tallies (restrict length of sentences)

go through tallies fro top counting trend words. Once one word is seen 5 times, grab these five (10 if done for both SENT and RECEIVED) sentences.

print all ten sentences left right for RECEIVED and SENT

chosen trend word is the title

// find a way to include randomness (trending screw can be turned too) and a preference of recent sentences



 Start with for loop to find the sweet spots for the trending word values. Also return blacklist. Use blacklist also when evaluating the sentences (trending word plus blacklist word minus)