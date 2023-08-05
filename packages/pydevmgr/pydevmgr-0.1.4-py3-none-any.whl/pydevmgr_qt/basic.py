from pydevmgr import Device
from .io import find_ui
from .generic import STYLE, method_switcher, record_widget, method_setup, get_style
from PyQt5 import QtWidgets, uic


class _Shared:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUI()
        self.connection  = None
        self._did_failed = False
        self.device_key = ""
    
    def connect_downloader(self, downloader):
        ## create a new connection 
        token = downloader.new_connection()
        self.connection = (downloader, token)
        return token
    
    def disconnect_downloader(self):
        if self.connection:
            previous_downloader, token = self.connection 
            previous_downloader.disconnect(token)
            
    def __del__(self):
        self.disconnect_downloader()
        
    @property
    def token(self):
        if self.connection is None:
            return None
        _, token = self.connection
        return token            

class BaseCtrl(QtWidgets.QFrame, _Shared):
            
    def initUI(self):
        uic.loadUi(find_ui('base_ctrl_frame.ui'), self)
        
        
    def feedback(self, er, txt):
        self.rpc_feedback.setText(txt)
        if er:
            self.rpc_feedback.setStyleSheet(get_style(STYLE.ERROR))
        else:
            self.rpc_feedback.setStyleSheet(get_style(STYLE.NORMAL))
        
    def update_failure(self, er):
        """ executed when the Downloader failed. Must be connected """
        style = get_style(STYLE.UNKNOWN)
        self.setEnabled(False)
        for wgt in [self.state, self.substate, self.error_txt]:
            wgt.setStyleSheet(style)
        self._did_failed = True    
    
    def link_failure(self):
        """ link a failure callback to the current connection """
        ## diconnect the downloader 
        if self.connection is None:
            raise ValueError("cannot link failure, widget is not connected")
        downloader, token = self.connection
        downloader.add_failure_callback(token, self.update_failure)
    
    
    def update_device(self, data, device):
        if self._did_failed:
            self.setEnabled(True)
            style = get_style(STYLE.NORMAL)
            for wgt in [self.state, self.substate, self.error_txt]:
                wgt.setStyleSheet(style)
            self._did_failed = False
        
        self.rpc_feedback.update()
        state = data['state']
        self.state.setText("{}: {}".format(state, data['state_txt']))
        self.state.setStyleSheet(get_style(data['state_group']))
        
        substate = data['substate']
        self.substate.setText("{}: {}".format(substate, data['substate_txt']))
        self.substate.setStyleSheet(get_style(data['substate_group']))
        
        erc = data['error_code']
        self.error_txt.setText("{}: {}".format(erc, data['error_txt']))
        self.error_txt.setStyleSheet( get_style(STYLE.ERROR) if erc else get_style(STYLE.OK) )
    
     
        
    def link_device(self, downloader, device, altname=None, more_methods=[]):
        """ Link a device to the widget 
        
        downloader (:class:`pydevmgr.Downloader`): a Downloader object 
        device (:class:`pydevmgr.Motor`):  device to be linked
        altname (string, optional): Alternative printed name for the device
        """
        try:
            self.state_action.currentIndexChanged.disconnect()
        except TypeError:
            pass
        
        
        ## disconnect all the button if they where already connected
        ## diconnect a previous connection
        self.disconnect_downloader()
        token = self.connect_downloader(downloader) 
        self.device_key = device.key 
        
        stat_methods = [
           ("",       None,          []), 
           ("INIT",   device.init,   []), 
           ("ENABLE", device.enable, []),
           ("DISABLE",device.disable,[]),
           ("RESET",  device.reset,  []) 
        ]+list(more_methods)
        
        # action menu 
        self.state_action.clear()
        # Add items to combo and remove string "---" separator from stat_methods
        stat_methods = method_setup(self.state_action, stat_methods)
                
        self.name.setText( device.key if altname is None else altname )
        
        stat = device.stat
        downloader.add_node(token, 
                         stat.state, stat.state_txt, stat.state_group, 
                         stat.substate, stat.substate_txt, stat.substate_group,  
                         stat.error_code, stat.error_txt,                                      
                        )
        # Add the callback to the downloader            
        def update(data):
            return self.update_device(downloader.get_data(device.key), device)                        
        downloader.add_callback(token, update)
        
        state_action = method_switcher(stat_methods, self.feedback, 
                                       lambda : self.state_action.setCurrentIndex(0)
                                       )
        self.state_action.currentIndexChanged.connect(state_action)



class BaseLine(QtWidgets.QFrame, _Shared):
    
    
    
        
    def initUI(self):
        uic.loadUi(find_ui('base_line_frame.ui'), self)
    
    def feedback(self, er, txt):
        if er:
            #self.state_action.setStyleSheet("border-color: red;")
            self.state_action.setItemText(0, '!ERROR')
        else:
            self.state_action.setItemText(0, '')
            #self.state_action.setStyleSheet(STYLE.NORMAL)
    
    def update_failure(self, er):
        """ executed when the Downloader failed. Must be connected """
        style = get_style(STYLE.UNKNOWN)
        self.setEnabled(False)
        for wgt in [self.substate]:
            wgt.setStyleSheet(style)
        self._did_failed = True    
    
    def link_failure(self):
        """ link a failure callback to the current connection """
        ## diconnect the downloader 
        if self.connection is None:
            raise ValueError("cannot link failure, widget is not connected")
        downloader, token = self.connection
        downloader.add_failure_callback(token, self.update_failure)
    
    def update_device(self, data, device):
        if self._did_failed:
            self.setEnabled(True)
            style = get_style(STYLE.NORMAL)
            for wgt in [self.substate]:
                wgt.setStyleSheet(style)
            self._did_failed = False
        
        substate = data['substate']
        self.substate.setText("{}".format(data['substate_txt']))
        self.substate.setStyleSheet(get_style(data['substate_group']))
    
    def link_device(self, downloader, device, altname=None, more_methods=[]):
        """ Link a device to the widget 
        
        downloader (:class:`pydevmgr.Downloader`): a Downloader object 
        device (:class:`pydevmgr.Motor`):  device to be linked
        altname (string, optional): Alternative printed name for the device
        """
        try:
            self.state_action.currentIndexChanged.disconnect()
        except TypeError:
            pass
        
        ## disconnect all the button if they where already connected
        ## diconnect a previous connection
        self.disconnect_downloader()
        token = self.connect_downloader(downloader) 
        self.device_key = device.key 
        
        
        stat_methods = [
           ("",       None,          []), 
           ("INIT",   device.init,   []), 
           ("ENABLE", device.enable, []),
           ("DISABLE",device.disable,[]),
           ("RESET",  device.reset,  []) 
        ]+list(more_methods)
        
        # action menu 
        self.state_action.clear()
        # Add items to combo and remove string "---" separator from stat_methods
        stat_methods = method_setup(self.state_action, stat_methods)
        
        self.name.setText( device.key if altname is None else altname )
        
        stat = device.stat
        downloader.add_node(token, 
                         stat.substate, stat.substate_txt, stat.substate_group                                    
                        )
        # Add the callback to the downloader            
        def update(data):
            return self.update_device(downloader.get_data(device.key), device)                        
        downloader.add_callback(token, update)
        
        state_action = method_switcher(stat_methods, self.feedback, 
                                       lambda : self.state_action.setCurrentIndex(0)
                                       )
        self.state_action.currentIndexChanged.connect(state_action)
        



record_widget("ctrl", "Device", BaseCtrl)
record_widget("line", "Device", BaseLine)
  