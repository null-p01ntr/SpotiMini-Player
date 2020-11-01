import sys
import spotidata
import json

from time import sleep
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QIcon, QFont, QImage, QPixmap, QPalette, QPixmapCache
from PyQt5.QtCore import QCoreApplication, QThread, Qt, QBasicTimer, QPoint, pyqtSignal
from PyQt5.QtWidgets import QAction, QMenu, QScrollArea, QWidget

class liveFetch(QThread):
	sig = pyqtSignal(int)
	def run(self):
		while True:
			spotidata.fetchData()
			self.sig.emit(1)
			sleep(0.3)

class MiniPlayer(QtWidgets.QMainWindow):
	
	state = {}
	with open('state.json') as json_file:
		state = json.load(json_file)

	stayTog = state['toggles']['stay_on']
	shuffTog = state['toggles']['shuff']
	repTog = state['toggles']['rep']
	titleTog = state['toggles']['title']

	posX = state['positions']['x']
	posY = state['positions']['y']

	def __init__(self):
		super().__init__()

		spotidata.fetchData()

		self.setObjectName("MiniPlayer")
		self.setEnabled(True)
		self.resize(300, 300)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(True)
		self.setSizePolicy(sizePolicy)
		self.setMinimumSize(QtCore.QSize(300, 300))
		self.setMaximumSize(QtCore.QSize(640, 640))
		self.setBaseSize(QtCore.QSize(0, 0))
		self.setFocusPolicy(QtCore.Qt.NoFocus)

		transBack = ".QPushButton{background-color : transparent;}"
		#play UI
		self.play_pause = QtWidgets.QPushButton(self)
		self.play_pause.setGeometry(QtCore.QRect(140, 250, 35, 35))
		self.play_pause.setObjectName("play_pause")
		hoverShow = ".QPushButton::hover{border-image : url(img/play.png);}"
		self.play_pause.setStyleSheet(transBack + hoverShow)
		#next UI
		self.next = QtWidgets.QPushButton(self)
		self.next.setGeometry(QtCore.QRect(265, 0, 35, 300))
		self.next.setObjectName("next")
		self.next.setStyleSheet(transBack)
		#previous UI
		self.prev = QtWidgets.QPushButton(self)
		self.prev.setGeometry(QtCore.QRect(0, 0, 35, 300))
		self.prev.setObjectName("prev")
		self.prev.setStyleSheet(transBack)
		#album art UI
		self.albumart = QtWidgets.QLabel(self)
		self.albumart.setGeometry(QtCore.QRect(0, 0, 300, 300))
		sizePolicy = QtWidgets.QSizePolicy(
				QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.albumart.sizePolicy().hasHeightForWidth())
		self.albumart.setSizePolicy(sizePolicy)
		self.albumart.setMinimumSize(QtCore.QSize(300, 300))
		self.albumart.setMaximumSize(QtCore.QSize(640, 640))
		#title
		self.song_info = QtWidgets.QLabel(self)
		self.song_info.setGeometry(QtCore.QRect(5, 0, 290, 30))
		if spotidata.online:
			self.song_info.setObjectName(spotidata.title)
		else:
			self.song_info.setObjectName("No song playing")
		self.song_info.setStyleSheet(".QLabel{border-radius : 8;}"
                               + ".QLabel::hover{background-color : rgba(255, 255, 255, 98);}")
		self.song_info.setHidden(not self.titleTog)
		
		self.albumart.raise_()
		self.song_info.raise_()
		self.play_pause.raise_()
		self.next.raise_()
		self.prev.raise_()

		self.oldPos = self.pos()

		cover = QtGui.QPixmap()
		if spotidata.online:		
			cover.loadFromData(spotidata.cover_data)
		else:
			null_song = QImage('img/null-song.png')
			cover.fromImage(null_song)

		self.albumart.setPixmap(cover)
		self.albumart.setScaledContents(True)
		self.albumart.setAlignment(QtCore.Qt.AlignCenter)
		self.albumart.setOpenExternalLinks(False)
		self.albumart.setObjectName("albumart")

		#button functions
		self.play_pause.clicked.connect(spotidata.play_pauseB)
		self.next.clicked.connect(spotidata.nextB)
		self.prev.clicked.connect(spotidata.prevB)

		self.retranslateUi(self)
		QtCore.QMetaObject.connectSlotsByName(self)

		self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

