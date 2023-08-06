#! /usr/bin/env python
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
from pydevmgr import Downloader, open_manager
from pydevmgr_qt.manager import ManagerDevices


usage = "pydevmgr_gui relative/path/to/manger.yml"

# if len(sys.argv)!=2:
#     print(usage)
#     sys.exit(1)

mgr = None
def app_main():
    global mgr
    
    mgr = open_manager(sys.argv[1], 'fcs')
    
    mgr.connect_all()
    mgr.configure_all() # configure through OPC-UA all the devices
    
    downloader = Downloader()


    app = QApplication(sys.argv)
    #app.setStyleSheet(style)
    #app.setStyle("Fusion")
    #win = ManagerMainWindow()
    win = ManagerDevices()
    win.link_device(downloader, mgr)
    win.link_failure()
    
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
    
    timer.start(200)
    return app.exec_()

def main():
    global mgr
    exit_code = 1
    try:
        exit_code = app_main()
    except Exception as e:
        if mgr:        
            mgr.disconnect_all()
        raise e
    else:
        mgr.disconnect_all()
        sys.exit(exit_code)

if __name__ == '__main__':
    main()

    # exit_code = 1
    # try:
    #     exit_code = main()
    # except Exception as e:
    #     if mgr:        
    #         mgr.disconnect_all()
    #     raise e
    # else:
    #     mgr.disconnect_all()
    #     sys.exit(exit_code)
    # finally:
    #     if mgr:        
    #         mgr.disconnect_all()
    #         sys.exit(exit_code)
    # 