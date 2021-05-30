import sys
from tkinter import Y
from PyQt5.QtWidgets import QMainWindow,QPushButton, QApplication
from PyQt5.QtCore import QSize, Qt, QLine, QPoint
from PyQt5.QtGui import *

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(300, 300))
        self.setMouseTracking(True)

        pybutton = QPushButton('button', self)
        pybutton.clicked.connect(self.draw_line)
        pybutton.resize(100,100)
        pybutton.move(100, 100) 
        self.line = QLine()
    
    def mouseMoveEvent(self, event):
        print('Mouse coords: ( %d : %d )' % (event.x(), event.y()))
        print(self.mapFromGlobal(QCursor.pos()))

        global x, y
        x, y = event.x(), event.y()

    def mousePressEvent(self, QMouseEvent):
        print(QMouseEvent.pos())

    def draw_line(self):
        button = self.sender()
        self.line = QLine(QPoint(), button.pos())
        self.update()

    def paintEvent(self, event):
        
        QMainWindow.paintEvent(self, event)
        if not self.line.isNull():
            painter = QPainter(self)
            pen = QPen(Qt.red, 3)
            painter.setPen(pen)
            painter.drawLine(self.line)
            painter.drawEllipse(x, y, 10, 10)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())