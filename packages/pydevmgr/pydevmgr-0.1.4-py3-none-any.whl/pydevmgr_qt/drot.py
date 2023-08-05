from PyQt5 import QtWidgets, uic
from .io import find_ui
from .generic import record_widget, method_caller, method_switcher, RpcError
from pydevmgr import Drot, Prefixed, download
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

class TRACK_MODE:
    SKY = 2
    ELEV = 3
    USER = 4
    txt = {
        SKY  : 'SKY', 
        ELEV : 'ELEV',
        USER : 'USER'
    }
    ordered = [SKY, ELEV, USER]
    count = 3


class DrotCtrl(BaseCtrl):
    
    def initUI(self):
        uic.loadUi(find_ui('drot_ctrl_frame.ui'), self)
        
    def update_device(self, data, drot):
        super(DrotCtrl, self).update_device(data, drot)
        #self.input_pos_target1.update()
        #self.input_pos_target2.update()
        #self.input_velocity.update() 
        
        if self.move_mode.currentIndex()==MOVE_MODE.VELOCITY: # VELOCITY
            self.input_pos_target.setEnabled(False)
        else:
            self.input_pos_target.setEnabled(True)
        
        
        self.pos_actual.setText( "{:.3f}".format(data['pos_actual']) )
        self.pos_error.setText( "{:.3E}".format(data['pos_error']) )
        
        self.pos_target.setText( "{:.3f}".format(data['pos_target']) )
        self.vel_actual.setText( "{:.3f}".format(data['vel_actual']) )
        
        self.angle_on_sky.setText( "{:.2f}".format(data['angle_on_sky']) )
        
        self.track_mode_txt.setText( "{}".format(data['track_mode_txt']) )
        
    def link_device(self, downloader, drot, altname=None):
        """ Link a device to the widget 
        
        downloader (:class:`pydevmgr.Downloader`): a Downloader object 
        drot (:class:`pydevmgr.Drot`):  Drot device
        altname (string, optional): Alternative printed name for the device
        """
        ## disconnect all the button if they where already connected
        
        super(DrotCtrl, self).link_device(downloader, drot, altname)
        token = self.token # comming from super 
        try:
            self.move.clicked.disconnect()
            self.start_track.disconnect()
            self.stop_track.disconnect()
        except TypeError:
            pass
        
        
        # init some field to what the state is 
        
        if drot.is_connected():
            v,p,a = download([drot.cfg.velocity, drot.stat.pos_actual, drot.stat.angle_on_sky])
            self.input_velocity.setText("%.3f"%v)
            self.input_pos_target.setText("%.3f"%p) 
            self.input_angle.setText("%.3f"%a)
  
        else:
            # put some dummy values
            self.input_velocity.setText("1.00")
            self.input_pos_target.setText("0.00")   
            self.input_angle.setText("0.0")
        
        self.track_mode.clear()
        self.track_mode.addItems(TRACK_MODE.txt[M] for M in TRACK_MODE.ordered)    
        
        self.move_mode.clear()
        self.move_mode.addItems(MOVE_MODE.txt[i] for i in range(MOVE_MODE.count))
        
        # add necessary nodes to the downloader state, substate, status, error_code 
        # are handled  by BaseCtrl.link_device
        
        downloader.add_node(token, 
                         drot.stat.track_mode_txt, 
                         drot.stat.pos_actual, drot.stat.pos_error, 
                         drot.stat.pos_target, drot.stat.vel_actual,# stat.vel_target,
                         drot.stat.angle_on_sky
                        )
        
        
        def move(idx,  pos, vel):
            if idx == MOVE_MODE.ABSOLUTE:
                drot.move_abs( pos, vel)
            elif idx == MOVE_MODE.RELATIVE:
                drot.move_rel( pos, vel)
            elif idx == MOVE_MODE.VELOCITY:
                drot.move_vel( vel)
            
        # Now link the buttons to an action
        move = method_caller(move, 
                            [self.move_mode.currentIndex, 
                             self.input_pos_target.text, 
                             self.input_velocity.text
                             ],
                             self.feedback
                            )
        self.move.clicked.connect(move)
        
        stop = method_caller(drot.stop, [], self.feedback)
        self.stop.clicked.connect(stop)
        
        move_angle = method_caller(drot.move_angle, [self.input_angle.text], self.feedback)
        self.move_angle.clicked.connect(move_angle)
        
        def track_mode():
            return TRACK_MODE.ordered[self.track_mode.currentIndex()]
        
        start_track = method_caller(drot.start_track, 
                                   [track_mode, self.input_angle.text], 
                                   self.feedback)
        self.start_track.clicked.connect(start_track)
        
        stop_track = method_caller(drot.stop_track, [], self.feedback)
        self.stop_track.clicked.connect(stop_track)
        
        

class DrotLine(BaseLine):    
    def initUI(self):
        uic.loadUi(find_ui('drot_line_frame.ui'), self)
        
    def update_device(self, data, drot):
        super(DrotLine, self).update_device(data, drot)
        
        
        self.pos_actual.setText( "{:.3f}".format(data['pos_actual']) )
        self.angle_on_sky.setText( "{:.2f}".format(data['angle_on_sky']) )

        self.track_mode_txt.setText( "{}".format(data['track_mode_txt']) )
    
    
    def link_device(self, downloader, drot, altname=None, more_methods=[]):
        """ Link a device to the widget 
        
        downloader (:class:`pydevmgr.Downloader`): a Downloader object 
        drot (:class:`pydevmgr.Drot`):  Drot device
        altname (string, optional): Alternative printed name for the device
        """
        ## disconnect all the button if they where already connected
        
        methods = [
             "---", # is a separator and is not counted as item 
            ("MOVE ANGLE", drot.move_angle, [self.input_angle.text]),
            ("TRK ELEV", drot.start_track,[lambda : TRACK_MODE.ELEV, self.input_angle.text]),
            ("TRK SKY", drot.start_track, [lambda : TRACK_MODE.SKY , self.input_angle.text]),
            ("TRK USER", drot.start_track,[lambda : TRACK_MODE.USER, self.input_angle.text]), 
            ("STOP TRK", drot.stop_track, [] ), 
        ]+ list(more_methods)
                        
        super(DrotLine, self).link_device(downloader, drot, altname, more_methods=methods)
        token = self.token # comming from super 
        
        self.input_angle.setText("{:.2f}".format(downloader.data.get(drot.stat.angle_on_sky.key, 0.0)))        
        
        downloader.add_node(token, 
                         drot.stat.pos_actual,drot.stat.angle_on_sky, 
                         drot.stat.track_mode_txt
                        )
        

record_widget("ctrl", "Drot", DrotCtrl)
record_widget("line", "Drot", DrotLine)

