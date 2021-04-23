from PyQt5.QtCore import QDateTime, Qt, QTimer, QSize, QTextStream, QFile, reset
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget, QMessageBox, QStackedWidget, QStatusBar, QDesktopWidget,
        QMainWindow, QMenuBar, QAction, QMenu, QListWidget, QListWidgetItem, QInputDialog, QToolBar, 
        QFileDialog, QTableWidgetItem, QHeaderView, QShortcut)

from PyQt5.QtGui import (QIcon, QColor, QPainter, QFontDatabase, QFont,
        QPixmap, QCursor, QKeySequence)

from PyQt5 import QtCore

import traceback
import datetime

from os import error, path
import os
import json
import re
import csv
import time

import Hangul

def WriteHandledError():
    filenamae = '[Checker] Error_{}.log'.format(str(datetime.datetime.now()).replace(' ','_').replace(':','-'))
    errormsg = str(traceback.format_exc())

    f = open(filenamae, 'w')
    f.write(errormsg)
    f.close()

    alert = QMessageBox()
    alert.setIcon(QMessageBox.Critical)
    alert.setWindowTitle('Error Occurred')
    alert.setWindowIcon(QIcon('icons/NK.png'))
    alert.setText('Error is logged in\n{}'.format(filenamae))
    alert.setDetailedText(errormsg)
    alert.setStandardButtons(QMessageBox.Ok)
    alert.setDefaultButton(QMessageBox.Ok)
    ret = alert.exec_()

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        if (os.path.exists('mod.txt') == True):
            self.strokeOrder = True
        else:
            self.strokeOrder = False
        # 다른곳에서 사용하는 변수 및 리스트 선언
        self.Tab2NAME1col = []
        self.Tab2NAME2col = []
        self.Tab2RESULTcol = []

        self.Tab3NAME1col = []
        self.Tab3NAME2col = []
        self.Tab3RESULTcol = []

        self.Tab3NAME1Count = 0
        self.Tab3NAME2Count = 0

        self.setWindowTitle('Korean Name Compatibility Checker GUI')
        self.iconfilename = path.abspath(path.join(path.dirname(__file__), 'icons/NK.png'))

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
        # self.QDev = QWidget()

        self.QTabs.addTab(self.QTab1, "𝟏 by 𝟏")
        self.QTabs.addTab(self.QTab2, "𝟏 by 𝒏")
        self.QTabs.addTab(self.QTab3, "𝒏 by 𝒏")
        self.QTabs.addTab(self.QGithub, "𝐄𝐭𝐜")
        # self.QTabs.addTab(self.QDev, "𝕯𝖊𝖛")
        
        self.layout.addWidget(self.QTabs)
        self.setLayout(self.layout)

        self.ShortCut()


        # 일단 사용하지 않음
        # self.Dev()

        self.Info()
        self.Tab1()
        self.Tab2()
        self.Tab3()

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

        self.SCTab3Plus1 = QShortcut(QKeySequence('Ctrl+K'), self)
        self.SCTab3Plus1.activated.connect(self.Tab3Plus1)
        self.SCTab3Plus2 = QShortcut(QKeySequence('Ctrl+L'), self)
        self.SCTab3Plus2.activated.connect(self.Tab3Plus2)

        self.SCTab3TXT1 = QShortcut(QKeySequence('Ctrl+F'), self)
        self.SCTab3TXT1.activated.connect(self.Tab3TXT1)
        self.SCTab3TXT2 = QShortcut(QKeySequence('Ctrl+G'), self)
        self.SCTab3TXT2.activated.connect(self.Tab3TXT2)

        self.SCTab3CSV1 = QShortcut(QKeySequence('Ctrl+V'), self)
        self.SCTab3CSV1.activated.connect(self.Tab3CSV1)
        self.SCTab3CSV2 = QShortcut(QKeySequence('Ctrl+B'), self)
        self.SCTab3CSV2.activated.connect(self.Tab3CSV2)

        self.SCTab3CSV2 = QShortcut(QKeySequence('Ctrl+D'), self)
        self.SCTab3CSV2.activated.connect(self.SDuplicate)

    def SDuplicate(self):
        self.Tab3DuplicateCheckBox.click()

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
            self.Tab3SaveAsCSV.click()

    def analysis(self):
        if (self.QTabs.currentIndex() == 0):
            self.Tab1analysisButton.click()
        elif (self.QTabs.currentIndex() == 1):
            self.Tab2analysisButton.click()
        elif (self.QTabs.currentIndex() == 2):
            self.Tab3analysisButton.click()

    def notSupportedError(self, Shortcut1, Shortcut2):
        self.alert = QMessageBox()
        self.alert.setIcon(QMessageBox.Information)
        self.alert.setWindowTitle('Not Supported')
        self.alert.setWindowIcon(QIcon('icons/NK.png'))
        self.alert.setText('Not Supported Shortcut in this Tab.\nUse {} and {} to Add Name to Each Box.'.format(Shortcut1, Shortcut2))
        self.alert.setStandardButtons(QMessageBox.Retry)
        self.alert.setDefaultButton(QMessageBox.Retry)
        self.ret = self.alert.exec_()
    
    def plus(self):
        if (self.QTabs.currentIndex() == 1):
            self.Tab2AddButton.click()
        elif (self.QTabs.currentIndex() == 2):
            self.notSupportedError('Ctrl+K','Ctrl+L')

    def Tab3Plus1(self):
        if (self.QTabs.currentIndex() == 2):
            self.Tab3AddButton1.click()

    def Tab3Plus2(self):
        if (self.QTabs.currentIndex() == 2):
            self.Tab3AddButton2.click()

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
            self.notSupportedError('Ctrl+Y','Ctrl+U')

    def Tab3TXT1(self):
        if (self.QTabs.currentIndex() == 2):
            self.Tab3TXTButton1.click()

    def Tab3TXT2(self):
        if (self.QTabs.currentIndex() == 2):
            self.Tab3TXTButton2.click()

    def CSV(self):
        if (self.QTabs.currentIndex() == 1):
            self.Tab2CSVButton.click()
        elif (self.QTabs.currentIndex() == 2):
            self.notSupportedError('Ctrl+F','Ctrl+G')

    def Tab3CSV1(self):
        if (self.QTabs.currentIndex() == 2):
            self.Tab3CSVButton1.click()

    def Tab3CSV2(self):
        if (self.QTabs.currentIndex() == 2):
            self.Tab3CSVButton2.click()

    def Info(self):
        self.Infolayout = QGridLayout(self)
        self.Infolayout.setAlignment(Qt.AlignTop)
        # self.Infolayout.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

        self.octocat = QLabel(self)
        self.octocat.setScaledContents(True)
        self.octocat.setPixmap(QPixmap(path.abspath(path.join(path.dirname(__file__), 'icons/github.png'))))
        self.octocat.setFixedSize(64, 64)

        self.sourceLink = QLabel('Source Code : <a href="https://github.com/STR-HK/Knac">Repository Link</a>')
        self.sourceLink.setOpenExternalLinks(True)

        self.font = QLabel(self)
        self.font.setScaledContents(True)
        self.font.setPixmap(QPixmap(path.abspath(path.join(path.dirname(__file__), 'icons/font.png'))))
        self.font.setFixedSize(64, 64)

        self.fontsourceLink = QLabel('NanumSquareOTF ac Bold : <a href="https://hangeul.naver.com/font">Site Link</a>')
        self.fontsourceLink.setOpenExternalLinks(True)

        groupbox = QGroupBox('Calculate Way Settings')
        rbtn1 = QRadioButton('By Line Number', self)
        rbtn2 = QRadioButton('By Stroke Order', self)
        if self.strokeOrder == False:
            rbtn1.setChecked(True)
        elif self.strokeOrder == True:
            rbtn2.setChecked(True)
        rbtn1.clicked.connect(self.ChangeMod)
        rbtn2.clicked.connect(self.ChangeMod)
        
        vbox = QVBoxLayout()
        vbox.addWidget(rbtn1)
        vbox.addWidget(rbtn2)
        groupbox.setLayout(vbox)

        self.Infolayout.addWidget(groupbox, 0, 1, 1, 3)
        self.Infolayout.addWidget(self.font, 1, 1, 1, 1)
        self.Infolayout.addWidget(self.fontsourceLink, 1, 2, 1, 2)
        self.Infolayout.addWidget(self.octocat, 2, 1, 1, 1)
        self.Infolayout.addWidget(self.sourceLink, 2, 2, 1, 2)
        
        
        self.QGithub.setLayout(self.Infolayout)

    def ChangeMod(self):
        if self.strokeOrder == False:
            f = open('mod.txt','w')
            f.write('This File is Setting File of KNAC DON\'T Remove.')
            f.close()
            self.strokeOrder = True
        else:
            os.remove('mod.txt')
            self.strokeOrder = False

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
        # self.QDev.setLayout(self.Devlayout)

    def inValidMsg(self):
        self.alert = QMessageBox()
        self.alert.setIcon(QMessageBox.Critical)
        self.alert.setWindowTitle('Invalid Input')
        self.alert.setWindowIcon(QIcon(path.abspath(path.join(path.dirname(__file__), 'icons/NK.png'))))
        self.alert.setText('Invalid Input. Please Retry.\nCondition : KR 2 or 3 Letter')
        self.alert.setStandardButtons(QMessageBox.Retry)
        self.alert.setDefaultButton(QMessageBox.Retry)
        self.ret = self.alert.exec_()

    def Tab1Ready(self):
        # Tab1의 보여주기 트리 생성
        self.Tab1TreeLayer1 = QGridLayout(self)
        self.Tab1TreeLayer2 = QGridLayout(self)
        self.Tab1TreeLayer3 = QGridLayout(self)
        self.Tab1TreeLayer4 = QGridLayout(self)
        self.Tab1TreeLayer5 = QGridLayout(self)
        self.Tab1TreeLayer6 = QGridLayout(self)

        self.Tab1TreeLayer1Text1 = QLabel(' ')
        self.Tab1TreeLayer1Text1.setStyleSheet('font-size: 20px;''padding : 5px;''background-color: #E8E8E8')
        self.Tab1TreeLayer1Text1.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer1Text2 = QLabel(' ')
        self.Tab1TreeLayer1Text2.setStyleSheet('font-size: 20px;''padding : 5px;''background-color: #F0F0F0')
        self.Tab1TreeLayer1Text2.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer1Text3 = QLabel(' ')
        self.Tab1TreeLayer1Text3.setStyleSheet('font-size: 20px;''padding : 5px;''background-color: #F0F0F0')
        self.Tab1TreeLayer1Text3.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer1Text4 = QLabel(' ')
        self.Tab1TreeLayer1Text4.setStyleSheet('font-size: 20px;''padding : 5px;''background-color: #F0F0F0')
        self.Tab1TreeLayer1Text4.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer1Text5 = QLabel(' ')
        self.Tab1TreeLayer1Text5.setStyleSheet('font-size: 20px;''padding : 5px;''background-color: #F0F0F0')
        self.Tab1TreeLayer1Text5.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer1Text6 = QLabel(' ')
        self.Tab1TreeLayer1Text6.setStyleSheet('font-size: 20px;''padding : 5px;''background-color: #F0F0F0')
        self.Tab1TreeLayer1Text6.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer2Text1 = QLabel(' ')
        self.Tab1TreeLayer2Text1.setStyleSheet('font-size: 15px;''padding-top : 2px;''padding-bottom : 1px;''background-color: #E0E0E0')
        self.Tab1TreeLayer2Text1.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer2Text2 = QLabel(' ')
        self.Tab1TreeLayer2Text2.setStyleSheet('font-size: 15px;''padding-top : 2px;''padding-bottom : 1px;''background-color: #E0E0E0')
        self.Tab1TreeLayer2Text2.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer2Text3 = QLabel(' ')
        self.Tab1TreeLayer2Text3.setStyleSheet('font-size: 15px;''padding-top : 2px;''padding-bottom : 1px;''background-color: #E0E0E0')
        self.Tab1TreeLayer2Text3.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer2Text4 = QLabel(' ')
        self.Tab1TreeLayer2Text4.setStyleSheet('font-size: 15px;''padding-top : 2px;''padding-bottom : 1px;''background-color: #E0E0E0')
        self.Tab1TreeLayer2Text4.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer2Text5 = QLabel(' ')
        self.Tab1TreeLayer2Text5.setStyleSheet('font-size: 15px;''padding-top : 2px;''padding-bottom : 1px;''background-color: #E0E0E0')
        self.Tab1TreeLayer2Text5.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer2Text6 = QLabel(' ')
        self.Tab1TreeLayer2Text6.setStyleSheet('font-size: 15px;''padding-top : 2px;''padding-bottom : 1px;''background-color: #E0E0E0')
        self.Tab1TreeLayer2Text6.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer3Text0 = QLabel(' ')
        self.Tab1TreeLayer3Text0.setStyleSheet('font-size: 15px;''padding-top : 2px;''padding-bottom : 1px;''background-color: white')
        self.Tab1TreeLayer3Text0.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer3Text1 = QLabel(' ')
        self.Tab1TreeLayer3Text1.setStyleSheet('font-size: 15px;''padding-top : 2px;''padding-bottom : 1px;''background-color: #DCDCDC')
        self.Tab1TreeLayer3Text1.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer3Text15 = QLabel(' ')
        self.Tab1TreeLayer3Text15.setStyleSheet('font-size: 15px;''padding-top : 2px;''padding-bottom : 1px;''background-color: white')
        self.Tab1TreeLayer3Text15.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer3Text2 = QLabel(' ')
        self.Tab1TreeLayer3Text2.setStyleSheet('font-size: 15px;''padding-top : 2px;''padding-bottom : 1px;''background-color: #DCDCDC')
        self.Tab1TreeLayer3Text2.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer3Text25 = QLabel(' ')
        self.Tab1TreeLayer3Text25.setStyleSheet('font-size: 15px;''padding-top : 2px;''padding-bottom : 1px;''background-color: white')
        self.Tab1TreeLayer3Text25.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer3Text3 = QLabel(' ')
        self.Tab1TreeLayer3Text3.setStyleSheet('font-size: 15px;''padding-top : 2px;''padding-bottom : 1px;''background-color: #DCDCDC')
        self.Tab1TreeLayer3Text3.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer3Text35 = QLabel(' ')
        self.Tab1TreeLayer3Text35.setStyleSheet('font-size: 15px;''padding-top : 2px;''padding-bottom : 1px;''background-color: white')
        self.Tab1TreeLayer3Text35.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer3Text4 = QLabel(' ')
        self.Tab1TreeLayer3Text4.setStyleSheet('font-size: 15px;''padding-top : 2px;''padding-bottom : 1px;''background-color: #DCDCDC')
        self.Tab1TreeLayer3Text4.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer3Text45 = QLabel(' ')
        self.Tab1TreeLayer3Text45.setStyleSheet('font-size: 15px;''padding-top : 2px;''padding-bottom : 1px;''background-color: white')
        self.Tab1TreeLayer3Text45.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer3Text5 = QLabel(' ')
        self.Tab1TreeLayer3Text5.setStyleSheet('font-size: 15px;''padding-top : 2px;''padding-bottom : 1px;''background-color: #DCDCDC')
        self.Tab1TreeLayer3Text5.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer3Text55 = QLabel(' ')
        self.Tab1TreeLayer3Text55.setStyleSheet('font-size: 15px;''padding-top : 2px;''padding-bottom : 1px;''background-color: white')
        self.Tab1TreeLayer3Text55.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer4Text0 = QLabel(' ')
        self.Tab1TreeLayer4Text0.setStyleSheet('font-size: 15px;''padding-top : 2px;''padding-bottom : 1px;''background-color: white')
        self.Tab1TreeLayer4Text0.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer4Text1 = QLabel(' ')
        self.Tab1TreeLayer4Text1.setStyleSheet('font-size: 15px;''padding-top : 2px;''padding-bottom : 1px;''background-color: #D8D8D8')
        self.Tab1TreeLayer4Text1.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer4Text2 = QLabel(' ')
        self.Tab1TreeLayer4Text2.setStyleSheet('font-size: 15px;''padding-top : 2px;''padding-bottom : 1px;''background-color: #D8D8D8')
        self.Tab1TreeLayer4Text2.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer4Text3 = QLabel(' ')
        self.Tab1TreeLayer4Text3.setStyleSheet('font-size: 15px;''padding-top : 2px;''padding-bottom : 1px;''background-color: #D8D8D8')
        self.Tab1TreeLayer4Text3.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer4Text4 = QLabel(' ')
        self.Tab1TreeLayer4Text4.setStyleSheet('font-size: 15px;''padding-top : 2px;''padding-bottom : 1px;''background-color: #D8D8D8')
        self.Tab1TreeLayer4Text4.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer4Text5 = QLabel(' ')
        self.Tab1TreeLayer4Text5.setStyleSheet('font-size: 15px;''padding-top : 2px;''padding-bottom : 1px;''background-color: white')
        self.Tab1TreeLayer4Text5.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer5Text0 = QLabel(' ')
        self.Tab1TreeLayer5Text0.setStyleSheet('font-size: 15px;''padding-top : 2px;''padding-bottom : 1px;''background-color: white')
        self.Tab1TreeLayer5Text0.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer5Text1 = QLabel(' ')
        self.Tab1TreeLayer5Text1.setStyleSheet('font-size: 15px;''padding-top : 2px;''padding-bottom : 1px;''background-color: white')
        self.Tab1TreeLayer5Text1.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer5Text2 = QLabel(' ')
        self.Tab1TreeLayer5Text2.setStyleSheet('font-size: 15px;''padding-top : 2px;''padding-bottom : 1px;''background-color: #D3D3D3')
        self.Tab1TreeLayer5Text2.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer5Text3 = QLabel(' ')
        self.Tab1TreeLayer5Text3.setStyleSheet('font-size: 15px;''padding-top : 2px;''padding-bottom : 1px;''background-color: #D3D3D3')
        self.Tab1TreeLayer5Text3.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer5Text4 = QLabel(' ')
        self.Tab1TreeLayer5Text4.setStyleSheet('font-size: 15px;''padding-top : 2px;''padding-bottom : 1px;''background-color: #D3D3D3')
        self.Tab1TreeLayer5Text4.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer5Text5 = QLabel(' ')
        self.Tab1TreeLayer5Text5.setStyleSheet('font-size: 15px;''padding-top : 2px;''padding-bottom : 1px;''background-color: white')
        self.Tab1TreeLayer5Text5.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer5Text6 = QLabel(' ')
        self.Tab1TreeLayer5Text6.setStyleSheet('font-size: 15px;''padding-top : 2px;''padding-bottom : 1px;''background-color: white')
        self.Tab1TreeLayer5Text6.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer6Text0 = QLabel(' ')
        self.Tab1TreeLayer6Text0.setStyleSheet('font-size: 15px;''padding-top : 2px;''padding-bottom : 1px;''background-color: white')
        self.Tab1TreeLayer6Text0.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer6Text1 = QLabel(' ')
        self.Tab1TreeLayer6Text1.setStyleSheet('font-size: 15px;''padding-top : 2px;''padding-bottom : 1px;''background-color: white')
        self.Tab1TreeLayer6Text1.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer6Text2 = QLabel(' ')
        self.Tab1TreeLayer6Text2.setStyleSheet('font-size: 25px;''padding-top : 2.5px;''padding-bottom : 2.5px;''background-color: #D0D0D0')
        self.Tab1TreeLayer6Text2.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer6Text3 = QLabel(' ')
        self.Tab1TreeLayer6Text3.setStyleSheet('font-size: 15px;''padding-top : 2px;''padding-bottom : 1px;''background-color: white')
        self.Tab1TreeLayer6Text3.setAlignment(QtCore.Qt.AlignCenter)
        self.Tab1TreeLayer6Text4 = QLabel(' ')
        self.Tab1TreeLayer6Text4.setStyleSheet('font-size: 15px;''padding-top : 2px;''padding-bottom : 1px;''background-color: white')
        self.Tab1TreeLayer6Text4.setAlignment(QtCore.Qt.AlignCenter)

        self.Tab1TreeLayer1.addWidget(self.Tab1TreeLayer1Text1, 0, 0)
        self.Tab1TreeLayer1.addWidget(self.Tab1TreeLayer1Text2, 0, 1)
        self.Tab1TreeLayer1.addWidget(self.Tab1TreeLayer1Text3, 0, 2)
        self.Tab1TreeLayer1.addWidget(self.Tab1TreeLayer1Text4, 0, 3)
        self.Tab1TreeLayer1.addWidget(self.Tab1TreeLayer1Text5, 0, 4)
        self.Tab1TreeLayer1.addWidget(self.Tab1TreeLayer1Text6, 0, 5)
        self.Tab1TreeLayer2.addWidget(self.Tab1TreeLayer2Text1, 0, 0)
        self.Tab1TreeLayer2.addWidget(self.Tab1TreeLayer2Text2, 0, 1)
        self.Tab1TreeLayer2.addWidget(self.Tab1TreeLayer2Text3, 0, 2)
        self.Tab1TreeLayer2.addWidget(self.Tab1TreeLayer2Text4, 0, 3)
        self.Tab1TreeLayer2.addWidget(self.Tab1TreeLayer2Text5, 0, 4)
        self.Tab1TreeLayer2.addWidget(self.Tab1TreeLayer2Text6, 0, 5)
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
        self.Tab1TreeLayer4.addWidget(self.Tab1TreeLayer4Text0, 0, 1)
        self.Tab1TreeLayer4.addWidget(self.Tab1TreeLayer4Text1, 0, 2)
        self.Tab1TreeLayer4.addWidget(self.Tab1TreeLayer4Text2, 0, 3)
        self.Tab1TreeLayer4.addWidget(self.Tab1TreeLayer4Text3, 0, 4)
        self.Tab1TreeLayer4.addWidget(self.Tab1TreeLayer4Text4, 0, 5)
        self.Tab1TreeLayer4.addWidget(self.Tab1TreeLayer4Text5, 0, 6)
        self.Tab1TreeLayer5.addWidget(self.Tab1TreeLayer5Text0, 0, 1)
        self.Tab1TreeLayer5.addWidget(self.Tab1TreeLayer5Text1, 0, 2)
        self.Tab1TreeLayer5.addWidget(self.Tab1TreeLayer5Text2, 0, 3)
        self.Tab1TreeLayer5.addWidget(self.Tab1TreeLayer5Text3, 0, 4)
        self.Tab1TreeLayer5.addWidget(self.Tab1TreeLayer5Text4, 0, 5)
        self.Tab1TreeLayer5.addWidget(self.Tab1TreeLayer5Text5, 0, 6)
        self.Tab1TreeLayer5.addWidget(self.Tab1TreeLayer5Text6, 0, 7)
        self.Tab1TreeLayer6.addWidget(self.Tab1TreeLayer6Text0, 0, 1, 1, 1)
        self.Tab1TreeLayer6.addWidget(self.Tab1TreeLayer6Text1, 0, 2, 1, 1)
        self.Tab1TreeLayer6.addWidget(self.Tab1TreeLayer6Text2, 0, 3, 1, 1)
        self.Tab1TreeLayer6.addWidget(self.Tab1TreeLayer6Text3, 0, 4, 1, 1)
        self.Tab1TreeLayer6.addWidget(self.Tab1TreeLayer6Text4, 0, 5, 1, 1)

        # self.Tab1Tree.addLayout(self.Tab1TreeLayer1, 0, 0)
        # self.Tab1Tree.addLayout(self.Tab1TreeLayer2, 1, 0)
        # self.Tab1Tree.addLayout(self.Tab1TreeLayer3, 2, 0)
        # self.Tab1Tree.addLayout(self.Tab1TreeLayer4, 3, 0)
        # self.Tab1Tree.addLayout(self.Tab1TreeLayer5, 4, 0)
        # self.Tab1Tree.addLayout(self.Tab1TreeLayer6, 5, 0)

        self.Tab1layout.addLayout(self.Tab1TreeLayer1, 3, 0, 1, 2)
        self.Tab1layout.addLayout(self.Tab1TreeLayer2, 4, 0, 1, 2)
        self.Tab1layout.addLayout(self.Tab1TreeLayer3, 5, 0, 1, 2)
        self.Tab1layout.addLayout(self.Tab1TreeLayer4, 6, 0, 1, 2)
        self.Tab1layout.addLayout(self.Tab1TreeLayer5, 7, 0, 1, 2)
        self.Tab1layout.addLayout(self.Tab1TreeLayer6, 8, 0, 1, 2)

        # self.QTab1.setLayout(self.Tab1layout)


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

        self.Tab1Ready()

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
        self.inValidMsg()

    def Tab1Analyser(self, Name1, Name2):
        # 2글자 이름의 경우에는 ○ 붙이기
        if (len(Name1) == 2):
            Name1 = Name1 + '○'
        if (len(Name2) == 2):
            Name2 = Name2 + '○'

        # 첫번째 줄 코드
        self.Tab1TreeLayer1Text1.setText(Name1[0])
        self.Tab1TreeLayer1Text2.setText(Name2[0])
        self.Tab1TreeLayer1Text3.setText(Name1[1])
        self.Tab1TreeLayer1Text4.setText(Name2[1])
        self.Tab1TreeLayer1Text5.setText(Name1[2])
        self.Tab1TreeLayer1Text6.setText(Name2[2])
        
        # 이름 글자별로 넣을 리스트 생성
        self.Name1toList = []
        self.Name2toList = []
        
        # 이름을 글자별로 리스트에 넣음
        for a in range(3):
            self.Name1toList.append(Name1[a])
            self.Name1toList[a] = Hangul.gyeopjamo(Hangul.jamo(self.Name1toList[a]))
            self.Name1toList[a] = Hangul.convertonumber(''.join(self.Name1toList[a]), self.strokeOrder)
        for b in range(3):
            self.Name2toList.append(Name2[b])
            self.Name2toList[b] = Hangul.gyeopjamo(Hangul.jamo(self.Name2toList[b]))
            self.Name2toList[b] = Hangul.convertonumber(''.join(self.Name2toList[b]), self.strokeOrder)

        # 두번째 줄 코드
        self.Tab1TreeLayer2Text1.setText(str(self.Name1toList[0]))
        self.Tab1TreeLayer2Text2.setText(str(self.Name2toList[0]))
        self.Tab1TreeLayer2Text3.setText(str(self.Name1toList[1]))
        self.Tab1TreeLayer2Text4.setText(str(self.Name2toList[1]))
        self.Tab1TreeLayer2Text5.setText(str(self.Name1toList[2]))
        self.Tab1TreeLayer2Text6.setText(str(self.Name2toList[2]))

        self.Name1and2 = []
        for w in range(3):
            self.Name1and2.append(self.Name1toList[w])
            self.Name1and2.append(self.Name2toList[w])

        self.Name3List = []

        for x in range(5):
            self.Name3List.append(int(str((self.Name1and2[x] + self.Name1and2[x+1]))[-1]))

        # 세번째 줄 코드
        self.Tab1TreeLayer3Text0.setText(' ')
        self.Tab1TreeLayer3Text1.setText(str(self.Name3List[0]))
        self.Tab1TreeLayer3Text15.setText(' ')
        self.Tab1TreeLayer3Text2.setText(str(self.Name3List[1]))
        self.Tab1TreeLayer3Text25.setText(' ')
        self.Tab1TreeLayer3Text3.setText(str(self.Name3List[2]))
        self.Tab1TreeLayer3Text35.setText(' ')
        self.Tab1TreeLayer3Text4.setText(str(self.Name3List[3]))
        self.Tab1TreeLayer3Text45.setText(' ')
        self.Tab1TreeLayer3Text5.setText(str(self.Name3List[4]))
        self.Tab1TreeLayer3Text55.setText(' ')

        self.Name4List = []

        for u in range(4):
            self.Name4List.append(int(str((self.Name3List[u] + self.Name3List[u+1]))[-1]))

        # 네번째 줄 코드
        self.Tab1TreeLayer4Text0.setText(' ')
        self.Tab1TreeLayer4Text1.setText(str(self.Name4List[0]))
        self.Tab1TreeLayer4Text2.setText(str(self.Name4List[1]))
        self.Tab1TreeLayer4Text3.setText(str(self.Name4List[2]))
        self.Tab1TreeLayer4Text4.setText(str(self.Name4List[3]))
        self.Tab1TreeLayer4Text5.setText(' ')

        self.Name5List = []

        for v in range(3):
            self.Name5List.append(int(str((self.Name4List[v] + self.Name4List[v+1]))[-1]))

        # 다섯번째 줄 코드
        self.Tab1TreeLayer5Text0.setText(' ')
        self.Tab1TreeLayer5Text1.setText(' ')
        self.Tab1TreeLayer5Text2.setText(str(self.Name5List[0]))
        self.Tab1TreeLayer5Text3.setText(str(self.Name5List[1]))
        self.Tab1TreeLayer5Text4.setText(str(self.Name5List[2]))
        self.Tab1TreeLayer5Text5.setText(' ')
        self.Tab1TreeLayer5Text6.setText(' ')

        self.Name6List = []

        for k in range(2):
            self.Name6List.append(int(str((self.Name5List[k] + self.Name5List[k+1]))[-1]))

        # 여섯번째 줄 코드
        self.Tab1TreeLayer6Text0.setText(' ')
        self.Tab1TreeLayer6Text1.setText(' ')
        self.Tab1TreeLayer6Text2.setText(str(self.Name6List[0]) + str(self.Name6List[1]) + '%')
        self.Tab1TreeLayer6Text3.setText(' ')
        self.Tab1TreeLayer6Text4.setText(' ')

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
            self.alert.setWindowIcon(QIcon(path.abspath(path.join(path.dirname(__file__), 'icons/NK.png'))))
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
        try:
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

            # self.Tab2layout.addWidget(self.Tab2input2, 1, 2, 1, 2)
            # self.QTab2.setLayout(self.Tab2layout)
        except:
            WriteHandledError()
        


    def Tab2CSVClick(self):
        self.loadTXT = QFileDialog()
        self.loadTXT.setFileMode(QFileDialog.AnyFile)
        self.loadTXTfilename = self.loadTXT.getOpenFileName(
            caption='Open CSV file', filter="Comma-Separated Values (*.csv)")

        if self.loadTXTfilename:
            if self.loadTXTfilename[0] == '':
                return
            
            f = open(self.loadTXTfilename[0], 'r',  encoding='utf-8')
            self.loadTXTList = f.read().replace('\ufeff','').split('\n')

            for x in range(len(self.loadTXTList)):
                self.loadTXTtoClear = ''.join(re.compile('[가-힣]+').findall(self.loadTXTList[x]))
                if (len(self.loadTXTList[x]) == 2 or len(self.loadTXTList[x]) == 3):
                    if (len(self.loadTXTtoClear) == 2 or len(self.loadTXTtoClear) == 3):
                        self.Tab2AddItem = QListWidgetItem(self.loadTXTtoClear)
                        self.Tab2AddItem.setTextAlignment(Qt.AlignCenter)
                        self.Tab2AddItem.setSizeHint(QSize(0, 25))
                        self.Tab2input2.addItem(self.Tab2AddItem)

            # self.Tab2layout.addWidget(self.Tab2input2, 1, 2, 1, 2)
            # self.QTab2.setLayout(self.Tab2layout)

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
                    # self.Tab2layout.addWidget(self.Tab2input2, 1, 2, 1, 2)
                    # self.QTab2.setLayout(self.Tab2layout)
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
        self.inValidMsg()

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
                self.Name1toList[a] = Hangul.convertonumber(''.join(self.Name1toList[a]), self.strokeOrder)
            for b in range(3):
                self.Name2toList.append(Names2[l][b])
                self.Name2toList[b] = Hangul.gyeopjamo(Hangul.jamo(self.Name2toList[b]))
                self.Name2toList[b] = Hangul.convertonumber(''.join(self.Name2toList[b]), self.strokeOrder)

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
            self.Tab2table.setItem(q, 2, QTableWidgetItem(self.Tab2RESULTcol[q]))

        self.Tab2layout.addWidget(self.Tab2table, 4, 0, 1, 4)

        # 최종 반영
        # self.QTab2.setLayout(self.Tab2layout)

    def Tab3(self):
        self.Tab3layout = QGridLayout(self)
        self.Tab3layout.setAlignment(Qt.AlignTop)

        self.GroupBox1 = QGroupBox('NAME 1')
        self.GroupBox2 = QGroupBox('NAME 2')
        self.Hbox1 = QHBoxLayout()
        self.Hbox15 = QHBoxLayout()
        self.Hbox2 = QHBoxLayout()
        self.Hbox25 = QHBoxLayout()

        self.Vbox1 = QVBoxLayout()
        self.Vbox2 = QVBoxLayout()

        self.Tab3TXTButton1 = QPushButton()
        self.Tab3TXTButton1.setText('TXT 1')
        self.Tab3TXTButton1.setFixedHeight(20)
        self.Tab3TXTButton1.clicked.connect(self.Tab3TXTButton1Click)
        self.Tab3CSVButton1 = QPushButton()
        self.Tab3CSVButton1.setText('CSV 1')
        self.Tab3CSVButton1.setFixedHeight(20)
        self.Tab3CSVButton1.clicked.connect(self.Tab3CSVButton1Click)
        self.Tab3AddButton1 = QPushButton()
        self.Tab3AddButton1.setText('+')
        self.Tab3AddButton1.setFixedHeight(20)
        self.Tab3AddButton1.clicked.connect(self.Tab3AddButton1Click)
        self.Tab3RemoveButton1 = QPushButton()
        self.Tab3RemoveButton1.setText('-')
        self.Tab3RemoveButton1.setFixedHeight(20)
        self.Tab3RemoveButton1.clicked.connect(self.Tab3RemoveButton1Click)
        self.Hbox1.addWidget(self.Tab3TXTButton1)
        self.Hbox1.addWidget(self.Tab3CSVButton1)
        self.Hbox15.addWidget(self.Tab3AddButton1)
        self.Hbox15.addWidget(self.Tab3RemoveButton1)

        self.Vbox1.addLayout(self.Hbox1)
        self.Vbox1.addLayout(self.Hbox15)

        self.Tab3TXTButton2 = QPushButton()
        self.Tab3TXTButton2.setText('TXT 2')
        self.Tab3TXTButton2.setFixedHeight(20)
        self.Tab3TXTButton2.clicked.connect(self.Tab3TXTButton2Click)
        self.Tab3CSVButton2 = QPushButton()
        self.Tab3CSVButton2.setText('CSV 2')
        self.Tab3CSVButton2.setFixedHeight(20)
        self.Tab3CSVButton2.clicked.connect(self.Tab3CSVButton2Click)
        self.Tab3AddButton2 = QPushButton()
        self.Tab3AddButton2.setText('+')
        self.Tab3AddButton2.setFixedHeight(20)
        self.Tab3AddButton2.clicked.connect(self.Tab3AddButton2Click)
        self.Tab3RemoveButton2 = QPushButton()
        self.Tab3RemoveButton2.setText('-')
        self.Tab3RemoveButton2.setFixedHeight(20)
        self.Tab3RemoveButton2.clicked.connect(self.Tab3RemoveButton2Click)
        self.Hbox2.addWidget(self.Tab3TXTButton2)
        self.Hbox2.addWidget(self.Tab3CSVButton2)
        self.Hbox25.addWidget(self.Tab3AddButton2)
        self.Hbox25.addWidget(self.Tab3RemoveButton2)

        self.Vbox2.addLayout(self.Hbox2)
        self.Vbox2.addLayout(self.Hbox25)

        self.GroupBox1.setLayout(self.Vbox1)
        self.GroupBox1.setFixedHeight(220)
        self.GroupBox1.setAlignment(Qt.AlignCenter)
        self.GroupBox2.setLayout(self.Vbox2)
        self.GroupBox2.setFixedHeight(220)
        self.GroupBox2.setAlignment(Qt.AlignCenter)

        self.Tab3input1 = QListWidget()
        self.Tab3input1.setFixedHeight(128)
        self.Tab3input2 = QListWidget()
        self.Tab3input2.setFixedHeight(128)

        self.Vbox1.addWidget(self.Tab3input1)
        self.Vbox2.addWidget(self.Tab3input2)

        self.Tab3DuplicateCheckBox = QPushButton('Duplicate\nL to R')
        self.Tab3DuplicateCheckBox.setStyleSheet('font-size: 11px')
        self.Tab3DuplicateCheckBox.setFixedHeight(32)
        self.Tab3DuplicateCheckBox.clicked.connect(self.Duplicate)

        self.Tab3analysisButton = QPushButton('Analysis (It will take some time)')
        self.Tab3analysisButton.setFixedHeight(32)
        self.Tab3analysisButton.clicked.connect(self.Tab3ButtonClick)

        self.Tab3Blank1 = QLabel('\n')
        self.Tab3table = QTableWidget()
        self.Tab3Blank2 = QLabel('\n')

        self.Tab3SaveAsCSV = QPushButton('SAVE AS CSV')
        self.Tab3SaveAsCSV.setFixedHeight(27)
        self.Tab3SaveAsCSV.clicked.connect(self.Tab3SaveCSV)

        self.Tab3layout.addWidget(self.GroupBox1, 0, 0, 1, 2)
        self.Tab3layout.addWidget(self.GroupBox2, 0, 2, 1, 2)
        self.Tab3layout.addWidget(self.Tab3DuplicateCheckBox, 1, 3, 1, 1)
        self.Tab3layout.addWidget(self.Tab3analysisButton, 1, 0, 1, 3)
        self.Tab3layout.addWidget(self.Tab3Blank1, 2, 0, 1, 4)
        self.Tab3layout.addWidget(self.Tab3table, 3, 0, 1, 4)
        self.Tab3layout.addWidget(self.Tab3SaveAsCSV, 4, 0, 1, 4)

        # 최종 반영
        self.QTab3.setLayout(self.Tab3layout)

    def Tab3SaveCSV(self):
        if (self.Tab3NAME1col == [] or self.Tab3NAME2col == []):
            self.alert = QMessageBox()
            self.alert.setIcon(QMessageBox.Critical)
            self.alert.setWindowTitle('No Data Exists')
            self.alert.setWindowIcon(QIcon(path.abspath(path.join(path.dirname(__file__), 'icons/NK.png'))))
            self.alert.setText('No Data Exists.\nPlease Analysis First.')
            self.alert.setStandardButtons(QMessageBox.Retry)
            self.alert.setDefaultButton(QMessageBox.Retry)
            self.ret = self.alert.exec_()
            return
        
        defaultFileName = self.Tab3NAME1col[0].replace('○','') + ' +' + str(self.Tab3NAME1Count - 1) + ', ' + self.Tab3NAME1col[0].replace('○','') + ' +' + str(self.Tab3NAME2Count - 1) + '.csv'
        name = QFileDialog.getSaveFileName(self, 'Save file', defaultFileName, "Comma-Separated Values (*.csv)")

        if name == ('', ''):
            return
        
        with open(list(name)[0], mode='w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            for h in range(self.Tab3NAME1Count * self.Tab3NAME2Count):
                csv_writer.writerow([self.Tab3NAME1col[h].replace('○',''), self.Tab3NAME2col[h].replace('○',''), self.Tab3RESULTcol[h]])

            # for f in range(len(self.Tab2NAME1col)):
            #     csv_writer.writerow([self.Tab2NAME1col[f].replace('○',''), self.Tab2NAME2col[f].replace('○',''), self.Tab2RESULTcol[f]])

    def Duplicate(self):
        self.Tab3input2.clear()
        for i in range(self.Tab3input1.count()):
            self.Tab3AddItem = QListWidgetItem(self.Tab3input1.item(i))
            self.Tab3AddItem.setTextAlignment(Qt.AlignCenter)
            self.Tab3AddItem.setSizeHint(QSize(0, 25))
            self.Tab3input2.addItem(self.Tab3AddItem)

    def Tab3TXTButton1Click(self):
        try:
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
                            self.Tab3AddItem = QListWidgetItem(self.loadTXTtoClear)
                            self.Tab3AddItem.setTextAlignment(Qt.AlignCenter)
                            self.Tab3AddItem.setSizeHint(QSize(0, 25))
                            self.Tab3input1.addItem(self.Tab3AddItem)

            # self.Vbox1.addWidget(self.Tab3input1)

        except:
            WriteHandledError()

    def Tab3CSVButton1Click(self):
        self.loadCSV = QFileDialog()
        self.loadCSV.setFileMode(QFileDialog.AnyFile)
        self.loadCSVfilename = self.loadCSV.getOpenFileName(
            caption='Open CSV file', filter="Comma-Separated Values (*.csv)")

        if self.loadCSVfilename:
            if self.loadCSVfilename[0] == '':
                return
            
            f = open(self.loadCSVfilename[0], 'r',  encoding='utf-8')
            self.loadCSVList = f.read().replace('\ufeff','').split('\n')

            for x in range(len(self.loadCSVList)):
                self.loadCSVtoClear = ''.join(re.compile('[가-힣]+').findall(self.loadCSVList[x]))
                if (len(self.loadCSVList[x]) == 2 or len(self.loadCSVList[x]) == 3):
                    if (len(self.loadCSVtoClear) == 2 or len(self.loadCSVtoClear) == 3):
                        self.Tab3AddItem = QListWidgetItem(self.loadCSVtoClear)
                        self.Tab3AddItem.setTextAlignment(Qt.AlignCenter)
                        self.Tab3AddItem.setSizeHint(QSize(0, 25))
                        self.Tab3input1.addItem(self.Tab3AddItem)

            # self.Vbox1.addWidget(self.Tab3input1)

    def Tab3TXTButton2Click(self):
        try:
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
                            self.Tab3AddItem = QListWidgetItem(self.loadTXTtoClear)
                            self.Tab3AddItem.setTextAlignment(Qt.AlignCenter)
                            self.Tab3AddItem.setSizeHint(QSize(0, 25))
                            self.Tab3input2.addItem(self.Tab3AddItem)

            # self.Vbox2.addWidget(self.Tab3input2)

        except:
            WriteHandledError()

    def Tab3CSVButton2Click(self):
        self.loadCSV = QFileDialog()
        self.loadCSV.setFileMode(QFileDialog.AnyFile)
        self.loadCSVfilename = self.loadCSV.getOpenFileName(
            caption='Open CSV file', filter="Comma-Separated Values (*.csv)")

        if self.loadCSVfilename:
            if self.loadCSVfilename[0] == '':
                return
            
            f = open(self.loadCSVfilename[0], 'r',  encoding='utf-8')
            self.loadCSVList = f.read().replace('\ufeff','').split('\n')

            for x in range(len(self.loadCSVList)):
                self.loadCSVtoClear = ''.join(re.compile('[가-힣]+').findall(self.loadCSVList[x]))
                if (len(self.loadCSVList[x]) == 2 or len(self.loadCSVList[x]) == 3):
                    if (len(self.loadCSVtoClear) == 2 or len(self.loadCSVtoClear) == 3):
                        self.Tab3AddItem = QListWidgetItem(self.loadCSVtoClear)
                        self.Tab3AddItem.setTextAlignment(Qt.AlignCenter)
                        self.Tab3AddItem.setSizeHint(QSize(0, 25))
                        self.Tab3input2.addItem(self.Tab3AddItem)

            # self.Vbox2.addWidget(self.Tab3input2)

    def Tab3AddButton1Click(self):
        text, ok = QInputDialog.getText(self, 'Add Dialog', 'Enter text:')
        if (ok):
            self.Tab3name1AddtoList = []
            self.Tab3name1AddtoList = re.compile('[가-힣]+').findall(str(text))
            self.Tab3name1Add = ''
            self.Tab3name1Add = self.Tab3name1Add.join(self.Tab3name1AddtoList)

            if (len(str(text)) == 2 or len(str(text)) == 3):
                if (len(self.Tab3name1Add) == 2 or len(self.Tab3name1Add) == 3):
                    self.Tab3AddItem = QListWidgetItem(self.Tab3name1Add)
                    self.Tab3AddItem.setTextAlignment(Qt.AlignCenter)
                    self.Tab3AddItem.setSizeHint(QSize(0, 25))
                    self.Tab3input1.addItem(self.Tab3AddItem)
                    # self.Vbox1.addWidget(self.Tab3input1)
                    return

    def Tab3RemoveButton1Click(self):
        listItems = self.Tab3input1.selectedItems()
        if not listItems: return
        for item in listItems:
            self.Tab3input1.takeItem(self.Tab3input1.row(item))

    def Tab3AddButton2Click(self):
        text, ok = QInputDialog.getText(self, 'Add Dialog', 'Enter text:')
        if (ok):
            self.Tab3name1AddtoList = []
            self.Tab3name1AddtoList = re.compile('[가-힣]+').findall(str(text))
            self.Tab3name1Add = ''
            self.Tab3name1Add = self.Tab3name1Add.join(self.Tab3name1AddtoList)

            if (len(str(text)) == 2 or len(str(text)) == 3):
                if (len(self.Tab3name1Add) == 2 or len(self.Tab3name1Add) == 3):
                    self.Tab3AddItem = QListWidgetItem(self.Tab3name1Add)
                    self.Tab3AddItem.setTextAlignment(Qt.AlignCenter)
                    self.Tab3AddItem.setSizeHint(QSize(0, 25))
                    self.Tab3input2.addItem(self.Tab3AddItem)
                    # self.Vbox2.addWidget(self.Tab3input2)
                    return

    def Tab3RemoveButton2Click(self):
        listItems = self.Tab3input2.selectedItems()
        if not listItems: return
        for item in listItems:
            self.Tab3input2.takeItem(self.Tab3input2.row(item))

    def Tab3ButtonClick(self):
        self.Tab3input1itemsList = []
        self.Tab3input2itemsList = []
        
        if (self.Tab3input1.count() != 0):
            if (self.Tab3input2.count() != 0):
                    self.Tab3Analyser(self.Tab3input1itemsList, self.Tab3input2itemsList)
                    return

        # 잘못된 입력
        self.inValidMsg()

    def Tab3Analyser(self, Names1, Names2):
        self.Tab3NAME1col = []
        self.Tab3NAME2col = []
        self.Tab3RESULTcol = []

        for f in range(self.Tab3input1.count()):
            Names1.append(self.Tab3input1.item(f))
        for g in range(self.Tab3input2.count()):
            Names2.append(self.Tab3input2.item(g))

        # 모든 아이템을 가져와 글자로 변환
        for j in range(len(Names1)):
            Names1[j] = Names1[j].text()
        for k in range(len(Names2)):
            Names2[k] = Names2[k].text()

         # 2글자 처리
        for l in range(len(Names1)):
            if (len(Names1[l]) == 2):
                Names1[l] = Names1[l] + '○'
        for m in range(len(Names2)):
            if (len(Names2[m]) == 2):
                Names2[m] = Names2[m] + '○'

        self.Tab3NAME1Count = len(Names1)
        self.Tab3NAME2Count = len(Names2)

        for o in range(len(Names1)):
            for p in range(len(Names2)):

                self.Name1toList = []
                self.Name2toList = []

                for a in range(3):
                    self.Name1toList.append(Names1[o][a])
                    self.Name1toList[a] = Hangul.gyeopjamo(Hangul.jamo(self.Name1toList[a]))
                    self.Name1toList[a] = Hangul.convertonumber(''.join(self.Name1toList[a]), self.strokeOrder)
                for b in range(3):
                    self.Name2toList.append(Names2[p][b])
                    self.Name2toList[b] = Hangul.gyeopjamo(Hangul.jamo(self.Name2toList[b]))
                    self.Name2toList[b] = Hangul.convertonumber(''.join(self.Name2toList[b]), self.strokeOrder)
                
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

                self.Tab3NAME1col.append(Names1[o].replace('○',''))
                self.Tab3NAME2col.append(Names2[p].replace('○',''))
                self.Tab3RESULTcol.append(str(self.Name6List[0]) + str(self.Name6List[1]) + '%')

        self.Tab3table = QTableWidget()
        self.Tab3table.setRowCount(len(Names1) * len(Names2))
        self.Tab3table.setColumnCount(3)

        self.Tab3table.setColumnWidth(0, 145)
        self.Tab3table.setColumnWidth(1, 145)
        self.Tab3table.setColumnWidth(2, 145)

        self.header = self.Tab3table.horizontalHeader()       
        self.header.setSectionResizeMode(0, QHeaderView.Stretch)
        self.header.setSectionResizeMode(1, QHeaderView.Stretch)
        self.header.setSectionResizeMode(2, QHeaderView.Stretch)

        for q in range(len(Names1) * len(Names2)):
            self.Tab3table.setItem(q, 0, QTableWidgetItem(self.Tab3NAME1col[q].replace('○','')))
            self.Tab3table.setItem(q, 1, QTableWidgetItem(self.Tab3NAME2col[q].replace('○','')))
            self.Tab3table.setItem(q, 2, QTableWidgetItem(self.Tab3RESULTcol[q]))

        self.Tab3layout.addWidget(self.Tab3table, 3, 0, 1, 4)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)

    fontDB = QFontDatabase()
    # fontDB.addApplicationFont(path.abspath(path.join(path.dirname(__file__), 'fonts/SDGothicNeoM.ttf')))
    # app.setFont(QFont('AppleSDGothicNeoM00', 11))

    fontDB.addApplicationFont(path.abspath(path.join(path.dirname(__file__), 'fonts/NanumSquareOTF_acB.otf')))
    app.setFont(QFont('NanumSquareOTF_ac Bold', 11))

    window = MainWindow()

    # 테마 설정
    # StyleFile = QFile(path.abspath(path.join(path.dirname(__file__), 'styles/MyStyle.css')))
    # StyleFile.open(QFile.ReadOnly | QFile.Text)
    # stream = QTextStream(StyleFile)
    # app.setStyleSheet(stream.readAll())

    # 윈도우 뒤쪽 색 설정
    # palatte = window.palette()
    # palatte.setColor(window.backgroundRole(), Qt.white)
    # window.setPalette(palatte)

    window.show()
    sys.exit(app.exec())