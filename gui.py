import sys
import os
import re
import time
from PySide.QtCore import *
from PySide.QtGui import *
import batotoDownloader as bd

app = QApplication(sys.argv)
window = QWidget()
chaptersList = []

#Event Handlers
def checkSelected():
	for i in list.selectedItems():
		i.setCheckState(Qt.CheckState.Checked)

def downloadChaptersList():
	global chaptersList
	if txtMangaUrl.text() == "":
		QMessageBox.warning(window, "Error", "Write an URL")
		return

	list.clear()
	downloader = bd.MangaDownloader()
	
	try:
		chaptersList = downloader.getChapterList(txtMangaUrl.text())
	except:
		QMessageBox.critical(window, "Error", str(sys.exc_info()[1]))  
	
	for c in chaptersList:
		if c.language == "English": #TODO: allow the user to choose a language
			item = QListWidgetItem(c.title + " [" + c.groupName + "]")
			item.setData(Qt.UserRole, c.id)
			item.setCheckState(Qt.CheckState.Unchecked)
			list.addItem(item)

def writeLog(text):
	txtLog.setPlainText(time.strftime("[%H:%M] ") + text + "\n" + txtLog.toPlainText())

def disableStuff():
	global btnStart, btnDownloadChaptersList, txtMangaUrl, btnCheckSelected, list
	btnStart.setEnabled(False)
	btnDownloadChaptersList.setEnabled(False)
	txtMangaUrl.setEnabled(False)
	btnCheckSelected.setEnabled(False)
	list.setEnabled(False)
	
def enableStuff():
	global btnStart, btnDownloadChaptersList, txtMangaUrl, btnCheckSelected, list
	btnStart.setEnabled(True)
	btnDownloadChaptersList.setEnabled(True)
	txtMangaUrl.setEnabled(True)
	btnCheckSelected.setEnabled(True)
	list.setEnabled(True)

def downloadSelectedChapters():
	global chaptersList
	chapters = []
	
	for i in range(0, list.count()):
		if list.item(i).checkState() == Qt.CheckState.Checked:
			chapters.append(chaptersList[list.item(i).data(Qt.UserRole)])
	
	thread = DownloaderThread(window, chapters)
	thread.logWritten.connect(writeLog)
	thread.workDone.connect(enableStuff)
	disableStuff()
	thread.start()
	return

# Worker Thread
class DownloaderThread(QThread):

	logWritten = Signal(str)
	workDone = Signal()
	
	def emitSignal(self, text):
		self.logWritten.emit(text)

	def __init__(self, parent, chapters):
		QThread.__init__(self, parent)
		self.chapters = chapters
		
	def run(self):
		try:
			downloader = bd.MangaDownloader()
			downloader.logWritten.connect(self.emitSignal)
			#downloader.fakeJob()
			#self.workDone.emit()
			#return
			
			for c in self.chapters:
				directory = c.title + " [" + c.groupName + "]"
				directory = re.sub(r'[/?<>\\:*|"]', "_", directory)
				directory = r"f:\mieiProgrammi\batotoDownloader" + "\\" + directory
				if not os.path.exists(directory):
					os.makedirs(directory)
				downloader.downloadChapter(c.link, directory, True)
			self.workDone.emit()
		except:
			self.emitSignal("Error:" + str(sys.exc_info()[1]))
			self.workDone.emit()

# Widgets setup

window.setWindowTitle("Batoto Downloader")

lblMangaUrl = QLabel("Manga url: ", window)
txtMangaUrl = QLineEdit(window)

btnDownloadChaptersList = QPushButton(window)
btnDownloadChaptersList.setText("Download Chapters List")
btnDownloadChaptersList.clicked.connect(downloadChaptersList)

btnCheckSelected = QPushButton(window)
btnCheckSelected.setText("Check Selected")
btnCheckSelected.clicked.connect(checkSelected)

list = QListWidget(window)
list.setSelectionMode(QAbstractItemView.ExtendedSelection)

btnStart = QPushButton(window)
btnStart.setText("Start Download")
btnStart.clicked.connect(downloadSelectedChapters)

txtLog = QTextEdit(window)
txtLog.setReadOnly(True)

# Set Layout
mainLayout = QVBoxLayout(window)
topLayout = QHBoxLayout()
topLayout.addWidget(lblMangaUrl)
topLayout.addWidget(txtMangaUrl)
topLayout.addWidget(btnDownloadChaptersList)
mainLayout.addItem(topLayout)
mainLayout.addWidget(btnCheckSelected)
mainLayout.addWidget(list)
mainLayout.addWidget(btnStart)
mainLayout.addWidget(txtLog)
window.resize(500, 600)

window.show()
app.exec_()

