import sys
from PySide.QtCore import *
from PySide.QtGui import *

import batotoDownloader as bd

app = QApplication(sys.argv)
window = QWidget()
chaptersList = None

#Event Handlers
def checkSelected():
	for i in list.selectedItems():
		i.setCheckState(Qt.CheckState.Checked)

def downloadChaptersList():
	if txtMangaUrl.text() == "":
		QMessageBox.warning(window, "Error", "Write an URL")
		return

	list.clear()
	try:
		chaptersList = bd.getChapterList(txtMangaUrl.text())
	except:
		QMessageBox.critical(window, "Error", str(sys.exc_info()[1]))  
	
	for c in chaptersList:
		if c.language == "English": #TODO: allow the user to choose a language
			item = QListWidgetItem(c.title + " [" + c.groupName + "]")
			item.setData(Qt.UserRole, c.link)
			item.setCheckState(Qt.CheckState.Unchecked)
			list.addItem(item)

def downloadSelectedChapters():
	for i in range(0, list.count()):
		if list.item(i).checkState() == Qt.CheckState.Checked:
			#print(list.item(i).data(Qt.UserRole))
			bd.downloadChapter(list.item(i).data(Qt.UserRole), ".")

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

#window.showMaximized()
window.show()
app.exec_()

