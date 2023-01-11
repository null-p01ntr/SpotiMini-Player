import sys
from PyQt5 import QtWidgets, QtCore


class MyWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setGeometry(200, 200, 800, 600)
        # label showing some text
        self.textLabel = QtWidgets.QLabel('')
        # label showing the news
        self.label = QtWidgets.QLabel('')
        # text starts on the right
        self.label.setAlignment(QtCore.Qt.AlignRight)
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.textLabel)
        self.layout.addWidget(self.label)
        self.layout.setStretch(0, 3)
        self.layout.setStretch(1, 3)
        self.layout.setStretch(2, 3)
        self.layout.setStretch(3, 1)
        self.setLayout(self.layout)

        self.timeLine = QtCore.QTimeLine()
        # linear Timeline
        self.timeLine.setCurveShape(QtCore.QTimeLine.LinearCurve)
        self.timeLine.frameChanged.connect(self.setText)
        self.timeLine.finished.connect(self.nextNews)
        self.signalMapper = QtCore.QSignalMapper(self)
        self.signalMapper.mapped[str].connect(self.setTlText)

        self.feed()

    def feed(self):
        fm = self.label.fontMetrics()
        self.nl = int(self.label.width()/fm.averageCharWidth()
                      )     # shown stringlength
        news = [
            ('user-read-private user-read-playback-state user-modify-playback-state user-read-recently-played')]
        appendix = ' '*self.nl                      # add some spaces at the end
        news.append(appendix)
        delimiter = ' '                   # shown between the messages
        self.news = delimiter.join(news)
        # number of letters in news = frameRange
        newsLength = len(self.news)
        lps = 4                                 # letters per second
        # duration until the whole string is shown in milliseconds
        dur = newsLength*500/lps
        self.timeLine.setDuration(dur)
        self.timeLine.setFrameRange(0, newsLength)
        self.timeLine.start()

    def setText(self, number_of_frame):
        if number_of_frame < self.nl:
            start = 0
        else:
            start = number_of_frame - self.nl
        text = '{}'.format(self.news[start:number_of_frame])
        self.label.setText(text)

    def nextNews(self):
        self.feed()  # start again

    def setTlText(self, text):
        string = '{} pressed'.format(text)
        self.textLabel.setText(string)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    widget = MyWidget()
    widget.show()
    sys.exit(app.exec_())
