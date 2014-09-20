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
	def searchAz(self, keywords):
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
	def getArtist(url):
		webpage = urllib2.urlopen(url)
		reading = False
		artist = "Error"
		for line in webpage:
			if "Artist: " in line:
				artist = lyrics.replace(line, False)
				artist = artist[artist.find(":")+2:]
		return artist

	@staticmethod
	def getTitle(url):
		webpage = urllib2.urlopen(url)
		reading = False
		title = "Error"
		for line in webpage:
			if 'meta property="og:title"' in line:
				title=line
				title = title.split('"')[3]
				title = title[:title.find("-")-1]
		return title

	@staticmethod
	def search(searchline):
		line = lyrics.formatSearch(searchline)
		query = "http://www.songlyrics.com/index.php?section=search&searchW="+line+"&submit=Search"
		webpage = urllib2.urlopen(query)
		#Make sure it is not reading unecessailry
		reading = False
		output = {}
		for line in webpage:
			if "<div class=\"coltwo-wide-2\">" in line:
				reading = True
			if reading and "<a href" in line and "<img" in line and "title" in line:
				idx = line.find("href=\"")+len("href=\"")
				link = line[idx:line.find('\"',idx)]
				idx = line.find("title=\"", idx) +len("title=\"")
				title = line[idx:line.find('\"',idx)]
				title =title.replace("\r", "")
				output[title] = link
			if "<! --end coltwo-center-->" in line:
				print "break"
				break;
		return output

	@staticmethod
	def formatSearch(query):
		while " " in query:
			query = query.replace(" ", "+")
		return query
	@staticmethod
	def replace(string, ahref = True):
		chars = ["<a href =\"", "\n"]
		iterator = 0
		endchar = 0
		if ahref:
			for char in chars:
				string = string.replace(char, "")
		else:
			string = string.replace(chars[1], "")
		while iterator < len(string):
			if string[iterator] == "<":
				endchar = string.find(">")
				if endchar != -1:
					string = string[:iterator]+string[endchar+1:]
					iterator-=1
			iterator+=1
		return string
	@staticmethod
	def arbitraryScale(url):
		lyrs = lyrics.getLyrics(url)
		count = 0
		for line in lyrs:
			if "it" in line.lower():
				count +=1
		return count
#lyrics.getLyrics("http://www.songlyrics.com/kanye-west/can-t-tell-me-nothing-lyrics/")
#print lyrics.search("kendrick lamar")
print lyrics.getArtist("http://www.songlyrics.com/kendrick-lamar/poetic-justice-lyrics/")