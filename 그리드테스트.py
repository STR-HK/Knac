import sys
from PyQt5 import QtCore, QtGui, QtWidgets

class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        
        self.qtabwidget = QtWidgets.QTabWidget(self) 
        
        widget  = QtWidgets.QPlainTextEdit("QPlainTextEdit 1")
        label   = 'Tab &1'
        widget2 = QtWidgets.QPlainTextEdit("QPlainTextEdit 2")
        
        tab_index1 = self.qtabwidget.addTab(widget, label)
        
        tab_index2 = self.qtabwidget.addTab(widget2, 'Tab &2')
        self.qtabwidget.setTabIcon(tab_index2, QtGui.QIcon('im.png'))                # <---  
        self.qtabwidget.setIconSize(QtCore.QSize(32, 32)) 
        
        self.qtabwidget.addTab(
                QtWidgets.QLabel("QLabel Tab &3", alignment=QtCore.Qt.AlignCenter), 
                QtGui.QIcon('Ok.png'),                                               # < ---
                'Tab &3')
        
        self.qtabwidget.addTab(None, "No Widget")
        
        self.qtabwidget.setTabsClosable(True)  
        self.qtabwidget.tabCloseRequested.connect(self.qtabwidget_tabcloserequested)
        self.qtabwidget.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.qtabwidget.setTabPosition(QtWidgets.QTabWidget.East)  
        self.qtabwidget.setTabEnabled(0, False)         # disable tab
        self.qtabwidget.setTabEnabled(1, True)          # enable tab
        self.qtabwidget.currentChanged.connect(self.qtabwidget_currentchanged)
       
        self.setCentralWidget(self.qtabwidget)

    @QtCore.pyqtSlot(int)
    def qtabwidget_tabcloserequested(self, index):
        # gets the widget
        widget = self.qtabwidget.widget(index)
        # if the widget exists
        if widget:
            widget.deleteLater()
        # removes the tab of the QTabWidget
        self.qtabwidget.removeTab(index)
        
    @QtCore.pyqtSlot(int)
    def qtabwidget_currentchanged(self, index):
        print(f"\n New index of current page: {index}")


if __name__ == '__main__':
    application = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.setWindowTitle('QTabWidget')
    window.resize(400, 400)
    window.show()
    sys.exit(application.exec_())        