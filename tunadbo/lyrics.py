#lyrics grabber test
import urllib2
class lyrics:
	@staticmethod
	def getLyrics(url):
		webpage = urllib2.urlopen(url)
		output = []
		lyrics = False
		for line in webpage:
			if "<!-- end of lyrics -->" in line:
				lyrics = False
				break;
			if lyrics and line is not None:
				line = replace(line)
				output.append(line)
				print output[-1]
			if "<!-- start of lyrics" in line:
				lyrics = True
		return output
	#implemented from the AZlyrics search function
	def search(self, keywords):
		query = "http://search.azlyrics.com/search.php?q="+keywords
		page = urllib2.urlopen(query)
		output = {}
		key = ""
		temp = []
		results = False
		for line in page:
			if "no results." in line:
				output.append("no results")
				break;
			if "Artist results" in line:
				if len(temp) > 0:
					output[key] = temp
				temp = []
				key = "artist"
				results = True
			elif "Album results" in line:
				if len(temp) > 0:
					output[key] = temp
				temp = []
				key = "album"
				results = True
			elif "Song results" in line:
				if len(temp) > 0:
					output[key] = temp
				temp = []
				key = "song"
				results = True
			if results:
				if "<a href" in line and "lyrics" in line:
					firstIdx = line.index("\"") +1
					secIdx = line.find("\"", firstIdx)
					temp.append(line[firstIdx:secIdx])
		if len(temp) > 0:
			output[key] = temp
		for key in output:
			print key +"=> key"
			for k in output[key]:
				print k
		return output

	def replace(string):
		chars = ["<br />\n", "<i>", "</i>", "<a href =\""]
		for char in chars:
			string = string.replace(char, "")
		return string
	def arbitraryScale(lyrics):
		count = 0
		for line in lyrics:
			if "kid" in line.lower():
				count +=1
		return count
	def test():
		lyrics = getLyrics("http://www.azlyrics.com/lyrics/kendricklamar/goodkid.html")
		print arbitraryScale(lyrics)


