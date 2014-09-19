#lyrics grabber test
#from google.appengine.api import urlfetch
import urllib2
class lyrics:
	@staticmethod
	def getLyrics(url):
		#urllib2
		webpage = urllib2.urlopen(url)
		'''urlfetch method
		server = urlfetch.fetch(url)
		webpage = server.content
		'''
		output = []
		lyrs = False
		for line in webpage:
			if lyrs and "</div>" in line:
				break;
			if lyrs and line is not None:
				line = lyrics.replace(line)
				output.append(line)
			if (not lyrs) and "id=\"songLyricsDiv-outer\"" in line:
				lyrs = True
		return output
	#implemented from the AZlyrics search function
	def search(self, keywords):
		query = "http://search.azlyrics.com/search.php?q="+keywords
		page = "asd"
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
	@staticmethod
	def replace(string):
		chars = ["<a href =\"", "\n"]
		iterator = 0
		endchar = 0
		for char in chars:
			string = string.replace(char, "")
		while iterator < len(string):
			if string[iterator] == "<":
				endchar = string.find(">")
				if endchar != -1:
					string = string[:iterator]+string[endchar+1:]
					iterator-=1
			iterator+=1
		return string
	@staticmethod
	def arbitraryScale(lyrics):
		count = 0
		for line in lyrics:
			if "gas" in line.lower():
				count +=1
		return count
	def test():
		lyrics = getLyrics("www.azlyrics.com/lyrics/kanyewest/canttellmenothing.html")
		print arbitraryScale(lyrics)
lyrics.getLyrics("http://www.songlyrics.com/kanye-west/can-t-tell-me-nothing-lyrics/")
