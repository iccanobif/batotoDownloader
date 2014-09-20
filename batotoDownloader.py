import sys
import os.path
import urllib.request
import re
import io
import gzip
from bs4 import BeautifulSoup

def printError():
	print("Error at line", sys.exc_info()[2].tb_lineno, ":", sys.exc_info()[1])

class Chapter:
	def __init(self):
		self.title = ""
		self.link = ""
		self.language = ""
		self.groupName = ""

def getChapterList(html):
	output = []
	soup = BeautifulSoup(html)
	rows = soup.find(class_="chapters_list").find_all("tr")
	
	for tr in rows:
		cols = tr.find_all("td")
		if (len(cols) == 0):
			continue #it's the header
		if (cols[0].a == None):
			continue
		
		c = Chapter()
		c.link = cols[0].a["href"]
		c.title = cols[0].a.text.strip()
		c.language = cols[1].div["title"]
		c.groupName = cols[2].a.text.strip()
		output.append(c)

#	for i in range(len(output) - 1, -1, -1):
#		c = output[i]
#		print(c.title + " " + c.link)
	return output

def getHtml(url):
	print("downloading " + url)
	req = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11", "Accept-Encoding": "gzip"}))
	bi = io.BytesIO(req.read())
	gf = gzip.GzipFile(fileobj=bi, mode="rb")
	output = gf.read()
	req.close()
	return output

def getImageUrl(html):
	soup = BeautifulSoup(html)
	return soup.find(id="comic_page")["src"]
	
def downloadPicture(chapterUrl, downloadDir):
	filename = downloadDir + "\\" + chapterUrl[chapterUrl.rfind("/") + 1:]
	print(filename)
	if os.path.isfile(filename):
		print("Warning: this file already exists. I won't re-download it")
		return
	req = urllib.request.urlopen(chapterUrl)
	content = req.read()
	f = open(filename, "wb")
	f.write(content)
	f.close()
	
def downloadChapter(chaptersListUrl, downloadDir):
	
	chaptersListHtml = getHtml(chaptersListUrl)
	soup = BeautifulSoup(chaptersListHtml)
	numberOfPages = len(soup.find(id="page_select").find_all("option"))
	print("Page 1 out of " + str(numberOfPages))
	
	downloadPicture(getImageUrl(chaptersListHtml), downloadDir)
	
	for i in range(2, numberOfPages + 1):
		try:
			chapterUrl = chaptersListUrl + "/" + str(i)
			print("Page " + str(i) + " out of " + str(numberOfPages) + ": " + chapterUrl)
			pageHtml = getHtml(chapterUrl)
			downloadPicture(getImageUrl(pageHtml), downloadDir)
		except:
			printError()

#########
# START #
#########

if len(sys.argv) == 1:
	print(r"Usage: python batotoDownloader.py chapterUrl [targetDirectory]")
	quit()

mainUrl = sys.argv[1]

if len(sys.argv) > 2:
	outputDirectory = sys.argv[2]
else:
	outputDirectory = "."

downloadChapter(mainUrl, outputDirectory)