from PyQt5.QtWidgets import *
import requests

class Porter(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Porter')

        self.setGeometry(0, 0, 200, 110)
        self.geometryInfo = self.frameGeometry()
        self.centerpoint = QDesktopWidget().availableGeometry().center()
        self.geometryInfo.moveCenter(self.centerpoint)
        self.move(self.geometryInfo.topLeft())

        self.layout = QVBoxLayout()

        self.ipAdress = QLineEdit()
        self.ipAdress.setPlaceholderText('IP Adress')
        self.port = QLineEdit()
        self.port.setPlaceholderText('Port Number')
        self.check = QPushButton('Check')
        self.check.clicked.connect(self.anal)
        self.viewer = QLabel()

        self.layout.addWidget(self.ipAdress)
        self.layout.addWidget(self.port)
        self.layout.addWidget(self.check)
        self.layout.addWidget(self.viewer)

        self.setLayout(self.layout)

    def anal(self):
        data = {'remoteAddress':self.ipAdress.text(), 'portNumber':self.port.text()}
        r = requests.post('https://ports.yougetsignal.com/check-port.php', params=data)
        if 'close' in str(r.content):
            self.viewer.setText('Closed')
        elif 'open' in str(r.content):
            self.viewer.setText('Opened')

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = Porter()
    window.show()
    sys.exit(app.exec())