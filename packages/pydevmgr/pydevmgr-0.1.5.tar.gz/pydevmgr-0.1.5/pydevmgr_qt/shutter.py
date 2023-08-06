from PyQt5 import QtWidgets, uic
from .io import find_ui
from .generic import record_widget,  method_caller, method_switcher, RpcError
from pydevmgr import Shutter, Prefixed
from .basic import BaseCtrl, BaseLine

class ShutterCtrl(BaseCtrl):
    
    def initUI(self):
        uic.loadUi(find_ui('shutter_ctrl_frame.ui'), self)
        
    def update_device(self, data, shutter):
        super(ShutterCtrl, self).update_device(data, shutter)
        
    
    def link_device(self, downloader, shutter, altname=None):
        """ Link a device to the widget 
        
        downloader (:class:`pydevmgr.Downloader`): a Downloader object 
        shutter (:class:`pydevmgr.Shutter`):  Shutter device
        altname (string, optional): Alternative printed name for the device
        """
        ## disconnect all the button if they where already connected
        
        super(ShutterCtrl, self).link_device(downloader, shutter, altname)
        downloader, token = self.connection # comming from super 
        try:
            self.open.clicked.disconnect()
            self.close.clicked.disconnect()
        except TypeError:
            pass
            
        # add necessary nodes to the downloader state, substate, status, error_code 
        # are handled  by BaseCtrl.link_device
        # stat = shutter.stat
        #downloader.add_node(token)
        
        # Now link the buttons to an action
        open = method_caller(shutter.open, 
                                 [],
                                 self.feedback
                                 )
        self.open.clicked.connect(open)
        close = method_caller(shutter.close, 
                                 [],
                                 self.feedback
                                 )
        self.close.clicked.connect(close)
        
class ShutterLine(BaseLine):

    def initUI(self):
        uic.loadUi(find_ui('shutter_line_frame.ui'), self)
        
    def update_device(self, data, shutter):
        super(ShutterLine, self).update_device(data, shutter)
        # nothing more 
    
    def link_device(self, downloader, shutter, altname=None,more_methods=[]):
        """ Link a device to the widget 
        
        downloader (:class:`pydevmgr.Downloader`): a Downloader object 
        shutter (:class:`pydevmgr.Shutter`):  Shutter device
        altname (string, optional): Alternative printed name for the device
        """
        ## disconnect all the button if they where already connected
        more_methods = [
                        ("OPEN" , shutter.open ,[]), 
                        ("CLOSE", shutter.close,[])
                        ]+list(more_methods)
        super(ShutterLine, self).link_device(downloader, shutter, altname, more_methods = more_methods)
        
        token = self.token # comming from super 
        
                

record_widget("ctrl", "Shutter", ShutterCtrl)
record_widget("line", "Shutter", ShutterLine)