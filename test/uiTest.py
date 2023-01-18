# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'spotimini.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# Warning! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MiniPlayer(object):
    def setupUi(self, MiniPlayer):
        MiniPlayer.setObjectName("MiniPlayer")
        MiniPlayer.setEnabled(True)
        MiniPlayer.resize(300, 300)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MiniPlayer.sizePolicy().hasHeightForWidth())
        MiniPlayer.setSizePolicy(sizePolicy)
        MiniPlayer.setMinimumSize(QtCore.QSize(300, 300))
        MiniPlayer.setMaximumSize(QtCore.QSize(640, 640))
        MiniPlayer.setBaseSize(QtCore.QSize(0, 0))
        MiniPlayer.setMouseTracking(False)
        MiniPlayer.setFocusPolicy(QtCore.Qt.NoFocus)
        MiniPlayer.setAutoFillBackground(False)
        MiniPlayer.setStyleSheet("")
        self.play_pause = QtWidgets.QPushButton(MiniPlayer)
        self.play_pause.setGeometry(QtCore.QRect(140, 250, 35, 35))
        self.play_pause.setStyleSheet("")
        self.play_pause.setFlat(False)
        self.play_pause.setObjectName("play_pause")
        self.next = QtWidgets.QPushButton(MiniPlayer)
        self.next.setGeometry(QtCore.QRect(250, 0, 50, 300))
        self.next.setFocusPolicy(QtCore.Qt.NoFocus)
        self.next.setAutoFillBackground(False)
        self.next.setCheckable(False)
        self.next.setAutoDefault(False)
        self.next.setDefault(False)
        self.next.setFlat(False)
        self.next.setObjectName("next")
        self.prev = QtWidgets.QPushButton(MiniPlayer)
        self.prev.setGeometry(QtCore.QRect(0, 0, 35, 300))
        self.prev.setFlat(False)
        self.prev.setObjectName("prev")
        self.albumart = QtWidgets.QLabel(MiniPlayer)
        self.albumart.setGeometry(QtCore.QRect(0, 0, 300, 300))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.albumart.sizePolicy().hasHeightForWidth())
        self.albumart.setSizePolicy(sizePolicy)
        self.albumart.setMinimumSize(QtCore.QSize(300, 300))
        self.albumart.setMaximumSize(QtCore.QSize(640, 640))
        self.albumart.setSizeIncrement(QtCore.QSize(0, 0))
        self.albumart.setText("")
        self.albumart.setPixmap(QtGui.QPixmap("../../../OneDrive/Resimler/ProfilePic/steveharris.sig.move.png"))
        self.albumart.setScaledContents(True)
        self.albumart.setAlignment(QtCore.Qt.AlignCenter)
        self.albumart.setOpenExternalLinks(False)
        self.albumart.setObjectName("albumart")
        self.label = QtWidgets.QLabel(MiniPlayer)
        self.label.setGeometry(QtCore.QRect(0, 0, 300, 30))
        self.label.setObjectName("label")
        self.albumart.raise_()
        self.play_pause.raise_()
        self.next.raise_()
        self.prev.raise_()
        self.label.raise_()

        self.retranslateUi(MiniPlayer)
        QtCore.QMetaObject.connectSlotsByName(MiniPlayer)

    def retranslateUi(self, MiniPlayer):
        _translate = QtCore.QCoreApplication.translate
        MiniPlayer.setWindowTitle(_translate("MiniPlayer", "spotidata.title"))
        self.play_pause.setText(_translate("MiniPlayer", ">||"))
        self.next.setText(_translate("MiniPlayer", ">>"))
        self.prev.setText(_translate("MiniPlayer", "<<"))
        self.label.setText(_translate("MiniPlayer", "spotidata.title"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MiniPlayer = QtWidgets.QWidget()
    ui = Ui_MiniPlayer()
    ui.setupUi(MiniPlayer)
    MiniPlayer.show()
    sys.exit(app.exec_())

