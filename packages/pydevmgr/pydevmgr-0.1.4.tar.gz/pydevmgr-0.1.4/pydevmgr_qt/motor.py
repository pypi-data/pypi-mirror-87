from PyQt5 import QtWidgets, uic
from .io import find_ui
from .generic import record_widget, STYLE, method_caller, method_switcher, RpcError, get_style
from pydevmgr import Motor, Prefixed
from pydevmgr.device import  _name_attr
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

class MotorCtrl(BaseCtrl):
    
    def initUI(self):
        uic.loadUi(find_ui('motor_ctrl_frame.ui'), self)
        
    def update_device(self, data, motor):
        super(MotorCtrl, self).update_device(data, motor)
        
        if self.move_mode.currentIndex()==MOVE_MODE.VELOCITY: # VELOCITY
            self.input_pos_target.setEnabled(False)
        else:
            self.input_pos_target.setEnabled(True)
        
        
        self.pos_actual.setText( "{:.3f}".format(data['pos_actual']) )
        self.pos_error.setText(  "{:.3E}".format(data['pos_error'])  )
        self.pos_target.setText( "{:.3f}".format(data['pos_target']) )
        self.vel_actual.setText( "{:.3f}".format(data['vel_actual']) )
        #self.vel_target.setText( "{:.3f}".format(data['vel_target']) )
        
        self.posname.setText("{}".format(data['pos_name']))
    
    def link_device(self, downloader, motor, altname=None):
        """ Link a device to the widget 
        
        downloader (:class:`pydevmgr.Downloader`): a Downloader object 
        motor (:class:`pydevmgr.Motor`):  Motor device
        altname (string, optional): Alternative printed name for the device
        """
        ## disconnect all the button if they where already connected
        
        super(MotorCtrl, self).link_device(downloader, motor, altname)
        token = self.token # comming from super 
        try:
            self.move.clicked.disconnect()
            self.move_by_posname.currentIndexChanged.disconnect()
        except TypeError:
            pass
        
        # init some field to what the state is 
        
        if motor.is_connected():
            self.input_velocity.setText("%.3f"%motor.cfg.velocity.get())
            self.input_pos_target.setText("%.3f"%motor.stat.pos_actual.get())            
        else:
            # put some dummy values
            self.input_velocity.setText("1.00")
            self.input_pos_target.setText("0.00")            
        
        # update the positoin name menu 
        self.move_by_posname.clear()
        self.move_by_posname.addItems(['']+list(motor.posnames))
        
        self.move_mode.clear()
        self.move_mode.addItems(MOVE_MODE.txt[i] for i in range(MOVE_MODE.count))
        
        # add necessary nodes to the downloader state, substate, status, error_code 
        # are handled  by BaseCtrl.link_device
        stat = motor.stat
        downloader.add_node(token, 
                         stat.pos_actual, stat.pos_error, stat.pos_name, 
                         stat.pos_target, stat.vel_actual,# stat.vel_target,
                        
                        )
        
        def move(idx, pos, vel):
            if idx == MOVE_MODE.ABSOLUTE:
                motor.move_abs(pos, vel)
            elif idx == MOVE_MODE.RELATIVE:
                motor.move_rel(pos, vel)
            elif idx == MOVE_MODE.VELOCITY:
                motor.move_vel(vel)
        
        # Now link the buttons to an action
        move = method_caller(move, 
                                 [self.move_mode.currentIndex, 
                                  self.input_pos_target.text, 
                                  self.input_velocity.text],
                                  self.feedback
                            )
        self.move.clicked.connect(move)
                
        stop = method_caller(motor.stop, [], self.feedback)
        self.stop.clicked.connect(stop)
        
        def move_name(i):
            target_name = self.move_by_posname.currentText()
            if target_name=="":
                return
            self.rpc_feedback.setStyleSheet(get_style(STYLE.NORMAL))
            try:
                motor.move_name(target_name, self.input_velocity.text())
            except (TypeError,ValueError,RpcError) as e: 
                self.rpc_feedback.setText(str(e))
                self.rpc_feedback.setStyleSheet(get_style(STYLE.ERROR))
            self.move_by_posname.setCurrentIndex(0)
            
        self.move_by_posname.currentIndexChanged.connect(move_name)
        

class MotorLine(BaseLine):
        
    def initUI(self):
        uic.loadUi(find_ui('motor_line_frame.ui'), self)
        
    def update_device(self, data, motor):
        super(MotorLine, self).update_device(data, motor)
        self.input_pos_target.update()
        self.input_velocity.update() 
        
        
        pos = data['pos_name'] if data['pos_name'] else "{:.3f}".format(data['pos_actual'])
            
        self.pos_actual.setText( pos )
    
    
    def link_device(self, downloader, motor, altname=None, more_methods=[]):
        """ Link a device to the widget 
        
        downloader (:class:`pydevmgr.Downloader`): a Downloader object 
        motor (:class:`pydevmgr.Motor`):  Motor device
        altname (string, optional): Alternative printed name for the device
        """
        ## disconnect all the button if they where already connected
        
        methods = [
            ("MOVE ABS", motor.move_abs,[self.input_pos_target.text, self.input_velocity.text]),
            ("MOVE REL", motor.move_rel,[self.input_pos_target.text, self.input_velocity.text]), 
            "---"
        ]
        methods += [(name, motor.move_name, [lambda name=name:name,self.input_velocity.text]) for name in motor.posnames]
        methods += list(more_methods)
        super(MotorLine, self).link_device(downloader, motor, altname, more_methods=methods)
        token = self.token # comming from super 
        
        if motor.is_connected():
            self.input_velocity.setText("%.3f"%motor.cfg.velocity.get())
            self.input_pos_target.setText("%.3f"%motor.stat.pos_actual.get())            
        else:
            # put some dummy values
            self.input_velocity.setText("1.00")
            self.input_pos_target.setText("0.00")            
        
        
        stat = motor.stat
        downloader.add_node(token, 
                         stat.pos_actual, stat.pos_name, 
                        )
        




record_widget("ctrl", "Motor", MotorCtrl)
record_widget("line", "Motor", MotorLine)

