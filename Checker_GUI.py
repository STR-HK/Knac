from PyQt5.QtCore import QDateTime, Qt, QTimer, QSize
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget, QMessageBox, QStackedWidget, QStatusBar, QDesktopWidget,
        QMainWindow, QMenuBar, QAction, QMenu)

from PyQt5.QtGui import (QIcon, QColor, QPainter, QFontDatabase, QFont,
        QPixmap, QCursor)

from PyQt5 import QtCore

from os import path
import json
import re

import Hangul

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.blockColor = 'white'

        self.setWindowTitle('Korean Name Compatibility Checker GUI')
        self.iconfilename = u'./icons/{}'.format('NK.png')

        self.setWindowIcon(QIcon(self.iconfilename))
        self.resize(500, 650)

        self.geometryInfo = self.frameGeometry()
        self.centerpoint = QDesktopWidget().availableGeometry().center()
        self.geometryInfo.moveCenter(self.centerpoint)
        self.move(self.geometryInfo.topLeft())

        self.layout = QVBoxLayout(self)

        self.QTabs = QTabWidget()
        self.QTab1 = QWidget()
        self.QTab2 = QWidget()
        self.QTab3 = QWidget()
        self.QGithub = QWidget()
        self.QDev = QWidget()


        self.QTabs.addTab(self.QTab1, "𝟏 by 𝟏")
        self.QTabs.addTab(self.QTab2, "𝟏 by 𝒏")
        self.QTabs.addTab(self.QTab3, "𝒏 by 𝒏")
        self.QTabs.addTab(self.QGithub, "𝐈𝐧𝐟𝐨")
        self.QTabs.addTab(self.QDev, "𝕯𝖊𝖛")
        
        self.layout.addWidget(self.QTabs)
        self.setLayout(self.layout)

        self.Dev()
        self.Tab1()

    def Info(self):
        print('Info')

    def Dev(self):
        
        self.Devlayout = QGridLayout(self)
        self.Devlayout.setAlignment(Qt.AlignTop)

        self.blockColorText = QLabel('Tab1 Block Color : ' + str(self.blockColor))
        self.blockColorText.setStyleSheet('background-color: white;')
        self.blockColorInputBox = QLineEdit()
        self.blockColorInputBox.setStyleSheet("padding-left: 2px;")
        self.blockColorInputBox.setPlaceholderText("Block Color")
        self.blockColorButton = QPushButton('Apply', self)
        self.blockColorButton.clicked.connect(self.blockColorFunc)
       
        self.Devlayout.addWidget(self.blockColorText, 0, 1, 1, 4)
        self.Devlayout.addWidget(self.blockColorInputBox, 1, 1, 1, 3)
        self.Devlayout.addWidget(self.blockColorButton, 1, 4, 1, 1)

        self.QDev.setLayout(self.Devlayout)


    def blockColorFunc(self):
        self.blockColor = self.blockColorInputBox.text()
        self.blockColorText = QLabel('Tab1 Block Color : ' + str(self.blockColor))
        self.blockColorText.setStyleSheet('background-color: white;')
        self.Devlayout.addWidget(self.blockColorText, 0, 1, 1, 4)
        self.QDev.setLayout(self.Devlayout)


    def Tab1(self):

        self.Tab1layout = QGridLayout(self)
        self.Tab1layout.setAlignment(Qt.AlignTop)

        self.Tab1input1 = QLineEdit()
        self.Tab1input1.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1input1.setPlaceholderText("NAME 1")
        self.Tab1input1.setFixedHeight(32)

        self.Tab1input2 = QLineEdit()
        self.Tab1input2.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1input2.setPlaceholderText("NAME 2")
        self.Tab1input2.setFixedHeight(32)

        self.Tab1analysisButton = QPushButton('Analysis')
        self.Tab1analysisButton.setFixedHeight(32)
        self.Tab1analysisButton.clicked.connect(self.Tab1ButtonClick)

        self.Tab1Blank = QLabel('\n')

        self.Tab1Tree = QGridLayout(self)
        self.Tab1Tree.setAlignment(Qt.AlignTop)

        self.Tab1layout.addWidget(self.Tab1input1, 0, 0)
        self.Tab1layout.addWidget(self.Tab1input2, 0, 1)
        self.Tab1layout.addWidget(self.Tab1analysisButton, 1, 0, 1, 2)
        self.Tab1layout.addWidget(self.Tab1Blank, 2, 0, 1, 2)

        # 최종 반영
        self.QTab1.setLayout(self.Tab1layout)


    def Tab1ButtonClick(self):
        self.Tab1name1list = re.compile('[가-힣]+').findall(self.Tab1input1.text())
        self.Tab1name2list = re.compile('[가-힣]+').findall(self.Tab1input2.text())

        self.Tab1name1 = ''
        self.Tab1name2 = ''

        self.Tab1name1 = self.Tab1name1.join(self.Tab1name1list)
        self.Tab1name2 = self.Tab1name2.join(self.Tab1name2list)

        if (len(self.Tab1input1.text()) == 2 or len(self.Tab1input1.text()) == 3):
            if (len(self.Tab1name1) == 2 or len(self.Tab1name1) == 3):
                if (len(self.Tab1input2.text()) == 2 or len(self.Tab1input2.text()) == 3):
                    if (len(self.Tab1name2) == 2 or len(self.Tab1name2) == 3):
                        self.Tab1Analyser(self.Tab1name1, self.Tab1name2)
                        return

        # 잘못된 입력
        self.alert = QMessageBox()
        self.alert.setIcon(QMessageBox.Critical)
        self.alert.setWindowTitle('Invalid Input')
        self.alert.setWindowIcon(QIcon('icons/name.png'))
        self.alert.setText('Invalid Input. Please Retry.\nCondition : KR 2 or 3 Letter')
        self.alert.setStandardButtons(QMessageBox.Retry)
        self.alert.setDefaultButton(QMessageBox.Retry)
        self.ret = self.alert.exec_()


    def Tab1Analyser(self, Name1, Name2):
        # 2글자 이름의 경우에는 ○ 붙이기
        if (len(Name1) == 2):
            Name1 = Name1 + '○'
        if (len(Name2) == 2):
            Name2 = Name2 + '○'

        # 첫번째 줄 코드
        self.Tab1TreeLayer1 = QGridLayout(self)
        self.Tab1TreeLayer1Text1 = QLabel(Name1[0])
        self.Tab1TreeLayer1Text1.setStyleSheet('font-size: 20px;''background-color: ' + self.blockColor)
        self.Tab1TreeLayer1Text1.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer1Text2 = QLabel(Name2[0])
        self.Tab1TreeLayer1Text2.setStyleSheet('font-size: 20px;''background-color: ' + self.blockColor)
        self.Tab1TreeLayer1Text2.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer1Text3 = QLabel(Name1[1])
        self.Tab1TreeLayer1Text3.setStyleSheet('font-size: 20px;''background-color: ' + self.blockColor)
        self.Tab1TreeLayer1Text3.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer1Text4 = QLabel(Name2[1])
        self.Tab1TreeLayer1Text4.setStyleSheet('font-size: 20px;''background-color: ' + self.blockColor)
        self.Tab1TreeLayer1Text4.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer1Text5 = QLabel(Name1[2])
        self.Tab1TreeLayer1Text5.setStyleSheet('font-size: 20px;''background-color: ' + self.blockColor)
        self.Tab1TreeLayer1Text5.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer1Text6 = QLabel(Name2[2])
        self.Tab1TreeLayer1Text6.setStyleSheet('font-size: 20px;''background-color: ' + self.blockColor)
        self.Tab1TreeLayer1Text6.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer1.addWidget(self.Tab1TreeLayer1Text1, 0, 0)
        self.Tab1TreeLayer1.addWidget(self.Tab1TreeLayer1Text2, 0, 1)
        self.Tab1TreeLayer1.addWidget(self.Tab1TreeLayer1Text3, 0, 2)
        self.Tab1TreeLayer1.addWidget(self.Tab1TreeLayer1Text4, 0, 3)
        self.Tab1TreeLayer1.addWidget(self.Tab1TreeLayer1Text5, 0, 4)
        self.Tab1TreeLayer1.addWidget(self.Tab1TreeLayer1Text6, 0, 5)
        self.Tab1Tree.addLayout(self.Tab1TreeLayer1, 0, 0)
        self.Tab1layout.addLayout(self.Tab1Tree, 3, 0, 1, 2)
        self.QTab1.setLayout(self.Tab1layout)
        
        # 이름 글자별로 넣을 리스트 생성
        self.Name1toList = []
        self.Name2toList = []
        
        # 이름을 글자별로 리스트에 넣음
        for a in range(3):
            self.Name1toList.append(Name1[a])
            self.Name1toList[a] = Hangul.gyeopjamo(Hangul.jamo(self.Name1toList[a]))
            self.Name1toList[a] = Hangul.convertonumber(''.join(self.Name1toList[a]))
        for b in range(3):
            self.Name2toList.append(Name2[b])
            self.Name2toList[b] = Hangul.gyeopjamo(Hangul.jamo(self.Name2toList[b]))
            self.Name2toList[b] = Hangul.convertonumber(''.join(self.Name2toList[b]))

        # 두번째 줄 코드
        self.Tab1TreeLayer2 = QGridLayout(self)
        self.Tab1TreeLayer2Text1 = QLabel(str(self.Name1toList[0]))
        self.Tab1TreeLayer2Text1.setStyleSheet('font-size: 15px;''background-color: ' + self.blockColor)
        self.Tab1TreeLayer2Text1.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer2Text2 = QLabel(str(self.Name2toList[0]))
        self.Tab1TreeLayer2Text2.setStyleSheet('font-size: 15px;''background-color: ' + self.blockColor)
        self.Tab1TreeLayer2Text2.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer2Text3 = QLabel(str(self.Name1toList[1]))
        self.Tab1TreeLayer2Text3.setStyleSheet('font-size: 15px;''background-color: ' + self.blockColor)
        self.Tab1TreeLayer2Text3.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer2Text4 = QLabel(str(self.Name2toList[1]))
        self.Tab1TreeLayer2Text4.setStyleSheet('font-size: 15px;''background-color: ' + self.blockColor)
        self.Tab1TreeLayer2Text4.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer2Text5 = QLabel(str(self.Name1toList[2]))
        self.Tab1TreeLayer2Text5.setStyleSheet('font-size: 15px;''background-color: ' + self.blockColor)
        self.Tab1TreeLayer2Text5.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer2Text6 = QLabel(str(self.Name2toList[2]))
        self.Tab1TreeLayer2Text6.setStyleSheet('font-size: 15px;''background-color: ' + self.blockColor)
        self.Tab1TreeLayer2Text6.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer2.addWidget(self.Tab1TreeLayer2Text1, 0, 0)
        self.Tab1TreeLayer2.addWidget(self.Tab1TreeLayer2Text2, 0, 1)
        self.Tab1TreeLayer2.addWidget(self.Tab1TreeLayer2Text3, 0, 2)
        self.Tab1TreeLayer2.addWidget(self.Tab1TreeLayer2Text4, 0, 3)
        self.Tab1TreeLayer2.addWidget(self.Tab1TreeLayer2Text5, 0, 4)
        self.Tab1TreeLayer2.addWidget(self.Tab1TreeLayer2Text6, 0, 5)
        self.Tab1Tree.addLayout(self.Tab1TreeLayer2, 1, 0)
        self.Tab1layout.addLayout(self.Tab1Tree, 4, 0, 1, 2)
        self.QTab1.setLayout(self.Tab1layout)

        self.Name1and2 = []
        for w in range(3):
            self.Name1and2.append(self.Name1toList[w])
            self.Name1and2.append(self.Name2toList[w])

        self.Name3List = []

        for x in range(5):
            self.Name3List.append(int(str((self.Name1and2[x] + self.Name1and2[x+1]))[-1]))

        # 세번째 줄 코드
        self.Tab1TreeLayer3 = QGridLayout(self)
        self.Tab1TreeLayer3Text0 = QLabel(' ')
        self.Tab1TreeLayer3Text0.setStyleSheet('font-size: 15px;''background-color: ' + self.blockColor)
        self.Tab1TreeLayer3Text0.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer3Text1 = QLabel(str(self.Name3List[0]))
        self.Tab1TreeLayer3Text1.setStyleSheet('font-size: 15px;''background-color: ' + self.blockColor)
        self.Tab1TreeLayer3Text1.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer3Text15 = QLabel(' ')
        self.Tab1TreeLayer3Text15.setStyleSheet('font-size: 15px;''background-color: ' + self.blockColor)
        self.Tab1TreeLayer3Text15.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer3Text2 = QLabel(str(self.Name3List[1]))
        self.Tab1TreeLayer3Text2.setStyleSheet('font-size: 15px;''background-color: ' + self.blockColor)
        self.Tab1TreeLayer3Text2.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer3Text25 = QLabel(' ')
        self.Tab1TreeLayer3Text25.setStyleSheet('font-size: 15px;''background-color: ' + self.blockColor)
        self.Tab1TreeLayer3Text25.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer3Text3 = QLabel(str(self.Name3List[2]))
        self.Tab1TreeLayer3Text3.setStyleSheet('font-size: 15px;''background-color: ' + self.blockColor)
        self.Tab1TreeLayer3Text3.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer3Text35 = QLabel(' ')
        self.Tab1TreeLayer3Text35.setStyleSheet('font-size: 15px;''background-color: ' + self.blockColor)
        self.Tab1TreeLayer3Text35.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer3Text4 = QLabel(str(self.Name3List[3]))
        self.Tab1TreeLayer3Text4.setStyleSheet('font-size: 15px;''background-color: ' + self.blockColor)
        self.Tab1TreeLayer3Text4.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer3Text45 = QLabel(' ')
        self.Tab1TreeLayer3Text45.setStyleSheet('font-size: 15px;''background-color: ' + self.blockColor)
        self.Tab1TreeLayer3Text45.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer3Text5 = QLabel(str(self.Name3List[4]))
        self.Tab1TreeLayer3Text5.setStyleSheet('font-size: 15px;''background-color: ' + self.blockColor)
        self.Tab1TreeLayer3Text5.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer3Text55 = QLabel(' ')
        self.Tab1TreeLayer3Text55.setStyleSheet('font-size: 15px;''background-color: ' + self.blockColor)
        self.Tab1TreeLayer3Text55.setAlignment(QtCore.Qt.AlignCenter)

        self.Tab1TreeLayer3.addWidget(self.Tab1TreeLayer3Text0, 0, 0, 1, 2)
        self.Tab1TreeLayer3.addWidget(self.Tab1TreeLayer3Text1, 0, 2, 1, 2)
        self.Tab1TreeLayer3.addWidget(self.Tab1TreeLayer3Text15, 0, 4, 1, 1)
        self.Tab1TreeLayer3.addWidget(self.Tab1TreeLayer3Text2, 0, 5, 1, 2)
        self.Tab1TreeLayer3.addWidget(self.Tab1TreeLayer3Text25, 0, 7, 1, 1)
        self.Tab1TreeLayer3.addWidget(self.Tab1TreeLayer3Text3, 0, 8, 1, 2)
        self.Tab1TreeLayer3.addWidget(self.Tab1TreeLayer3Text35, 0, 10, 1, 1)
        self.Tab1TreeLayer3.addWidget(self.Tab1TreeLayer3Text4, 0, 11, 1, 2)
        self.Tab1TreeLayer3.addWidget(self.Tab1TreeLayer3Text45, 0, 13, 1, 1)
        self.Tab1TreeLayer3.addWidget(self.Tab1TreeLayer3Text5, 0, 15, 1, 2)
        self.Tab1TreeLayer3.addWidget(self.Tab1TreeLayer3Text55, 0, 17, 1, 2)

        self.Tab1Tree.addLayout(self.Tab1TreeLayer3, 2, 0)
        self.Tab1layout.addLayout(self.Tab1Tree, 5, 0, 1, 2)
        self.QTab1.setLayout(self.Tab1layout)

        self.Name4List = []

        for u in range(4):
            self.Name4List.append(int(str((self.Name3List[u] + self.Name3List[u+1]))[-1]))

        # 네번째 줄 코드
        self.Tab1TreeLayer4 = QGridLayout(self)
        self.Tab1TreeLayer4Text0 = QLabel(' ')
        self.Tab1TreeLayer4Text0.setStyleSheet('font-size: 15px;''background-color: ' + self.blockColor)
        self.Tab1TreeLayer4Text0.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer4Text1 = QLabel(str(self.Name4List[0]))
        self.Tab1TreeLayer4Text1.setStyleSheet('font-size: 15px;''background-color: ' + self.blockColor)
        self.Tab1TreeLayer4Text1.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer4Text2 = QLabel(str(self.Name4List[1]))
        self.Tab1TreeLayer4Text2.setStyleSheet('font-size: 15px;''background-color: ' + self.blockColor)
        self.Tab1TreeLayer4Text2.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer4Text3 = QLabel(str(self.Name4List[2]))
        self.Tab1TreeLayer4Text3.setStyleSheet('font-size: 15px;''background-color: ' + self.blockColor)
        self.Tab1TreeLayer4Text3.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer4Text4 = QLabel(str(self.Name4List[3]))
        self.Tab1TreeLayer4Text4.setStyleSheet('font-size: 15px;''background-color: ' + self.blockColor)
        self.Tab1TreeLayer4Text4.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer4Text5 = QLabel(' ')
        self.Tab1TreeLayer4Text5.setStyleSheet('font-size: 15px;''background-color: ' + self.blockColor)
        self.Tab1TreeLayer4Text5.setAlignment(QtCore.Qt.AlignCenter)

        self.Tab1TreeLayer4.addWidget(self.Tab1TreeLayer4Text0, 0, 1)
        self.Tab1TreeLayer4.addWidget(self.Tab1TreeLayer4Text1, 0, 2)
        self.Tab1TreeLayer4.addWidget(self.Tab1TreeLayer4Text2, 0, 3)
        self.Tab1TreeLayer4.addWidget(self.Tab1TreeLayer4Text3, 0, 4)
        self.Tab1TreeLayer4.addWidget(self.Tab1TreeLayer4Text4, 0, 5)
        self.Tab1TreeLayer4.addWidget(self.Tab1TreeLayer4Text5, 0, 6)

        self.Tab1Tree.addLayout(self.Tab1TreeLayer4, 3, 0)
        self.Tab1layout.addLayout(self.Tab1Tree, 6, 0, 1, 2)
        self.QTab1.setLayout(self.Tab1layout)

        self.Name5List = []

        for v in range(3):
            self.Name5List.append(int(str((self.Name4List[v] + self.Name4List[v+1]))[-1]))

        # 다섯번째 줄 코드
        self.Tab1TreeLayer5 = QGridLayout(self)
        self.Tab1TreeLayer5Text0 = QLabel(' ')
        self.Tab1TreeLayer5Text0.setStyleSheet('font-size: 15px;''background-color: ' + self.blockColor)
        self.Tab1TreeLayer5Text0.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer5Text1 = QLabel(' ')
        self.Tab1TreeLayer5Text1.setStyleSheet('font-size: 15px;''background-color: ' + self.blockColor)
        self.Tab1TreeLayer5Text1.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer5Text2 = QLabel(str(self.Name5List[0]))
        self.Tab1TreeLayer5Text2.setStyleSheet('font-size: 15px;''background-color: ' + self.blockColor)
        self.Tab1TreeLayer5Text2.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer5Text3 = QLabel(str(self.Name5List[1]))
        self.Tab1TreeLayer5Text3.setStyleSheet('font-size: 15px;''background-color: ' + self.blockColor)
        self.Tab1TreeLayer5Text3.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer5Text4 = QLabel(str(self.Name5List[2]))
        self.Tab1TreeLayer5Text4.setStyleSheet('font-size: 15px;''background-color: ' + self.blockColor)
        self.Tab1TreeLayer5Text4.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer5Text5 = QLabel(' ')
        self.Tab1TreeLayer5Text5.setStyleSheet('font-size: 15px;''background-color: ' + self.blockColor)
        self.Tab1TreeLayer5Text5.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer5Text6 = QLabel(' ')
        self.Tab1TreeLayer5Text6.setStyleSheet('font-size: 15px;''background-color: ' + self.blockColor)
        self.Tab1TreeLayer5Text6.setAlignment(QtCore.Qt.AlignCenter)

        self.Tab1TreeLayer5.addWidget(self.Tab1TreeLayer5Text0, 0, 1)
        self.Tab1TreeLayer5.addWidget(self.Tab1TreeLayer5Text1, 0, 2)
        self.Tab1TreeLayer5.addWidget(self.Tab1TreeLayer5Text2, 0, 3)
        self.Tab1TreeLayer5.addWidget(self.Tab1TreeLayer5Text3, 0, 4)
        self.Tab1TreeLayer5.addWidget(self.Tab1TreeLayer5Text4, 0, 5)
        self.Tab1TreeLayer5.addWidget(self.Tab1TreeLayer5Text5, 0, 6)
        self.Tab1TreeLayer5.addWidget(self.Tab1TreeLayer5Text6, 0, 7)

        self.Tab1Tree.addLayout(self.Tab1TreeLayer5, 4, 0)
        self.Tab1layout.addLayout(self.Tab1Tree, 7, 0, 1, 2)
        self.QTab1.setLayout(self.Tab1layout)

        self.Name6List = []

        for k in range(2):
            self.Name6List.append(int(str((self.Name5List[k] + self.Name5List[k+1]))[-1]))

        # 여섯번째 줄 코드
        self.Tab1TreeLayer6 = QGridLayout(self)
        self.Tab1TreeLayer6Text0 = QLabel(' ')
        self.Tab1TreeLayer6Text0.setStyleSheet('font-size: 15px;''background-color: ' + self.blockColor)
        self.Tab1TreeLayer6Text0.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer6Text1 = QLabel(' ')
        self.Tab1TreeLayer6Text1.setStyleSheet('font-size: 15px;''background-color: ' + self.blockColor)
        self.Tab1TreeLayer6Text1.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer6Text2 = QLabel(str(self.Name6List[0]) + str(self.Name6List[1]) + '%')
        self.Tab1TreeLayer6Text2.setStyleSheet('font-size: 25px;''background-color: ' + self.blockColor)
        self.Tab1TreeLayer6Text2.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer6Text3 = QLabel(' ')
        self.Tab1TreeLayer6Text3.setStyleSheet('font-size: 15px;''background-color: ' + self.blockColor)
        self.Tab1TreeLayer6Text3.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer6Text4 = QLabel(' ')
        self.Tab1TreeLayer6Text4.setStyleSheet('font-size: 15px;''background-color: ' + self.blockColor)
        self.Tab1TreeLayer6Text4.setAlignment(QtCore.Qt.AlignCenter)

        self.Tab1TreeLayer6.addWidget(self.Tab1TreeLayer6Text0, 0, 1, 1, 1)
        self.Tab1TreeLayer6.addWidget(self.Tab1TreeLayer6Text1, 0, 2, 1, 1)
        self.Tab1TreeLayer6.addWidget(self.Tab1TreeLayer6Text2, 0, 3, 1, 2)
        self.Tab1TreeLayer6.addWidget(self.Tab1TreeLayer6Text3, 0, 5, 1, 1)
        self.Tab1TreeLayer6.addWidget(self.Tab1TreeLayer6Text4, 0, 6, 1, 1)

        self.Tab1Tree.addLayout(self.Tab1TreeLayer6, 5, 0)
        self.Tab1layout.addLayout(self.Tab1Tree, 8, 0, 1, 2)
        self.QTab1.setLayout(self.Tab1layout)




if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)

    fontDB = QFontDatabase()
    fontDB.addApplicationFont(path.abspath(path.join(path.dirname(__file__), 'fonts/SDGothicNeoM.ttf')))
    app.setFont(QFont('AppleSDGothicNeoM00', 11))

    window = MainWindow()

    #palatte = window.palette()
    #palatte.setColor(window.backgroundRole(), Qt.white)
    #window.setPalette(palatte)

    window.show()
    sys.exit(app.exec())