from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
from pydevmgr import Motor, Downloader
from pydevmgr_qt.motor import MotorCtrl, BaseCtrl

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
        
motor1, motor2 = None, None
def main():
    global motor1, motor2
    #motor = Motor.from_config('fcf/devmgr/server/m403.yml', 'm403')
    motor1 = Motor.from_config('fcf/devmgr/server/motor1.yml', 'motor1')
    motor2 = Motor.from_config('fcf/devmgr/server/motor2.yml', 'motor2')
    motor1.connect(); motor1.configure()
    motor2.connect(); motor2.configure()
    #motor.configure() # configure true OPC-UA the device
    downloader = Downloader()
    
    app = QApplication(sys.argv)
    win = QtWidgets.QWidget()
    layout =  QtWidgets.QVBoxLayout(win)

    motFrame1 = MotorCtrl(win)
    motFrame1.link_device(downloader, motor1)
    motFrame1.link_failure()
    
    motFrame2 = BaseCtrl(win)
    motFrame2.link_device(downloader, motor2)
    motFrame2.link_failure()
    
    
    connect = QtWidgets.QPushButton("Connect")
    disconnect = QtWidgets.QPushButton("Disconnect")
    connect.clicked.connect( motor1.connect )
    disconnect.clicked.connect( motor1.disconnect )
    
    
    layout.addWidget(motFrame1)
    layout.addWidget(motFrame2)
    
    layout.addWidget(connect)
    layout.addWidget(disconnect)
    
    
    #### test ####
    # test1 = Test(win)
    # test2 = Test2(win)
    #
    # layout.addWidget(test1)
    # layout.addWidget(test2)


    #win.setLayout( layout )
    win.show()
    timer = QtCore.QTimer()
    timer.timeout.connect(downloader.download)
    timer.start(100)
    sys.exit(app.exec_())


if __name__ == '__main__':
    try:
        main()
    finally:
        motor1.disconnect()
        motor2.disconnect()
