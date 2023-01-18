from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QPalette
from PyQt5.QtWidgets import QLabel, QApplication, QVBoxLayout, QFormLayout, QLineEdit, QSlider, \
    QHBoxLayout, QWidget, QPushButton, QRadioButton, QFontDialog, QColorDialog


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
        self.setFixedHeight(self.fontMetrics().height())

    def setFont(self, font):
        QLabel.setFont(self, font)
        self.setFixedHeight(self.fontMetrics().height())

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


class Example(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setWindowTitle("Marquee Effect")
        self.setLayout(QVBoxLayout())
        self.marqueeLabel = MarqueeLabel(self)
        flayout = QFormLayout()
        self.layout().addLayout(flayout)
        le = QLineEdit(self)
        le.textChanged.connect(self.marqueeLabel.setText)
        le.setText("""Lorem ipsum dolor sit amet, consectetur adipiscing elit, 
sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.""")
        slider = QSlider(Qt.Horizontal, self)
        slider.valueChanged.connect(self.marqueeLabel.setSpeed)
        slider.setValue(10)

        rtl = QRadioButton("Right to Left", self)
        ltr = QRadioButton("Left to Rigth", self)
        rtl.toggled.connect(lambda state: self.marqueeLabel.setDirection(Qt.RightToLeft if state else  Qt.LeftToRight))
        ltr.setChecked(True)

        directionWidget = QWidget(self)
        directionWidget.setLayout(QHBoxLayout())
        directionWidget.layout().setContentsMargins(0, 0, 0, 0)
        directionWidget.layout().addWidget(rtl)
        directionWidget.layout().addWidget(ltr)
        fontBtn = QPushButton("Font...", self)
        fontBtn.clicked.connect(self.changeFont)
        colorBtn = QPushButton("Color...", self)
        colorBtn.clicked.connect(self.changeColor)
        pauseBtn = QPushButton("Pause", self)
        pauseBtn.setCheckable(True)
        pauseBtn.toggled.connect(lambda state: self.marqueeLabel.pause() if state else self.marqueeLabel.unpause())
        pauseBtn.toggled.connect(lambda state: pauseBtn.setText("Resume") if state else pauseBtn.setText("Pause"))

        flayout.addRow("Change Text", le)
        flayout.addRow("Change Speed", slider)
        flayout.addRow("Direction", directionWidget)
        flayout.addRow("fontBtn", fontBtn)
        flayout.addRow("colorBtn", colorBtn)
        flayout.addRow("Animation", pauseBtn)
        self.layout().addWidget(self.marqueeLabel)

    def changeColor(self):
        palette = self.marqueeLabel.palette()
        color = QColorDialog.getColor(palette.brush(QPalette.WindowText).color(), self)
        if color.isValid():
            palette.setBrush(QPalette.WindowText, color)
            self.marqueeLabel.setPalette(palette)

    def changeFont(self):
        font, ok = QFontDialog.getFont(self.marqueeLabel.font(), self)
        if ok:
            self.marqueeLabel.setFont(font)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    w = Example()
    w.show()
    sys.exit(app.exec_())