import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

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

class MainWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        self.mare = Button('Start')
        self.quto = Button('Next')

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.mare)
        self.layout.addWidget(self.quto)
        self.setLayout(self.layout)

        hover_tracker = HoverTracker(self.mare)
        hover_tracker.positionChanged.connect(self.on_position_changed)
        hover_tracker = HoverTracker(self.quto)
        hover_tracker.positionChanged.connect(self.on_position_changed)

    @pyqtSlot(QPoint)
    def on_position_changed(self, pt):
        global point
        point = pt
        print(pt)

class Button(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.r = 0
        self.timer = QTimer(interval=5, timeout=self.set_radius)
        self.clicked.connect(self.timer.start)
        self.setToolTip('This is a <b>QPushButton</b> widget')

    def set_radius(self):
        if self.r == 0:
            self.fixedPoint = point
        if self.r < self.width() * 1.1:
            self.r += self.width() / 100
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
            qp.drawEllipse(self.fixedPoint, self.r, self.r)
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWidget()
    window.setStyleSheet('''
    QPushButton {
        font-size: 15px;
        background-color: #09e;
        border: none;
        padding: 10px
    }''')
    window.show()
    sys.exit(app.exec_())