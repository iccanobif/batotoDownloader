import sys
import os.path
import urllib.request
import re
import io
import gzip
import time
from zipfile import ZipFile
from bs4 import BeautifulSoup
from PySide import QtCore

class Chapter:
	def __init(self):
		self.title = ""
		self.link = ""
		self.language = ""
		self.groupName = ""

class MangaDownloader(QtCore.QObject):
	
	logWritten = QtCore.Signal(str)
	
	def log(self, text):
		self.logWritten.emit(text)
	
	def printError(self):
		self.log("Error at line", sys.exc_info()[2].tb_lineno, ":", sys.exc_info()[1])
	
	def getHtml(self, url):
		#self.log("downloading " + url)
		req = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11", "Accept-Encoding": "gzip"}))
		bi = io.BytesIO(req.read())
		gf = gzip.GzipFile(fileobj=bi, mode="rb")
		output = gf.read()
		req.close()
		return output
	
	def getChapterList(self, url):
		html = self.getHtml(url)
		output = []
		soup = BeautifulSoup(html)
		rows = soup.find(class_="chapters_list").find_all("tr")
		i = 0
		
		for tr in rows:
			cols = tr.find_all("td")
			if (len(cols) == 0):
				continue #it's the header
			if (cols[0].a == None):
				continue
			
			c = Chapter()
			c.id = i
			c.link = cols[0].a["href"]
			c.title = cols[0].a.text.strip()
			c.language = cols[1].div["title"]
			c.groupName = cols[2].a.text.strip()
			output.append(c)
			
			i += 1
		return output
	
	def getImageUrl(self, html):
		soup = BeautifulSoup(html)
		return soup.find(id="comic_page")["src"]
		
	def downloadPicture(self, chapterUrl, downloadDir):
		filename = downloadDir + "\\" + chapterUrl[chapterUrl.rfind("/") + 1:]
		#self.log(filename)
		if os.path.isfile(filename):
			self.log("Warning: this file already exists. I won't re-download it")
			return
		req = urllib.request.urlopen(chapterUrl)
		content = req.read()
		f = open(filename, "wb")
		f.write(content)
		f.close()
		
	def downloadChapter(self, chaptersListUrl, downloadDir, saveToZip):
		if downloadDir[-1:] == '\\':
			downloadDir = downloadDir[0:-1]
			
		chaptersListHtml = self.getHtml(chaptersListUrl)
		soup = BeautifulSoup(chaptersListHtml)
		numberOfPages = len(soup.find(id="page_select").find_all("option"))
		self.log("Page 1 out of " + str(numberOfPages))
		
		self.downloadPicture(self.getImageUrl(chaptersListHtml), downloadDir)
		
		for i in range(2, numberOfPages + 1):
			try:
				chapterUrl = chaptersListUrl + "/" + str(i)
				self.log("Page " + str(i) + " out of " + str(numberOfPages))
				pageHtml = self.getHtml(chapterUrl)
				self.downloadPicture(self.getImageUrl(pageHtml), downloadDir)
			except:
				self.printError()
		
		if saveToZip:
			self.log("Zipping...")
			zip = ZipFile(downloadDir + ".zip", "w")
			for fileName in os.listdir(downloadDir):
				f = open(downloadDir + "\\" + fileName, "rb")
				zip.writestr(fileName, f.read())
				f.close()
				os.remove(downloadDir + "\\" + fileName)
			zip.close()
			os.removedirs(downloadDir)
		self.log("Chapter done! Saved to " + downloadDir)
	
	def fakeJob(self):
		self.log("START JOB")
		for i in range(0, 20):
			time.sleep(0.1)
			self.log("working " + str(i) + "...")
		self.log("DONE")
