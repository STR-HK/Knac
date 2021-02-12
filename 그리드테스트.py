import sys
from PyQt5.QtWidgets import (QWidget, QGridLayout,QPushButton, QApplication)

class basicWindow(QWidget):
    def __init__(self):
        super().__init__()
        menu = QM
        self.setLayout(grid_layout)

        button = QPushButton('1-3')
        grid_layout.addWidget(button, 0, 0, 1, 2)

        button = QPushButton('1-3')
        grid_layout.addWidget(button, 0, 2, 1, 1)

        button = QPushButton('1-3')
        grid_layout.addWidget(button, 0, 3, 1, 2)
        
        button = QPushButton('4, 7')
        grid_layout.addWidget(button, 1, 0, -1, 1)
        
        self.setWindowTitle('Basic Grid Layout')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    windowExample = basicWindow()
    windowExample.show()
    sys.exit(app.exec_())
    