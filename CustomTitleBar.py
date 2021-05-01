import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class Button(QPushButton):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.r = 0
        self.timer = QTimer(interval=25, timeout=self.set_radius)
        self.clicked.connect(self.timer.start)

    def set_radius(self):
        if self.r < self.width() / 2:
            self.r += self.width() / 20
        else:
            self.timer.stop()
            self.r = 0
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.r:
            qp = QPainter(self)
            qp.setBrush(QColor(255, 255, 255, 127))
            qp.setPen(Qt.NoPen)
            qp.drawEllipse(self.rect().center(), self.r, self.r)
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QWidget()
    layout = QVBoxLayout(window)
    layout.addWidget(Button('Start'))
    window.setStyleSheet('''
    QPushButton {
        color: #fff;
        background-color: #09e;
        padding: 20px;
        font-size: 24pt;
        border: none;
    }
    QPushButton:pressed {
        color: #ddd;
    }''')
    window.show()
    sys.exit(app.exec_())