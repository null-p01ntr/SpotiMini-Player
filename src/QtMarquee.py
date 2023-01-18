from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPainter

class MarqueeLabel(QLabel):
    def __init__(self, parent=None):
        QLabel.__init__(self, parent)
        self.px = 0
        self.py = 15
        self._direction = Qt.LeftToRight
        self.setWordWrap(True)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(40)
        self._speed = 2
        self.textLength = 0
        self.fontPointSize = 0
        self.setAlignment(Qt.AlignVCenter)
        # self.setFixedHeight(self.fontMetrics().height())

    def setFont(self, font):
        QLabel.setFont(self, font)
        # self.setFixedHeight(self.fontMetrics().height())

    def updateCoordinates(self):
        align = self.alignment()
        if align == Qt.AlignTop:
            self.py = 10
        elif align == Qt.AlignBottom:
            self.py = self.height() - 10
        elif align == Qt.AlignVCenter:
            self.py = self.height() / 2
        self.fontPointSize = self.font().pointSize() / 2
        self.textLength = self.fontMetrics().width(self.text())

    def setAlignment(self, alignment):
        self.updateCoordinates()
        QLabel.setAlignment(self, alignment)

    def resizeEvent(self, event):
        self.updateCoordinates()
        QLabel.resizeEvent(self, event)

    def paintEvent(self, event):
        painter = QPainter(self)
        if self._direction == Qt.RightToLeft:
            self.px -= self.speed()
            if self.px <= -self.textLength:
                self.px = self.width()
        else:
            self.px += self.speed()
            if self.px >= self.width():
                self.px = -self.textLength
        painter.drawText(self.px, self.py + self.fontPointSize, self.text())
        painter.translate(self.px, 0)

    def speed(self):
        return self._speed

    def setSpeed(self, speed):
        self._speed = speed

    def setDirection(self, direction):
        self._direction = direction
        if self._direction == Qt.RightToLeft:
            self.px = self.width() - self.textLength
        else:
            self.px = 0
        self.update()

    def pause(self):
        self.timer.stop()

    def unpause(self):
        self.timer.start()
