import os
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from Checker_GUI import iconfilename

class Listener(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Listener')
        self.setWindowIcon(QIcon(iconfilename))
        self.resize(400, 550)
        self.geometryInfo = self.frameGeometry()
        self.centerpoint = QDesktopWidget().availableGeometry().center()
        self.geometryInfo.moveCenter(self.centerpoint)
        self.move(self.geometryInfo.topLeft())
        self.show()

        self.layout = QVBoxLayout()
        
        self.consoleBox = QTextEdit()
        self.executeButton = QPushButton('Run')
        self.executeButton.clicked.connect(self.execute)

        self.layout.addWidget(self.consoleBox)
        self.layout.addWidget(self.executeButton)
        self.setLayout(self.layout)

    def execute(self):
        t = Thread1(self)
        t.start()

class Thread1(QThread):
    def __init__(self, parent):
        super().__init__(parent)
    def run(self):
        if os.path.isfile('Checker_GUI.py'):
            os.system('Checker_GUI.py')
        elif os.path.isfile('Checker_GUI.exe'):
            os.system('Checker_GUI.exe')
        fi = ''
        sys.stdout = fi
        print(fi)


if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = Listener()
   sys.exit(app.exec_())