from PyQt5 import QtWidgets, uic
from .io import find_ui
from .generic import record_widget, method_caller, method_switcher, RpcError
from pydevmgr import Lamp, Prefixed
from .basic import BaseCtrl, BaseLine

class LampCtrl(BaseCtrl):
    
    def initUI(self):
        uic.loadUi(find_ui('lamp_ctrl_frame.ui'), self)
        
    def update_device(self, data, lamp):
        super(LampCtrl, self).update_device(data, lamp)
        self.input_intensity.update()
        self.input_time.update() 
        
        self.time_left.setText( "{:.0f}".format(data['time_left']) )
        self.intensity.setText( "{:.1f}".format(data['intensity']) )
        
    def link_device(self, downloader, lamp, altname=None):
        """ Link a device to the widget 
        
        downloader (:class:`pydevmgr.Downloader`): a Downloader object 
        lamp (:class:`pydevmgr.Lamp`):  Lamp device
        altname (string, optional): Alternative printed name for the device
        """
        ## disconnect all the button if they where already connected
        
        super(LampCtrl, self).link_device(downloader, lamp, altname)
        downloader, token = self.connection # comming from super 
        try:
            self.on.clicked.disconnect()
            self.off.clicked.disconnect()
        except TypeError:
            pass
        
        
        # put some start values, a pity that there is no way to get the last 
        # entered value
        self.input_intensity.setText("1")
        self.input_time.setText("10")            
        
        # add necessary nodes to the downloader state, substate, status, error_code 
        # are handled  by BaseCtrl.link_device
        stat = lamp.stat
        downloader.add_node(token, 
                         stat.time_left, stat.intensity
                        
                        )
        
        # Now link the buttons to an action
        on = method_caller(lamp.switch_on, 
                                 [self.input_intensity.text, self.input_time.text],
                                 self.feedback
                                 )
        
        self.on.clicked.connect(on)
        
        
        off = method_caller(lamp.switch_off, [], self.feedback)
        self.off.clicked.connect(off)


class LampLine(BaseLine):    
    def initUI(self):
        uic.loadUi(find_ui('lamp_line_frame.ui'), self)
        self.check.hide() # hide check box by default it is show by the manager panel

    def update_device(self, data, lamp):
        super(LampLine, self).update_device(data, lamp)
        self.input_intensity.update()
        self.input_time.update() 
        
        self.time_left.setText( "{:.0f}".format(data['time_left']) )
        
    def link_device(self, downloader, lamp, altname=None, more_methods=[]):
        """ Link a device to the widget 
        
        downloader (:class:`pydevmgr.Downloader`): a Downloader object 
        lamp (:class:`pydevmgr.Lamp`):  Lamp device
        altname (string, optional): Alternative printed name for the device
        """
        ## disconnect all the button if they where already connected
        
        more_methods = [
                        ("ON",  lamp.switch_on, [self.input_intensity.text, self.input_time.text]),
                        ("OFF", lamp.switch_off, [])
                        ]+list(more_methods)
        super(LampLine, self).link_device(downloader, lamp, altname, 
                                          more_methods=more_methods)
        token = self.token # comming from super 
        
        # put some start values, a pity that there is no way to get the last 
        # entered value
        self.input_intensity.setText("1")
        self.input_time.setText("10")            
        
        # add necessary nodes to the downloader state, substate, status, error_code 
        # are handled  by BaseCtrl.link_device
        stat = lamp.stat
        downloader.add_node(token, 
                         stat.time_left, stat.intensity
                        
                        )


record_widget("ctrl", "Lamp", LampCtrl)
record_widget("line", "Lamp", LampLine)