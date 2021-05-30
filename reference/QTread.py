from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import time
import sys


#쓰레드 선언
class Thread1(QThread):
    #parent = MainWidget을 상속 받음.
    def __init__(self, parent):
        super().__init__(parent)
    def run(self):
        for i in range(10):
            print("Thread :",i)
            time.sleep(1)


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        thread_start = QPushButton("시 작!")
        thread_start.clicked.connect(self.increaseNumber)

        vbox = QVBoxLayout()
        vbox.addWidget(thread_start)

        self.resize(200,200)
        self.setLayout(vbox)

    def increaseNumber(self):
        x = Thread1(self)
        x.start()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MainWidget()
    widget.show()
    sys.exit(app.exec_())