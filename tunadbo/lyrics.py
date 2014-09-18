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
	def search(keywords):
		stri
		query = "http://search.azlyrics.com/search.php?q="+string
		fille = urlib2.urlopen(url)
		output = []
		for line in fille:
			if "no results." in line:
				output.append("no results")
				break;

	def replace(string):
		chars = ["<br />\n", "<i>", "</i>"]
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

