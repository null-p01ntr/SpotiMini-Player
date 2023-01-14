import sys
from PyQt5 import QtCore, QtWidgets


class FramelessResizable(object):
    def setup(self, f):
        f.setObjectName("Frameless-Resizable-Window")
        f.resize(300, 400)
        self.gridLayout = QtWidgets.QGridLayout(f)

        self.button = QtWidgets.QPushButton(f)
        self.button.setText("Button")
        self.gridLayout.addWidget(self.button, 0, 0, 1, 1)

        self.sizegrip = QtWidgets.QSizeGrip(f)
        self.gridLayout.addWidget(
            self.sizegrip, 1, 0, QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)

        flags = QtCore.Qt.WindowFlags(
            QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        f.setWindowFlags(flags)


app = QtWidgets.QApplication(sys.argv)
f = QtWidgets.QWidget()
ui = FramelessResizable()
ui.setup(f)
f.show()
sys.exit(app.exec_())
