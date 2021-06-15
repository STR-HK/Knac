import os
import time
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import json

def jamo(args):
    CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
    JUNGSUNG_LIST = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
    JONGSUNG_LIST = ['', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
    r_lst = []
    for w in list(args):
        if (w == '○'):
            r_lst.append('○')
            continue
        ch1 = (ord(w) - ord('가')) // 588
        ch2 = ((ord(w) - ord('가')) - (588 * ch1)) // 28
        ch3 = (ord(w) - ord('가')) - (588 * ch1) - (28 * ch2)
        r_lst.append(CHOSUNG_LIST[ch1])
        r_lst.append(JUNGSUNG_LIST[ch2])
        r_lst.append(JONGSUNG_LIST[ch3])
    return r_lst

def gyeopjamo(args):
    data = '''{
                "ㄲ" : "ㄱㄱ", "ㄸ" : "ㄷㄷ", "ㅃ" : "ㅂㅂ", "ㅆ" : "ㅅㅅ", "ㅉ" : "ㅈㅈ", 
                "ㄳ" : "ㄱㅅ", "ㄵ" : "ㄴㅈ", "ㄶ" : "ㄴㅎ", "ㄺ" : "ㄹㄱ", "ㄻ" : "ㄹㅁ", 
                "ㄼ" : "ㄹㅂ", "ㄽ" : "ㄹㅅ", "ㄾ" : "ㄹㅌ", "ㄿ" : "ㄹㅍ", "ㅀ" : "ㄹㅎ", "ㅄ" : "ㅂㅅ", 
                "ㅐ" : "ㅏㅣ", "ㅒ" : "ㅑㅣ", "ㅔ" : "ㅓㅣ", "ㅖ" : "ㅕㅣ", "ㅘ" : "ㅗㅏ", 
                "ㅙ" : "ㅗㅏㅣ", "ㅚ" : "ㅗㅣ", "ㅝ" : "ㅜㅓ", "ㅞ" : "ㅜㅓㅣ", "ㅟ" : "ㅜㅣ", "ㅢ" : "ㅡㅣ", "" : ""
            }'''
    data = json.loads(data)
    returns = []
    for s in range(len(args)):
        if args[s] not in data:
            returns.append(args[s])
        if args[s] in data:
            returns.append(data[args[s]])
    return returns

class HoverTracker(QObject):
    positionChanged = pyqtSignal(QPoint)

    def __init__(self, widget):
        super().__init__(widget)
        self._widget = widget
        self.widget.setMouseTracking(True)
        self.widget.installEventFilter(self)

    @property
    def widget(self):
        return self._widget

    def eventFilter(self, obj, event):
        if obj is self.widget and event.type() == QEvent.MouseMove:
            self.positionChanged.emit(event.pos())
        return super().eventFilter(obj, event)

class Button(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.r = 0
        self.timer = QTimer(interval=5, timeout=self.set_radius)
        self.clicked.connect(self.timer.start)

    def set_radius(self):
        if self.r == 0:
            try:
                self.fixedPoint = point
            except:
                self.fixedPoint = self.rect().center()
        if self.r < self.width() * 1.2:
            self.r += self.width() / 100
        else:
            self.timer.stop()
            self.r = 0
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.r:
            qp = QPainter(self)
            qp.setBrush(QColor(255, 255, 255, 80))
            qp.setPen(Qt.NoPen)
            qp.drawEllipse(self.fixedPoint, self.r, self.r)

class Listener(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('')
        self.resize(650, 500)
        self.geometryInfo = self.frameGeometry()
        self.centerpoint = QDesktopWidget().availableGeometry().center()
        self.geometryInfo.moveCenter(self.centerpoint)
        self.move(self.geometryInfo.topLeft())
        self.show()

        self.style()

        self.initUI()
    
    @pyqtSlot(QPoint)
    def on_position_changed(self, pt):
        global point
        point = pt

    def addRipple(self, button):
        self.hover_tracker = HoverTracker(button)
        self.hover_tracker.positionChanged.connect(self.on_position_changed)

    def style(self):
        self.sampleST = """
        QPushButton {
            border-radius: 2px;
            padding: 15px;
            background-color: #F0F0F0;
            outline: 0;
            text-align: left;
            border: 2px solid transparent;
            border-bottom-color: #A19BFE;
        }
        """
        self.inputST = """
        QLineEdit {
            border: 2px solid #A19BFE;
            background-color: #F0F0F0;
            color: black;
            padding: 13px;
            border-top-left-radius: 3px;
            border-top-right-radius: 3px;
    
            selection-background-color: #A19BFE;
            selection-color: black;
        }
        """
        self.resultST = """
        QPushButton {
            border-radius: 2px;
            padding: 15px;
            background-color: #F0F0F0;
            outline: 0;
            text-align: left;
            border: 2px solid transparent;
            border-left-color: #A19BFE;
        }
        """

        self.functionST = """
        QPushButton {
            border-radius: 2px;
            padding: 15px;
            background-color: #F0F0F0;
            outline: 0;
            text-align: left;
            border: 2px solid transparent;
            border-top-color: #A19BFE;
            border-bottom-color: #A19BFE;
        }
        """

    def initUI(self):
        self.mainlayout = QVBoxLayout()
        
        self.sample = QPushButton('이 문장은 예시 문장이니 적절한 문장을 적당히 입력해 주시면 감사하고 조언드립니다')
        self.sample.setStyleSheet(self.sampleST)
        self.addRipple(self.sample)
        self.input = QLineEdit()
        self.input.setPlaceholderText(self.sample.text())
        self.input.setStyleSheet(self.inputST)
        self.input.textEdited.connect(self.textEdited)
        self.input.editingFinished.connect(self.editingFinished)
        self.input.setFocus()
        self.result = QPushButton('소요 시간 : NONE\n타자 속도 : NONE')
        self.result.setStyleSheet(self.resultST)
        self.addRipple(self.result)

        self.mainlayout.addWidget(self.sample)
        self.mainlayout.addWidget(self.input)
        self.mainlayout.addWidget(self.result)

        self.sublayout = QHBoxLayout()

        self.addsentence = Button('문장 추가하기')
        self.addsentence.setStyleSheet(self.functionST)
        self.addRipple(self.addsentence)
        self.showsentence = Button('문장 목록 보기')
        self.showsentence.setStyleSheet(self.functionST)
        self.addRipple(self.showsentence)
        self.exit = Button('프로그램 종료')
        self.exit.setStyleSheet(self.functionST)
        self.addRipple(self.exit)

        self.sublayout.addWidget(self.addsentence)
        
        self.sublayout.addWidget(self.showsentence)
        self.sublayout.addWidget(self.exit)

        self.mainlayout.addLayout(self.sublayout)
        self.mainlayout.setAlignment(Qt.AlignTop)

        self.setLayout(self.mainlayout)

    def textEdited(self):
        try:
            if self.did == True:
                return
            else:
                self.did = True
                self.start = time.time()
        except:
            self.did = True
            self.start = time.time()

    def editingFinished(self):
        if self.input.text() == self.sample.text():
            self.stop = time.time()
            self.did = False
            self.time = self.stop - self.start
            self.speed = len(list(gyeopjamo(jamo(self.sample.text().replace(' ',''))))) / (self.stop - self.start) * 60

            self.input.setText('')
            self.result.setText('소요 시간 : {}\n타자 속도 : {}'.format(round(self.time), round(self.speed)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Listener()

    palatte = window.palette()
    palatte.setColor(window.backgroundRole(), QColor('#FFFFFF'))
    window.setPalette(palatte)

    from os import path
    fontDB = QFontDatabase()
    fontDB.addApplicationFont(path.abspath(path.join(path.dirname(__file__), 'font/NanumSquareOTF_acB.otf')))
    app.setFont(QFont('NanumSquareOTF_ac Bold', 11))

    
    sys.exit(app.exec_())