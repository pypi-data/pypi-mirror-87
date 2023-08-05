from PyQt5 import QtWidgets, uic
from .io import find_ui
from .generic import record_widget, method_caller, method_switcher, RpcError
from pydevmgr import Adc, Prefixed
from .basic import BaseCtrl, BaseLine


class MOVE_MODE:
    ABSOLUTE = 0
    RELATIVE = 1
    VELOCITY = 2
    txt = {
       ABSOLUTE : "ABSOLUTE", 
       RELATIVE : "RELATIVE", 
       VELOCITY : "VELOCITY"
    }
    count = 3

class AXES:
    BOTH = 0
    AXIS1 = 1
    AXIS2 = 2
    txt = {
        BOTH  : 'BOTH AXES', 
        AXIS1 : 'AXIS 1',
        AXIS2 : 'AXIS 2'
    }
    count = 3


class AdcCtrl(BaseCtrl):
    
    def initUI(self):
        uic.loadUi(find_ui('adc_ctrl_frame.ui'), self)
        
    def update_device(self, data, adc):
        super(AdcCtrl, self).update_device(data, adc)
        #self.input_pos_target1.update()
        #self.input_pos_target2.update()
        #self.input_velocity.update() 
        
        if self.move_mode.currentIndex()==MOVE_MODE.VELOCITY: # VELOCITY
            self.input_pos_target.setEnabled(False)
        else:
            self.input_pos_target.setEnabled(True)
        
        
        self.motor1_pos_actual.setText( "{:.3f}".format(data['motor1.pos_actual']) )
        self.motor2_pos_actual.setText( "{:.3f}".format(data['motor2.pos_actual']) )
        self.motor1_pos_error.setText( "{:.3E}".format(data['motor1.pos_error']) )
        self.motor2_pos_error.setText( "{:.3E}".format(data['motor2.pos_error']) )
        
        self.motor1_pos_target.setText( "{:.3f}".format(data['motor1.pos_target']) )
        self.motor2_pos_target.setText( "{:.3f}".format(data['motor2.pos_target']) )
        self.motor1_vel_actual.setText( "{:.3f}".format(data['motor1.vel_actual']) )
        self.motor2_vel_actual.setText( "{:.3f}".format(data['motor2.vel_actual']) )
        
        self.track_mode_txt.setText( "{}".format(data['track_mode_txt']) )
        
    def link_device(self, downloader, adc, altname=None):
        """ Link a device to the widget 
        
        downloader (:class:`pydevmgr.Downloader`): a Downloader object 
        adc (:class:`pydevmgr.Adc`):  Adc device
        altname (string, optional): Alternative printed name for the device
        """
        ## disconnect all the button if they where already connected
        
        super(AdcCtrl, self).link_device(downloader, adc, altname)
        token = self.token # comming from super 
        try:
            self.move.clicked.disconnect()
            self.start_track.disconnect()
            self.stop_track.disconnect()
        except TypeError:
            pass
        
        # init some field to what the state is 
        
        if adc.is_connected():
            self.input_velocity.setText("%.3f"%adc.motor1.cfg.velocity.get())
            self.input_pos_target.setText("%.3f"%adc.motor1.stat.pos_actual.get())   
        else:
            # put some dummy values
            self.input_velocity.setText("1.00")
            self.input_pos_target.setText("0.00")   
        self.input_angle.setText("0.0")
        
        self.input_axis.clear()
        self.input_axis.addItems(AXES.txt[i] for i in range(AXES.count))    
        
        self.move_mode.clear()
        self.move_mode.addItems(MOVE_MODE.txt[i] for i in range(MOVE_MODE.count))
        
        # add necessary nodes to the downloader state, substate, status, error_code 
        # are handled  by BaseCtrl.link_device
        
        downloader.add_node(token, 
                         adc.stat.track_mode_txt, 
                         adc.motor1.stat.pos_actual, adc.motor1.stat.pos_error, 
                         adc.motor1.stat.pos_target, adc.motor1.stat.vel_actual,# stat.vel_target,
                         adc.motor2.stat.pos_actual, adc.motor2.stat.pos_error, 
                         adc.motor2.stat.pos_target, adc.motor2.stat.vel_actual,# stat.vel_target,
                        )
        
        
        def move(idx, axis, pos, vel):
            if idx == MOVE_MODE.ABSOLUTE:
                adc.move_abs(axis, pos, vel)
            elif idx == MOVE_MODE.RELATIVE:
                adc.move_rel(axis, pos, vel)
            elif idx == MOVE_MODE.VELOCITY:
                adc.move_vel(axis, vel)
            
        # Now link the buttons to an action
        move = method_caller(move, 
                            [self.move_mode.currentIndex, 
                             self.input_axis.currentIndex,
                             self.input_pos_target.text, 
                             self.input_velocity.text
                             ],
                             self.feedback
                            )
        self.move.clicked.connect(move)
        
        stop = method_caller(adc.stop, [], self.feedback)
        self.stop.clicked.connect(stop)
        
        
        start_track = method_caller(adc.start_track, [self.input_angle.text], self.feedback)
        self.start_track.clicked.connect(start_track)
        
        stop_track = method_caller(adc.stop_track, [], self.feedback)
        self.stop_track.clicked.connect(stop_track)
        
        move_angle = method_caller(adc.move_angle,
                                   [self.input_angle.text], 
                                    self.feedback
                                   )
        self.move_angle.clicked.connect(move_angle)

class AdcLine(BaseLine):
    
    def initUI(self):
        uic.loadUi(find_ui('adc_line_frame.ui'), self)
        
    def update_device(self, data, adc):
        super(AdcLine, self).update_device(data, adc)
        
        
        self.motor1_pos_actual.setText( "{:.3f}".format(data['motor1.pos_actual']) )
        self.motor2_pos_actual.setText( "{:.3f}".format(data['motor2.pos_actual']) )
        
        self.track_mode_txt.setText( "{}".format(data['track_mode_txt']) )
    
    
    def link_device(self, downloader, adc, altname=None, more_methods=[]):
        """ Link a device to the widget 
        
        downloader (:class:`pydevmgr.Downloader`): a Downloader object 
        adc (:class:`pydevmgr.Adc`):  Adc device
        altname (string, optional): Alternative printed name for the device
        """
        ## disconnect all the button if they where already connected
        
        methods = [
             "---", # is a separator and is not counted as item 
            ("MOVE ANGLE", adc.move_angle, [self.input_angle.text]),
            ("START TRACK", adc.start_track,[self.input_angle.text]), 
            ("STOP TRACK", adc.stop_track, [] ), 
        ]+ list(more_methods)
                        
        super(AdcLine, self).link_device(downloader, adc, altname, more_methods=methods)
        token = self.token # comming from super 
                
        self.input_angle.setText("0.00")            
        
        downloader.add_node(token, 
                         adc.motor1.stat.pos_actual, adc.motor2.stat.pos_actual, 
                         adc.stat.track_mode_txt
                        )
        

record_widget("ctrl", "Adc", AdcCtrl)
record_widget("line", "Adc", AdcLine)

