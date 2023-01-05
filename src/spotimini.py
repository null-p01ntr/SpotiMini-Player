import sys
import spotidata
import json

from time import sleep
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QThread, Qt, QPoint, pyqtSignal
from PyQt5.QtWidgets import QMenu


class liveFetch(QThread):
    sig = pyqtSignal(int)

    def run(self):
        while True:
            spotidata.fetchData()
            self.sig.emit(1)
            sleep(0.05)


class MiniPlayer(QtWidgets.QMainWindow):

    state = {}
    with open('state.json') as json_file:
        state = json.load(json_file)

    spotidata.fetchData()

    # load from state
    stayTog = state['toggles']['stay_on']
    titleTog = state['toggles']['title']
    # load from current user
    shuffTog = spotidata.toggle_states[0]
    repState = spotidata.toggle_states[1]

    posX = state['positions']['x']
    posY = state['positions']['y']

    size = state['size']

    def __init__(self):
        super().__init__()
        spotidata.fetchData()

        self.setObjectName("MiniPlayer")
        self.setEnabled(True)
        self.resize(self.size, self.size)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHeightForWidth(True)
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(150, 150))
        self.setMaximumSize(QtCore.QSize(640, 640))
        self.setBaseSize(QtCore.QSize(0, 0))
        self.setFocusPolicy(QtCore.Qt.NoFocus)

        transBack = ".QPushButton{background-color : transparent;}"
        # play UI
        self.play_pause = QtWidgets.QPushButton(self)
        self.play_pause.setGeometry(QtCore.QRect(
            int((self.size/2)-17), self.size-50, 35, 35))
        self.play_pause.setObjectName("play_pause")
        hoverShow = ".QPushButton::hover{border-image : url(img/" + \
            spotidata.play_state+".png);}"
        self.play_pause.setStyleSheet(transBack + hoverShow)
        # next UI
        self.next = QtWidgets.QPushButton(self)
        self.next.setGeometry(QtCore.QRect(self.size-35, 0, 35, self.size))
        self.next.setObjectName("next")
        self.next.setStyleSheet(transBack)
        # previous UI
        self.prev = QtWidgets.QPushButton(self)
        self.prev.setGeometry(QtCore.QRect(0, 0, 35, self.size))
        self.prev.setObjectName("prev")
        self.prev.setStyleSheet(transBack)
        # album art UI
        self.albumart = QtWidgets.QLabel(self)
        self.albumart.setGeometry(QtCore.QRect(0, 0, self.size, self.size))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.albumart.sizePolicy().hasHeightForWidth())
        self.albumart.setSizePolicy(sizePolicy)
        self.albumart.setMinimumSize(QtCore.QSize(150, 150))
        self.albumart.setMaximumSize(QtCore.QSize(640, 640))
        # title
        self.song_info = QtWidgets.QLabel(self)
        self.song_info.setGeometry(QtCore.QRect(5, 0, self.size-10, 30))
        self.song_info.setObjectName(spotidata.title)
        self.song_info.setStyleSheet(".QLabel{border-radius : 8;}"
                                     + ".QLabel::hover{background-color : rgba(255, 255, 255, 160);}")
        self.song_info.setHidden(not self.titleTog)

        # resizers
        self.resizer1 = QtWidgets.QSizeGrip(self)
        self.resizer1.setMaximumSize(640, 640)
        self.resizer1.setGeometry(QtCore.QRect(0, 0, 15, 15))

        self.resizer2 = QtWidgets.QSizeGrip(self)
        self.resizer2.setMaximumSize(640, 640)
        self.resizer2.setGeometry(QtCore.QRect(0, self.size-15, 15, 15))

        self.resizer3 = QtWidgets.QSizeGrip(self)
        self.resizer3.setMaximumSize(640, 640)
        self.resizer3.setGeometry(QtCore.QRect(self.size-15, 0, 15, 15))

        self.resizer4 = QtWidgets.QSizeGrip(self)
        self.resizer4.setMaximumSize(640, 640)
        self.resizer4.setGeometry(QtCore.QRect(
            self.size-15, self.size-15, 15, 15))

        self.albumart.raise_()
        self.song_info.raise_()
        self.play_pause.raise_()
        self.next.raise_()
        self.prev.raise_()
        self.resizer1.raise_()
        self.resizer2.raise_()
        self.resizer3.raise_()
        self.resizer4.raise_()

        self.oldPos = self.pos()

        cover = QtGui.QPixmap()
        cover.loadFromData(spotidata.cover_data)

        self.albumart.setPixmap(cover)
        self.albumart.setScaledContents(True)
        self.albumart.setAlignment(QtCore.Qt.AlignCenter)
        self.albumart.setOpenExternalLinks(False)
        self.albumart.setObjectName("albumart")

        # button functions
        self.play_pause.clicked.connect(spotidata.play_pauseB)
        self.play_pause.clicked.connect(self.errorMessage)

        self.next.clicked.connect(spotidata.nextB)
        self.next.clicked.connect(self.errorMessage)

        self.prev.clicked.connect(spotidata.prevB)
        self.prev.clicked.connect(self.errorMessage)

        ##
        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        # load from state
        # stay_on
        if self.stayTog:
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
        # position
        self.move(self.posX, self.posY)
        self.updateThread()
        self.show()

    # TOGGLES

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
        repeat_states = ['off', 'context', 'track']
        i = repeat_states.index(self.repState)
        if i == 2:
            i = 0
        else:
            i += 1
        self.repState = repeat_states[i]
        spotidata.repeat(self.repState)

    # LIVE DATA

    def updateThread(self):
        self.thread = liveFetch()
        self.thread.sig.connect(self.updateData)
        self.thread.start()

    def updateData(self):
        _translate = QtCore.QCoreApplication.translate
        cover = QtGui.QPixmap()
        self.setWindowTitle(_translate("MiniPlayer", spotidata.title))
        self.song_info.setText(_translate(
            "MiniPlayer", "  "+spotidata.title))
        cover.loadFromData(spotidata.cover_data)
        self.albumart.setPixmap(cover)

        hoverShow = ".QPushButton::hover{border-image : url(img/" + \
            spotidata.play_state+".png);}"
        self.play_pause.setStyleSheet(
            ".QPushButton{background-color : transparent;}" + hoverShow)

        self.shuffTog = spotidata.toggle_states[0]
        self.repState = spotidata.toggle_states[1]

    def errorMessage(self):
        if(not spotidata.online):
            errorPopUp = QtWidgets.QMessageBox.warning(
                self, 'Spotify Offline', 'Please start Spotify on one of your devices\n(or hit play button on Desktop App)', QtWidgets.QMessageBox.Ok)

    # WINDOW EVENTS

    def retranslateUi(self, MiniPlayer):
        _translate = QtCore.QCoreApplication.translate

        MiniPlayer.setWindowTitle(
            _translate("MiniPlayer", spotidata.title))
        MiniPlayer.song_info.setText(_translate(
            "MiniPlayer", "  "+spotidata.title))

        size_ = self.frameGeometry().width()

        MiniPlayer.play_pause.setGeometry(QtCore.QRect(
            int((size_/2)-17.5), size_-50, 35, 35))
        MiniPlayer.prev.setGeometry(QtCore.QRect(0, 0, 35, size_))
        MiniPlayer.next.setGeometry(QtCore.QRect(size_-35, 0, 35, size_))
        MiniPlayer.song_info.setGeometry(QtCore.QRect(5, 0, size_-10, 30))
        MiniPlayer.albumart.setGeometry(QtCore.QRect(0, 0, size_, size_))

        MiniPlayer.resizer2.setGeometry(QtCore.QRect(0, size_-15, 15, 15))
        MiniPlayer.resizer3.setGeometry(QtCore.QRect(size_-15, 0, 15, 15))
        MiniPlayer.resizer4.setGeometry(QtCore.QRect(
            size_-15, size_-15, 15, 15))

        MiniPlayer.resize(size_, size_)

    def resizeEvent(self, event):
        self.retranslateUi(self)
        # album art
        self.albumart.resize(self.frameGeometry().width(),
                             self.frameGeometry().height())

    def contextMenuEvent(self, event):
        contextMenu = QMenu(self)
        # always on top
        stay_on = contextMenu.addAction('Always on Top')
        stay_on.setCheckable(True)
        stay_on.setChecked(self.stayTog)
        stay_on.toggled.connect(self.stay_onToggle)
        # show title
        title = contextMenu.addAction('Show Title: ' + spotidata.title)
        title.setCheckable(True)
        title.setChecked(self.titleTog)
        title.toggled.connect(self.title_Toggle)
        # shuffle
        shuffle = contextMenu.addAction('Shuffle')
        shuffle.setCheckable(True)
        shuffle.setChecked(self.shuffTog)
        shuffle.toggled.connect(self.shuffle_Toggle)
        # repeat
        repeat = contextMenu.addAction('Repeat mode: ' + self.repState)
        repeat.triggered.connect(self.repeat_Toggle)
        repeat.setCheckable(False)
        # close
        close = contextMenu.addAction('Close')
        action = contextMenu.exec_(self.mapToGlobal(event.pos()))
        if action == close:
            self.close()

    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        # print(delta)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

    def mouseDoubleClickEvent(self, event):
        spotidata.play_pauseB()
        self.errorMessage()

    def closeEvent(self, event):
        # save state
        self.state['toggles']['stay_on'] = self.stayTog
        self.state['toggles']['title'] = self.titleTog

        self.state['positions']['x'] = self.pos().x()
        self.state['positions']['y'] = self.pos().y()

        self.state['size'] = self.frameGeometry().width()

        # SAVE SIZE

        with open('state.json', 'w') as save:
            json.dump(self.state, save, indent=4)


app = QtWidgets.QApplication(sys.argv)
ex = MiniPlayer()
sys.exit(app.exec_())
