#lyrics grabber test
#from google.appengine.api import urlfetch
import urllib2
import logging

from google.appengine.ext import db
from google.appengine.api import users
VS_NUM = 1
class Tune(db.Model):
    idd = db.StringProperty(required=True)
    version = db.IntegerProperty(required=True)
    title = db.StringProperty(required=True)
    artist = db.StringProperty(required=True)
    scale = db.FloatProperty(required=True)
    popularity = db.IntegerProperty(required=True)

class Lyrics:
	#proposal: alternative option to load from Tune database
	def __init__(self, url):
		self.webpage = urllib2.urlopen(url)
		artist = "Error"
		title = "Error"
		output = []
		artistB = False
		titleB = False
		lyricsB = False
		lyrs = False
		for line in self.webpage:
			if not artistB and "Artist: " in line:
				artist = Lyrics.replace(line, False)
				artist = artist[artist.find(":")+2:]
				artistB = True
			if not titleB and 'meta property="og:title"' in line:
				title=line
				title = title.split('"')[3]
				title = title[:title.find("-")-1]
				titleB = True
			#why this may be called
			if lyrs and "</div>" in line:
				lyrs = False
				lyricsB = True
			if lyrs and line is not None:
				line = Lyrics.replace(line)
				output.append(line)
			if (not lyrs) and "id=\"songLyricsDiv-outer\"" in line:
				lyrs = True
			if titleB and artistB and lyricsB:
				break;
		self.lyrics = output	
		self.artist = artist
		self.title = title
		self.score = Lyrics.getScore(lyrs=self.lyrics)
	@staticmethod
	def getLyrics(url=None, webpage=None):
		output = []
		if webpage is None:
			webpage = urllib2.urlopen(url)
		lyrs = False
		for line in webpage:
			if lyrs and "</div>" in line:
				break;
			if lyrs and line is not None:
				line = Lyrics.replace(line)
				output.append(line)
			if (not lyrs) and "id=\"songLyricsDiv-outer\"" in line:
				lyrs = True
		return output
	@staticmethod
	def getArtist(url=None, webpage=None):
		artist = "Error"
		for line in webpage:
			if "Artist: " in line:
				artist = Lyrics.replace(line, False)
				artist = artist[artist.find(":")+2:]
		return artist
	@staticmethod
	def getTitle(url=None, webpage=None):
		if webpage is None:
			webpage = urllib2.urlopen(url)
		lyrs = False
		title = "Error"
		for line in webpage:
			if 'meta property="og:title"' in line:
				title=line
				title = title.split('"')[3]
				title = title[:title.find("-")-1]
		return title
	@staticmethod
	def getScore(url=None, webpage=None, lyrs=None):
		if lyrs is None:
			if webpage is None:
				webpage = urllib2.urlopen(url)
			lyrs = Lyrics.getLyrics(webpage=webpage)
		count = 0
		for line in lyrs:
			if "it" in line.lower():
				count +=1
		return count
	#We should expand this function to pull more results if prompted
	@staticmethod
	def search(searchline, page = 1):
		line = Lyrics.formatSearch(searchline)
		query = "http://www.songlyrics.com/index.php?section=search&searchW="+line+"&submit=Search"

		if page != 1:
			query = "http://www.songlyrics.com/index.php?section=search&searchIn1=artist&searchIn2=album&searchIn3=song&searchIn4=lyrics&searchW="+line+"&pageNo="+str(page)
		webpage = urllib2.urlopen(query)
		

		#Make sure it is not reading unecessailry
		reading = False
		artdone = False
		output = {}
		count = 0
		for line in webpage:
			if "<div class=\"coltwo-wide-2\">" in line:
				reading = True
			if reading and not artdone and "<a href" in line and "<img" in line and "title" in line:
				idx = line.find("href=\"")+len("href=\"")
				link = line[idx:line.find('\"',idx)]
				titx = line.find("title=\"")+len("title=\"")
				title = line[titx:line.find('"',idx)]
				idd = link.replace('http://www.songlyrics.com/', '')
				output.update(
					{str(count): {'id': idd,
					'version': VS_NUM,
					'title': title,
					'artist': None,
					'scale': float(0),
					'popularity': 1}})
				artdone = True
			if reading and artdone and "<p>by " in line:
				artx = line.find("\">")+len("\">")
				artist = line[artx:line.find("</a> ")]
				output[str(count)]['artist'] = artist
				count+= 1
				artdone = False

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
	
#Lyrics.getLyrics("http://www.songlyrics.com/kanye-west/can-t-tell-me-nothing-lyrics/")
#print Lyrics.search("kendrick lamar")
print Lyrics.search("kendrick+lamar")