#load from state{
		#stay_on
		if self.stayTog:
			self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
		else:
			self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
		#position
		self.move(self.posX, self.posY)
#}
		self.updateThread()
		self.show()

	def contextMenuEvent(self, event):
		contextMenu = QMenu(self)
		#always on top
		stay_on = contextMenu.addAction('Always on Top')
		stay_on.setCheckable(True)
		stay_on.setChecked(self.stayTog)
		stay_on.toggled.connect(self.stay_onToggle)
		#shuffle
		shuffle = contextMenu.addAction('Shuffle')
		shuffle.setCheckable(True)
		shuffle.setChecked(self.shuffTog)
		shuffle.toggled.connect(self.shuffle_Toggle)
		#repeat
		repeat = contextMenu.addAction('Repeat')
		repeat.setCheckable(True)
		repeat.setChecked(self.repTog)
		repeat.toggled.connect(self.repeat_Toggle)
		#show title
		if spotidata.online:
			title = contextMenu.addAction('Show Title: ' + spotidata.title)
		else:
			title = contextMenu.addAction('Show Title: No song playing')
		title.setCheckable(True)
		title.setChecked(self.titleTog)
		title.toggled.connect(self.title_Toggle)
		
		close = contextMenu.addAction('Close')

		action = contextMenu.exec_(self.mapToGlobal(event.pos()))

		if action == close:
			self.close()

	def stay_onToggle(self):
		self.stayTog = not self.stayTog
		if self.stayTog:
			self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
		else:
			self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
		self.show()

	def title_Toggle(self):
		self.titleTog = not self.titleTog
		self.song_info.setHidden(not self.titleTog)

	def shuffle_Toggle(self):
		self.shuffTog = not self.shuffTog
		spotidata.shuff(self.shuffTog)
	
	def repeat_Toggle(self):
		self.repTog = not self.repTog
		if self.repTog: tmp = 'context'
		else: tmp = 'off'
		spotidata.repeat(tmp)

	def retranslateUi(self, MiniPlayer):
		_translate = QtCore.QCoreApplication.translate
		if spotidata.online:
			MiniPlayer.setWindowTitle(_translate("MiniPlayer", spotidata.title))
			MiniPlayer.song_info.setText(_translate("MiniPlayer", "  "+spotidata.title))
		else:
			MiniPlayer.setWindowTitle(_translate("MiniPlayer", "No song playing"))
			MiniPlayer.song_info.setText(_translate("MiniPlayer", "No song playing"))

	def updateThread(self):
		self.thread = liveFetch()
		self.thread.sig.connect(self.updateData)
		self.thread.start()

	def updateData(self):
		_translate = QtCore.QCoreApplication.translate
		cover = QtGui.QPixmap()		
		if spotidata.online:
			self.setWindowTitle(_translate("MiniPlayer", spotidata.title))
			self.song_info.setText(_translate("MiniPlayer", "  "+spotidata.title))
			cover.loadFromData(spotidata.cover_data)
			self.albumart.setPixmap(cover)
		else: 
			self.setWindowTitle(_translate("MiniPlayer", "No song playing"))
			self.song_info.setText(_translate("MiniPlayer", "No song playing"))
			self.albumart.setPixmap(QPixmap('img/null-song.png'))
		
		#RESIZE
		#self.albumart.resize(MiniPlayer.width(), MiniPlayer.height())

	def center(self):
		qr = self.frameGeometry()
		cp = QtWidgets.QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

	def mousePressEvent(self, event):
		self.oldPos = event.globalPos()

	def mouseMoveEvent(self, event):
		delta = QPoint(event.globalPos() - self.oldPos)
		#print(delta)
		self.move(self.x() + delta.x(), self.y() + delta.y())
		self.oldPos = event.globalPos()

	def closeEvent(self, event):
		self.state['toggles']['stay_on'] = self.stayTog
		self.state['toggles']['shuff'] = self.shuffTog
		self.state['toggles']['title'] = self.titleTog

		self.state['positions']['x'] = self.pos().x()
		self.state['positions']['y'] = self.pos().y()

		with open('state.json', 'w') as save:
			json.dump(self.state, save)

app = QtWidgets.QApplication(sys.argv)
ex = MiniPlayer()
sys.exit(app.exec_())
