from PyQt5.QtCore import QDateTime, Qt, QTimer, QSize, QTextStream, QFile
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget, QMessageBox, QStackedWidget, QStatusBar, QDesktopWidget,
        QMainWindow, QMenuBar, QAction, QMenu, QListWidget, QListWidgetItem, QInputDialog,
        QFileDialog, QTableWidgetItem, QHeaderView, QShortcut)

from PyQt5.QtGui import (QIcon, QColor, QPainter, QFontDatabase, QFont,
        QPixmap, QCursor, QKeySequence)

from PyQt5 import QtCore

from os import path
import json
import re
import csv

import Hangul

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        # 다른곳에서 사용하는 변수 및 리스트 선언
        self.blockColor = 'white'
        self.Tab2NAME1col = []
        self.Tab2NAME2col = []
        self.Tab2RESULTcol = []

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

        self.ShortCut()

        self.Dev()
        self.Info()
        self.Tab1()
        self.Tab2()

    def ShortCut(self):
        self.SCexit = QShortcut(QKeySequence('Ctrl+W'), self)
        self.SCexit.activated.connect(app.quit)
        self.SCanal = QShortcut(QKeySequence('Ctrl+A'), self)
        self.SCanal.activated.connect(self.analysis)
        self.SCsave = QShortcut(QKeySequence('Ctrl+S'), self)
        self.SCsave.activated.connect(self.save)

        self.SCTab1 = QShortcut(QKeySequence('Ctrl+1'), self)
        self.SCTab1.activated.connect(self.gotoTab1)
        self.SCTab2 = QShortcut(QKeySequence('Ctrl+2'), self)
        self.SCTab2.activated.connect(self.gotoTab2)
        self.SCTab3 = QShortcut(QKeySequence('Ctrl+3'), self)
        self.SCTab3.activated.connect(self.gotoTab3)
        self.SCTab4 = QShortcut(QKeySequence('Ctrl+4'), self)
        self.SCTab4.activated.connect(self.gotoTab4)
        self.SCTab5 = QShortcut(QKeySequence('Ctrl+5'), self)
        self.SCTab5.activated.connect(self.gotoTab5)
        
        self.SCTXT = QShortcut(QKeySequence('Ctrl+T'), self)
        self.SCTXT.activated.connect(self.TXT)
        self.SCSCV = QShortcut(QKeySequence('Ctrl+C'), self)
        self.SCSCV.activated.connect(self.CSV)

        self.SCADD = QShortcut(QKeySequence('Ctrl+P'), self)
        self.SCADD.activated.connect(self.plus)

        self.SCN1 = QShortcut(QKeySequence('Ctrl+N'), self)
        self.SCN1.activated.connect(self.Name1)
        self.SCN2 = QShortcut(QKeySequence('Ctrl+M'), self)
        self.SCN2.activated.connect(self.Name2)

    def Name1(self):
        if (self.QTabs.currentIndex() == 0):
            self.Tab1input1.setFocus()
        elif (self.QTabs.currentIndex() == 1):
            self.Tab2input1.setFocus()

    def Name2(self):
        if (self.QTabs.currentIndex() == 0):
            self.Tab1input2.setFocus()

    def save(self):
        if (self.QTabs.currentIndex() == 1):
            self.Tab2SaveAsCSV.click()
        elif (self.QTabs.currentIndex() == 2):
            print('탭3s')

    def analysis(self):
        if (self.QTabs.currentIndex() == 0):
            self.Tab1analysisButton.click()
        elif (self.QTabs.currentIndex() == 1):
            self.Tab2analysisButton.click()
        elif (self.QTabs.currentIndex() == 2):
            print('탭3A')
    
    def plus(self):
        if (self.QTabs.currentIndex() == 1):
            self.Tab2AddButton.click()
        elif (self.QTabs.currentIndex() == 2):
            print('탭3P')

    def gotoTab1(self):
        self.QTabs.setCurrentIndex(0)
    def gotoTab2(self):
        self.QTabs.setCurrentIndex(1)
    def gotoTab3(self):
        self.QTabs.setCurrentIndex(2)
    def gotoTab4(self):
        self.QTabs.setCurrentIndex(3)
    def gotoTab5(self):
        self.QTabs.setCurrentIndex(4)

    def TXT(self):
        if (self.QTabs.currentIndex() == 1):
            self.Tab2TXTButton.click()
        elif (self.QTabs.currentIndex() == 2):
            print('탭3T')
    
    def CSV(self):
        if (self.QTabs.currentIndex() == 1):
            self.Tab2CSVButton.click()
        elif (self.QTabs.currentIndex() == 2):
            print('탭3C')

    def Info(self):
        self.Infolayout = QGridLayout(self)
        self.Infolayout.setAlignment(Qt.AlignTop)
        # self.Infolayout.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

        self.octocat = QLabel(self)
        self.octocat.setScaledContents(True)
        self.octocat.setPixmap(QPixmap('./icons/github.png'))
        self.octocat.setFixedSize(64, 64)

        self.sourceLink = QLabel('  Source Code : <a href="https://github.com/STR-HK/Knac">Repository Link</a>')
        self.sourceLink.setOpenExternalLinks(True)

        self.Infolayout.addWidget(self.octocat, 0, 1, 1, 1)
        self.Infolayout.addWidget(self.sourceLink, 0, 2, 1, 2)
        self.QGithub.setLayout(self.Infolayout)

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
        self.Tab1input1.editingFinished.connect(self.Tab1input1Fin)

        self.Tab1input2 = QLineEdit()
        self.Tab1input2.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1input2.setPlaceholderText("NAME 2")
        self.Tab1input2.setFixedHeight(32)
        self.Tab1input2.editingFinished.connect(self.Tab1input2Fin)

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

    def Tab1input1Fin(self):
        self.Tab1input2.setFocus()
        self.Tab1input2.selectAll()

    def Tab1input2Fin(self):
        self.Tab1analysisButton.click()
        self.Tab1input1.setFocus()
        self.Tab1input1.selectAll()

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
        self.alert.setWindowIcon(QIcon('icons/NK.png'))
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

    def Tab2(self):
        self.Tab2layout = QGridLayout(self)
        self.Tab2layout.setAlignment(Qt.AlignTop)

        self.Tab2TXTButton = QPushButton()
        self.Tab2TXTButton.setText('TXT')
        self.Tab2TXTButton.setFixedHeight(20)
        self.Tab2TXTButton.clicked.connect(self.Tab2TXTClick)
        
        self.Tab2CSVButton = QPushButton()
        self.Tab2CSVButton.setText('CSV')
        self.Tab2CSVButton.setFixedHeight(20)
        self.Tab2CSVButton.clicked.connect(self.Tab2CSVClick)

        self.Tab2AddButton = QPushButton()
        self.Tab2AddButton.setText('+')
        self.Tab2AddButton.setFixedHeight(20)
        self.Tab2AddButton.clicked.connect(self.Tab2AddClick)

        self.Tab2RemoveButton = QPushButton()
        self.Tab2RemoveButton.setText('-')
        self.Tab2RemoveButton.setFixedHeight(20)
        self.Tab2RemoveButton.clicked.connect(self.Tab2RemoveClick)

        self.Tab2input1 = QLineEdit()
        self.Tab2input1.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab2input1.setPlaceholderText("NAME 1")
        self.Tab2input1.setFixedHeight(40)
        self.Tab2input1.editingFinished.connect(self.Tab2input1Fin)

        self.Tab2input2 = QListWidget()
        self.Tab2input2.setFixedHeight(128)

        self.Tab2analysisButton = QPushButton('Analysis')
        self.Tab2analysisButton.setFixedHeight(32)
        self.Tab2analysisButton.clicked.connect(self.Tab2ButtonClick)

        self.Tab2Blank1 = QLabel('\n')
        self.Tab2table = QTableWidget()
        self.Tab2Blank2 = QLabel('\n')

        self.Tab2SaveAsCSV = QPushButton('SAVE AS CSV')
        self.Tab2SaveAsCSV.setFixedHeight(27)
        self.Tab2SaveAsCSV.clicked.connect(self.Tab2SaveCSV)

        self.Tab2Tree = QGridLayout(self)
        self.Tab2Tree.setAlignment(Qt.AlignTop)

        self.Tab2layout.addWidget(self.Tab2TXTButton, 0, 0, 1, 1)
        self.Tab2layout.addWidget(self.Tab2CSVButton, 0, 1, 1, 1)
        self.Tab2layout.addWidget(self.Tab2AddButton, 0, 2, 1, 1)
        self.Tab2layout.addWidget(self.Tab2RemoveButton, 0, 3, 1, 1)

        self.Tab2layout.addWidget(self.Tab2input1, 1, 0, 1, 2)
        self.Tab2layout.addWidget(self.Tab2input2, 1, 2, 1, 2)
        self.Tab2layout.addWidget(self.Tab2analysisButton, 2, 0, 1, 4)
        self.Tab2layout.addWidget(self.Tab2Blank1, 3, 0, 1, 4)
        self.Tab2layout.addWidget(self.Tab2table, 4, 0, 1, 4)
        self.Tab2layout.addWidget(self.Tab2SaveAsCSV, 5, 0, 1, 4)

        # 최종 반영
        self.QTab2.setLayout(self.Tab2layout)

    def Tab2input1Fin(self):
        self.Tab2AddButton.setFocus()

    def Tab2SaveCSV(self):
        if (self.Tab2NAME1col == []):
            self.alert = QMessageBox()
            self.alert.setIcon(QMessageBox.Critical)
            self.alert.setWindowTitle('No Data Exists')
            self.alert.setWindowIcon(QIcon('icons/NK.png'))
            self.alert.setText('No Data Exists.\nPlease Analysis First.')
            self.alert.setStandardButtons(QMessageBox.Retry)
            self.alert.setDefaultButton(QMessageBox.Retry)
            self.ret = self.alert.exec_()
            return
        
        defaultFileName = self.Tab2NAME1col[0].replace('○','') + ', ' + str(len(self.Tab2NAME2col)) + '.csv'
        name = QFileDialog.getSaveFileName(self, 'Save file', defaultFileName, "Comma-Separated Values (*.csv)")

        if name == ('', ''):
            return
        
        with open(list(name)[0], mode='w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            for f in range(len(self.Tab2NAME1col)):
                csv_writer.writerow([self.Tab2NAME1col[f].replace('○',''), self.Tab2NAME2col[f].replace('○',''), self.Tab2RESULTcol[f]])

    def Tab2TXTClick(self):
        self.loadTXT = QFileDialog()
        self.loadTXT.setFileMode(QFileDialog.AnyFile)
        self.loadTXTfilename = self.loadTXT.getOpenFileName(
            caption='Open TXT file', filter="Text files (*.txt)")

        if self.loadTXTfilename:
            if self.loadTXTfilename[0] == '':
                return
            
            f = open(self.loadTXTfilename[0], 'r',  encoding='utf-8')
            self.loadTXTList = f.read().split('\n')

            for x in range(len(self.loadTXTList)):
                self.loadTXTtoClear = ''.join(re.compile('[가-힣]+').findall(self.loadTXTList[x]))
                if (len(self.loadTXTList[x]) == 2 or len(self.loadTXTList[x]) == 3):
                    if (len(self.loadTXTtoClear) == 2 or len(self.loadTXTtoClear) == 3):
                        self.Tab2AddItem = QListWidgetItem(self.loadTXTtoClear)
                        self.Tab2AddItem.setTextAlignment(Qt.AlignCenter)
                        self.Tab2AddItem.setSizeHint(QSize(0, 25))
                        self.Tab2input2.addItem(self.Tab2AddItem)

            self.Tab2layout.addWidget(self.Tab2input2, 1, 2, 1, 2)
            self.QTab2.setLayout(self.Tab2layout)


    def Tab2CSVClick(self):
        self.loadTXT = QFileDialog()
        self.loadTXT.setFileMode(QFileDialog.AnyFile)
        self.loadTXTfilename = self.loadTXT.getOpenFileName(
            caption='Open CSV file', filter="Comma-Separated Values (*.csv)")

        if self.loadTXTfilename:
            if self.loadTXTfilename[0] == '':
                return
            
            f = open(self.loadTXTfilename[0], 'r',  encoding='utf-8')
            self.loadTXTList = f.read().split('\n')

            for x in range(len(self.loadTXTList)):
                self.loadTXTtoClear = ''.join(re.compile('[가-힣]+').findall(self.loadTXTList[x]))
                if (len(self.loadTXTList[x]) == 2 or len(self.loadTXTList[x]) == 3):
                    if (len(self.loadTXTtoClear) == 2 or len(self.loadTXTtoClear) == 3):
                        self.Tab2AddItem = QListWidgetItem(self.loadTXTtoClear)
                        self.Tab2AddItem.setTextAlignment(Qt.AlignCenter)
                        self.Tab2AddItem.setSizeHint(QSize(0, 25))
                        self.Tab2input2.addItem(self.Tab2AddItem)

            self.Tab2layout.addWidget(self.Tab2input2, 1, 2, 1, 2)
            self.QTab2.setLayout(self.Tab2layout)

    def Tab2AddClick(self):
        text, ok = QInputDialog.getText(self, 'Add Dialog', 'Enter text:')
        if (ok):
            self.Tab2name2AddtoList = []
            self.Tab2name2AddtoList = re.compile('[가-힣]+').findall(str(text))
            self.Tab2name2Add = ''
            self.Tab2name2Add = self.Tab2name2Add.join(self.Tab2name2AddtoList)

            if (len(str(text)) == 2 or len(str(text)) == 3):
                if (len(self.Tab2name2Add) == 2 or len(self.Tab2name2Add) == 3):
                    self.Tab2AddItem = QListWidgetItem(self.Tab2name2Add)
                    self.Tab2AddItem.setTextAlignment(Qt.AlignCenter)
                    self.Tab2AddItem.setSizeHint(QSize(0, 25))
                    self.Tab2input2.addItem(self.Tab2AddItem)
                    self.Tab2layout.addWidget(self.Tab2input2, 1, 2, 1, 2)
                    self.QTab2.setLayout(self.Tab2layout)
                    return

    def Tab2RemoveClick(self):
        listItems = self.Tab2input2.selectedItems()
        if not listItems: return
        for item in listItems:
            self.Tab2input2.takeItem(self.Tab2input2.row(item))
    
    def Tab2ButtonClick(self):
        self.Tab2input1Text = ''.join(re.compile('[가-힣]+').findall(self.Tab2input1.text()))
        self.Tab2input2itemsList = []
        
        if (len(self.Tab2input1Text) == 2 or len(self.Tab2input1Text) == 3):
            if (len(self.Tab2input1.text()) == 2 or len(self.Tab2input1.text()) == 3):
                if (self.Tab2input2.count() != 0):
                    
                    self.Tab2Analyser(self.Tab2input1Text, self.Tab2input2itemsList)
                    return

        # 잘못된 입력
        self.alert = QMessageBox()
        self.alert.setIcon(QMessageBox.Critical)
        self.alert.setWindowTitle('Invalid Input')
        self.alert.setWindowIcon(QIcon('icons/NK.png'))
        self.alert.setText('Invalid Input. Please Retry.\nCondition : KR 2 or 3 Letter')
        self.alert.setStandardButtons(QMessageBox.Retry)
        self.alert.setDefaultButton(QMessageBox.Retry)
        self.ret = self.alert.exec_()

    def Tab2Analyser(self, Name1, Names2):
        self.Tab2NAME1col = []
        self.Tab2NAME2col = []
        self.Tab2RESULTcol = []

        for i in range(self.Tab2input2.count()):
            Names2.append(self.Tab2input2.item(i))

        # 모든 아이템을 가져와 글자로 변환
        for j in range(len(Names2)):
            Names2[j] = Names2[j].text()

         # 2글자 처리
        if (len(Name1) == 2):
            Name1 = Name1 + '○'

        for k in range(len(Names2)):
            if (len(Names2[k]) == 2):
                Names2[k] = Names2[k] + '○'

        for l in range(len(Names2)):
            self.Name1toList = []
            self.Name2toList = []

            for a in range(3):
                self.Name1toList.append(Name1[a])
                self.Name1toList[a] = Hangul.gyeopjamo(Hangul.jamo(self.Name1toList[a]))
                self.Name1toList[a] = Hangul.convertonumber(''.join(self.Name1toList[a]))
            for b in range(3):
                self.Name2toList.append(Names2[l][b])
                self.Name2toList[b] = Hangul.gyeopjamo(Hangul.jamo(self.Name2toList[b]))
                self.Name2toList[b] = Hangul.convertonumber(''.join(self.Name2toList[b]))

            self.Name1and2 = []
            for w in range(3):
                self.Name1and2.append(self.Name1toList[w])
                self.Name1and2.append(self.Name2toList[w])

            self.Name3List = []
            for x in range(5):
                self.Name3List.append(int(str((self.Name1and2[x] + self.Name1and2[x+1]))[-1]))

            self.Name4List = []
            for u in range(4):
                self.Name4List.append(int(str((self.Name3List[u] + self.Name3List[u+1]))[-1]))

            self.Name5List = []
            for v in range(3):
                self.Name5List.append(int(str((self.Name4List[v] + self.Name4List[v+1]))[-1]))

            self.Name6List = []
            for k in range(2):
                self.Name6List.append(int(str((self.Name5List[k] + self.Name5List[k+1]))[-1]))

            self.Tab2NAME1col.append(Name1)
            self.Tab2NAME2col.append(Names2[l])
            self.Tab2RESULTcol.append(str(self.Name6List[0]) + str(self.Name6List[1]) + '%')

        self.Tab2table = QTableWidget()
        self.Tab2table.setRowCount(len(Names2))
        self.Tab2table.setColumnCount(3)

        self.Tab2table.setColumnWidth(0, 145)
        self.Tab2table.setColumnWidth(1, 145)
        self.Tab2table.setColumnWidth(2, 145)

        self.header = self.Tab2table.horizontalHeader()       
        self.header.setSectionResizeMode(0, QHeaderView.Stretch)
        self.header.setSectionResizeMode(1, QHeaderView.Stretch)
        self.header.setSectionResizeMode(2, QHeaderView.Stretch)

        for q in range(len(Names2)):
            self.Tab2table.setItem(q, 0, QTableWidgetItem(self.Tab2NAME1col[q].replace('○','')))
            self.Tab2table.setItem(q, 1, QTableWidgetItem(self.Tab2NAME2col[q].replace('○','')))
            self.Tab2table.setItem(q, 2, QTableWidgetItem(self.Tab2RESULTcol[q].replace('○','')))

        self.Tab2layout.addWidget(self.Tab2table, 4, 0, 1, 4)

        # 최종 반영
        self.QTab2.setLayout(self.Tab2layout)



if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)

    fontDB = QFontDatabase()
    fontDB.addApplicationFont(path.abspath(path.join(path.dirname(__file__), 'fonts/SDGothicNeoM.ttf')))
    app.setFont(QFont('AppleSDGothicNeoM00', 11))

    window = MainWindow()

    # 테마 설정
    # DarkThemeFile = QFile(path.abspath(path.join(path.dirname(__file__), 'styles/style.qss')))
    # DarkThemeFile.open(QFile.ReadOnly | QFile.Text)
    # stream = QTextStream(DarkThemeFile)
    # app.setStyleSheet(stream.readAll())

    # 윈도우 뒤쪽 색 설정
    # palatte = window.palette()
    # palatte.setColor(window.backgroundRole(), Qt.white)
    # window.setPalette(palatte)

    window.show()
    sys.exit(app.exec())