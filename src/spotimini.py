import sys

from PyQt5.QtGui import QFont, QFontDatabase

from spotidata import SpotifyData
import json

from time import sleep
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QThread, Qt, QPoint, pyqtSignal
from PyQt5.QtWidgets import QMenu

sptObj = SpotifyData().auth()
if sptObj == 0:
    print("'creds.json' has been created, enter your credentials")
    quit()


class LiveFetch(QThread):
    sig = pyqtSignal(int)

    def run(self):
        while True:
            MiniPlayer.spoti_dict = SpotifyData(sptObj).data_dict
            self.sig.emit(1)
            sleep(0.05)


class MiniPlayer(QtWidgets.QMainWindow):
    with open('state.json') as json_file:
        state = json.load(json_file)

    print('SpotiMini RUNNING')
    spoti_dict = SpotifyData(sptObj).data_dict

    # load from state
    stayTog = state['toggles']['stay_on']
    titleTog = state['toggles']['title']
    # load from current user
    shuffTog = spoti_dict['toggle_states'][0]
    repState = spoti_dict['toggle_states'][1]

    posX = state['positions']['x']
    posY = state['positions']['y']

    size = state['size']

    def __init__(self):
        super().__init__()

        self.setObjectName("MiniPlayer")
        self.setEnabled(True)
        self.resize(self.size, self.size)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        # sizePolicy.setHeightForWidth(True)
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(150, 150))
        self.setMaximumWidth(640)  # WARNING not best practice
        self.setBaseSize(QtCore.QSize(0, 0))
        self.setFocusPolicy(QtCore.Qt.NoFocus)

        transBack = ".QPushButton{background-color : transparent;}"
        # play UI
        self.play_pause = QtWidgets.QPushButton(self)
        self.play_pause.setGeometry(
            QtCore.QRect(int((self.size / 2) - 17), self.size - 50, 35, 35))
        self.play_pause.setObjectName("play_pause")
        hoverShow = ".QPushButton::hover{border-image : url(img/" + \
                    self.spoti_dict['play_state'] + ".png);}"
        self.play_pause.setStyleSheet(transBack + hoverShow)
        # next UI
        self.next = QtWidgets.QPushButton(self)
        self.next.setGeometry(QtCore.QRect(self.size - 35, 0, 35, self.size))
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
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.albumart.sizePolicy().hasHeightForWidth())
        self.albumart.setSizePolicy(sizePolicy)
        self.albumart.setMinimumSize(QtCore.QSize(150, 150))
        self.albumart.setMaximumSize(QtCore.QSize(640, 640))

        # title
        self.song_info = QtWidgets.QLabel(self)
        # TODO find font
        self.song_info.setFont(QFont('Arial', 10, QFont.Bold))
        self.song_info.setAlignment(QtCore.Qt.AlignRight
                                    | QtCore.Qt.AlignVCenter)
        self.song_info.setGeometry(QtCore.QRect(5, 0, self.size - 10, 30))
        self.song_info.setStyleSheet(
            ".QLabel{color:rgb(0,0,0); border-radius : 8;}" +
            ".QLabel::hover{background-color : rgba(255, 255, 255, 160);}")
        self.song_info.setHidden(not self.titleTog)

        self.timeLine = QtCore.QTimeLine()
        # linear Timeline
        self.timeLine.setCurveShape(QtCore.QTimeLine.LinearCurve)
        self.timeLine.frameChanged.connect(self.setText)
        self.timeLine.finished.connect(self.nextNews)
        self.signalMapper = QtCore.QSignalMapper(self)
        self.signalMapper.mapped[str].connect(self.setTlText)

        # TODO dont slide if text fits
        # TODO start again while ending
        self.feed()

        # size grips
        self.resizer1 = QtWidgets.QSizeGrip(self)
        # self.resizer1.setMaximumSize(640, 640)
        self.resizer1.setGeometry(QtCore.QRect(0, 0, 15, 15))
        self.resizer1.setVisible(True)

        self.resizer2 = QtWidgets.QSizeGrip(self)
        # self.resizer2.setMaximumSize(640, 640)
        self.resizer2.setGeometry(QtCore.QRect(0, self.size - 15, 15, 15))
        self.resizer2.setVisible(True)

        self.resizer3 = QtWidgets.QSizeGrip(self)
        # self.resizer3.setMaximumSize(640, 640)
        self.resizer3.setGeometry(QtCore.QRect(self.size - 15, 0, 15, 15))
        self.resizer3.setVisible(True)

        self.resizer4 = QtWidgets.QSizeGrip(self)
        # self.resizer4.setMaximumSize(640, 640)
        self.resizer4.setGeometry(
            QtCore.QRect(self.size - 15, self.size - 15, 15, 15))
        self.resizer4.setVisible(True)

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
        cover.loadFromData(self.spoti_dict['cover_data'])

        self.albumart.setPixmap(cover)
        self.albumart.setScaledContents(True)
        self.albumart.setAlignment(QtCore.Qt.AlignCenter)
        self.albumart.setOpenExternalLinks(False)
        self.albumart.setObjectName("albumart")

        # button functions
        self.play_pause.clicked.connect(self.play_pause_wrapper)
        self.play_pause.clicked.connect(self.errorMessage)

        self.next.clicked.connect(self.nextB_wrapper)
        self.next.clicked.connect(self.errorMessage)

        self.prev.clicked.connect(self.prevB_wrapper)
        self.prev.clicked.connect(self.errorMessage)

        self.retranslateUI(self)
        QtCore.QMetaObject.connectSlotsByName(self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        # stay_on
        if self.stayTog:
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
        # position
        self.move(self.posX, self.posY)

        self.updateThread()
        self.show()

    def feed(self):
        fm = self.song_info.fontMetrics()
        self.nl = int(self.song_info.width())  # shown stringlength
        news = [(self.spoti_dict['title'])]
        appendix = ' ' * self.nl  # add some spaces at the end
        news.append(appendix)
        delimiter = ' '  # shown between the messages
        self.news = delimiter.join(news)
        # number of letters in news = frameRange
        newsLength = len(self.news)
        lps = 5  # letters per second
        # duration until the whole string is shown in milliseconds
        dur = newsLength * 500 / lps
        self.timeLine.setDuration(int(dur))
        self.timeLine.setFrameRange(5, newsLength)
        self.timeLine.start()

    def setText(self, number_of_frame):
        if number_of_frame < self.nl:
            start = 0
        else:
            start = number_of_frame - self.nl
        text = '{}'.format(self.news[start:number_of_frame])
        self.song_info.setText(text)

    def nextNews(self):
        self.feed()  # start again

    def setTlText(self, text):
        string = '{} pressed'.format(text)
        self.textLabel.setText(string)

    # FUNCTIONALITY

    def play_pause_wrapper(self):
        SpotifyData(sptObj).play_pauseB()
        # self.spoti_dict = SpotifyData().fetchData()

    def nextB_wrapper(self):
        SpotifyData(sptObj).nextB()
        # self.spoti_dict = SpotifyData().fetchData()

    def prevB_wrapper(self):
        SpotifyData(sptObj).prevB()
        # self.spoti_dict = SpotifyData().fetchData()

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
        SpotifyData(sptObj).shuff(self.shuffTog)
        # self.spoti_dict = SpotifyData().fetchData()

    def repeat_Toggle(self):
        SpotifyData(sptObj).repeat(self.repState)
        # self.spoti_dict = SpotifyData().fetchData()

    # LIVE DATA

    def updateThread(self):
        self.thread = LiveFetch()
        self.thread.sig.connect(self.updateData)
        self.thread.start()

    def updateData(self):
        _translate = QtCore.QCoreApplication.translate
        cover = QtGui.QPixmap()
        self.setWindowTitle(_translate("MiniPlayer", self.spoti_dict['title']))
        # TODO update title
        # self.song_info.setText(_translate(
        #     "MiniPlayer", "  " + self.spoti_dict['title']))
        cover.loadFromData(self.spoti_dict['cover_data'])
        self.albumart.setPixmap(cover)

        hoverShow = ".QPushButton::hover{border-image : url(img/" + \
                    self.spoti_dict['play_state'] + ".png);}"
        self.play_pause.setStyleSheet(
            ".QPushButton{background-color : transparent;}" + hoverShow)

        self.shuffTog = self.spoti_dict['toggle_states'][0]
        self.repState = self.spoti_dict['toggle_states'][1]

    def errorMessage(self):
        if not self.spoti_dict['online']:
            errorPopUp = QtWidgets.QMessageBox.warning(
                self, 'Spotify Offline',
                'Please start Spotify on one of your devices\n(or hit play button on Desktop App)',
                QtWidgets.QMessageBox.Ok)

    # WINDOW EVENTS

    def retranslateUI(self, MiniPlayer):
        _translate = QtCore.QCoreApplication.translate

        MiniPlayer.setWindowTitle(
            _translate("MiniPlayer", self.spoti_dict['title']))
        MiniPlayer.song_info.setText(
            _translate("MiniPlayer", "  " + self.spoti_dict['title']))

        _size = self.frameGeometry().width()

        MiniPlayer.play_pause.setGeometry(
            QtCore.QRect(int((_size / 2) - 17.5), _size - 50, 35, 35))
        MiniPlayer.prev.setGeometry(QtCore.QRect(0, 0, 35, _size))
        MiniPlayer.next.setGeometry(QtCore.QRect(_size - 35, 0, 35, _size))
        MiniPlayer.song_info.setGeometry(QtCore.QRect(5, 0, _size - 10, 30))
        MiniPlayer.albumart.setGeometry(QtCore.QRect(0, 0, _size, _size))

        MiniPlayer.resizer2.setGeometry(QtCore.QRect(0, _size - 15, 15, 15))
        MiniPlayer.resizer3.setGeometry(QtCore.QRect(_size - 15, 0, 15, 15))
        MiniPlayer.resizer4.setGeometry(
            QtCore.QRect(_size - 15, _size - 15, 15, 15))

        MiniPlayer.resize(_size, _size)

    def resizeEvent(self, event):
        self.retranslateUI(self)
        # ERROR title dissapears at 150x150
        # album art
        # self.albumart.resize(self.frameGeometry().width(),
        #                      self.frameGeometry().height())

    def contextMenuEvent(self, event):
        contextMenu = QMenu(self)

        # always on top
        stay_on = contextMenu.addAction('Always on Top')
        stay_on.setCheckable(True)
        stay_on.setChecked(self.stayTog)
        stay_on.toggled.connect(self.stay_onToggle)

        # show title
        title = contextMenu.addAction('Show Title: ' +
                                      self.spoti_dict['title'])
        title.setCheckable(True)
        title.setChecked(self.titleTog)
        title.toggled.connect(self.title_Toggle)

        # shuffle
        shuffle = contextMenu.addAction('Shuffle')
        shuffle.setCheckable(True)
        shuffle.setChecked(self.shuffTog)
        shuffle.toggled.connect(self.shuffle_Toggle)

        # repeat
        repeat = contextMenu.addMenu('Repeat mode')

        # repeat off
        repeatOff = repeat.addAction('Off')
        repeatOff.setCheckable(True)
        repeatOff.setChecked(bool(self.repState == 'off'))
        repeatOff.toggled.connect(lambda: SpotifyData(sptObj).repeat('off'))

        # repeat track
        repeatTrack = repeat.addAction('This track')
        repeatTrack.setCheckable(True)
        repeatTrack.setChecked(bool(self.repState == 'track'))
        repeatTrack.toggled.connect(
            lambda: SpotifyData(sptObj).repeat('track'))

        # repeat context
        repeatContext = repeat.addAction('Playlist')
        repeatContext.setCheckable(True)
        repeatContext.setChecked(bool(self.repState == 'context'))
        repeatContext.toggled.connect(
            lambda: SpotifyData(sptObj).repeat('context'))

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
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

    def mouseDoubleClickEvent(self, event):
        SpotifyData(sptObj).play_pauseB()
        self.errorMessage()

    def closeEvent(self, event):
        # save state
        self.state['toggles']['stay_on'] = self.stayTog
        self.state['toggles']['title'] = self.titleTog

        self.state['positions']['x'] = self.pos().x()
        self.state['positions']['y'] = self.pos().y()

        self.state['size'] = self.frameGeometry().width()

        with open('state.json', 'w') as save:
            json.dump(self.state, save, indent=4)


app = QtWidgets.QApplication(sys.argv)
ex = MiniPlayer()
sys.exit(app.exec_())
