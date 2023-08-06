from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
from pydevmgr import Motor, Downloader, Manager
from pydevmgr_qt.motor import MotorCtrl
from pydevmgr_qt.manager import ManagerDevices

class Test(QtWidgets.QWidget):
    def __init__(self, *args):
        super(Test, self).__init__(*args)
        self.label = QtWidgets.QLabel(self)
        self.label.setText('Hello')
class Test2(QtWidgets.QWidget):
    def __init__(self, *args):
        super(Test2, self).__init__(*args)
        self.label = QtWidgets.QLabel(self)
        self.label.setText('      ----Hello')
        
mgr = None

live = True
def main():
    global mgr
    
    #mgr = Manager.from_config('fcf/devmgr/server/cfgM403.yml', 'fcs')
    #mgr = Manager.from_config('fcf/devmgr/server/tins.yml', 'fcs', extra_file="fcf/devmgr/server/tins_pydevmgr.yml")
    mgr = Manager.from_config('fcf/devmgr/server/tins.yml', 'fcs')
    
    
    if live:
        mgr.connect_all()
        mgr.configure_all() # configure true OPC-UA the devices
    
    downloader = Downloader()


    app = QApplication(sys.argv)
    #app.setStyleSheet(style)
    #app.setStyle("Fusion")
    #win = ManagerMainWindow()
    win = ManagerDevices()
    win.link_device(downloader, mgr, widget_type='ctrl')
    
    # win = QtWidgets.QWidget()
    # layout =  QtWidgets.QVBoxLayout(win)
    #
    # managerWidget = ManagerCtrl(win)
    # managerWidget.link_device(downloader, mgr)
    #
    # layout.addWidget(managerWidget)
    #win.setLayout( layout )
    win.show()
    timer = QtCore.QTimer()
    timer.timeout.connect(downloader.download)
    if live:
        timer.start(200)
    sys.exit(app.exec_())


if __name__ == '__main__':
    try:
        main()
    finally:
        if live and mgr: 
            mgr.disconnect_all()
