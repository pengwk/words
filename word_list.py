
# with open("cet6.csv", 'r') as cet:
# 	words = []
# 	for line in cet.readlines():
# 		if len(line) > 2:
# 			words.append(line[1:-1])
# 	print len(words)
# 	import json
# 	with open("cet_clean.json", "w") as f:
# 		json.dump(words, f)
import json
with open("cet_clean.json", "r") as f:
	print type(set(json.load(f)))
path = "E:\sparks\youtube_word\words\cet6.txt"

