from .device import Device, _name_attr, GROUP
from . import trk
from .motor import Motor, axis_type
from . import keys as K
from .manager import Manager # see at the end of file
from .interface import Int16, Int32, nodealiasproperty
from .tools import upload

#                      _              _   
#   ___ ___  _ __  ___| |_ __ _ _ __ | |_ 
#  / __/ _ \| '_ \/ __| __/ _` | '_ \| __|
# | (_| (_) | | | \__ \ || (_| | | | | |_ 
#  \___\___/|_| |_|___/\__\__,_|_| |_|\__|
# 

##### ############
# SUBSTATE
@_name_attr
class SUBSTATE(trk.SUBSTATE):
    pass
### ##############
# errors
@_name_attr
class RPC_ERROR(trk.RPC_ERROR):
    txt = {
        # add more rpc error description here if necessary
    }

### ##############
# RPC error
@_name_attr
class ERROR(trk.ERROR):
    txt = {
        # add more rpc error description here if necessary
    }

### ############# 
# Mode 
@_name_attr
class MODE:
    ENG		= 0
    STAT	= 1
    SKY		= 2
    ELEV	= 3
    USER	= 4
    group = {
        ENG		: GROUP.ENG,
        STAT	: GROUP.STATIC,
        SKY		: GROUP.TRACKING,
        ELEV	: GROUP.TRACKING,
        USER	: GROUP.TRACKING,
    }
    
def mode_parser(mode):
    if isinstance(mode, str):
        if mode not in ['SKY', 'ELEV']:
            raise ValueError('tracking mode must be one of SKY or ELEV got %r'%mode)
        mode = getattr(MODE,mode)
    return Int16(mode)

#  _       _             __                
# (_)_ __ | |_ ___ _ __ / _| __ _  ___ ___ 
# | | '_ \| __/ _ \ '__| |_ / _` |/ __/ _ \
# | | | | | ||  __/ |  |  _| (_| | (_|  __/
# |_|_| |_|\__\___|_|  |_|  \__,_|\___\___|

class DrotStatInterface(Device.StatInterface):
    ERROR = ERROR
    MODE = MODE
    SUBSTATE = SUBSTATE
    
    @nodealiasproperty("track_mode_txt", ["track_mode"])
    def track_mode_txt(self, track_mode):
        return self.MODE.txt.get(track_mode, "UNKNOWN")
    
class DrotCfgInterface(Motor.CfgInterface):
    focus_sign : Int32
    dir_sign   : Int32
    trk_period : Int32
    
# redefine the Method interface to include the proper description of the RpcError
class DrotRpcNode(Device.RpcInterface.RpcNode):
    RPC_ERROR = RPC_ERROR

class DrotRpcInterface(Device.RpcInterface):
    RpcNode = DrotRpcNode
    RPC_ERROR = RPC_ERROR
    ##
    # the type of rpcMethod argument can be defined by annotation
    # All method args types must be defined in a tuple
    rpcMoveAbs    : (float, float)
    rpcMoveRel    : (float, float)
    rpcMoveAngle  : (float,)
    rpcMoveVel    : (float,)
    rpcStartTrack : (mode_parser, float)
    
#      _            _          
#   __| | _____   _(_) ___ ___ 
#  / _` |/ _ \ \ / / |/ __/ _ \
# | (_| |  __/\ V /| | (_|  __/
#  \__,_|\___| \_/ |_|\___\___|
#
class Drot(Motor,trk.Trk):
    SUBSTATE = SUBSTATE
    MODE = MODE 
    ERROR = ERROR
    
    RpcInterface  = DrotRpcInterface
    StatInterface = DrotStatInterface
    CfgInterface  = DrotCfgInterface
    
    def start_track(self, mode, angle=0.0):
        """ Start drot tracking 
        
        Args:
            mode (int, str): tracking mode. Int constant defined in Drot.MODE.SKY, Drot.MODE.ELEV
                             str 'SKY' or 'ELEV' is also accepted
            angle (float): paSky or paPupil depending of the mode
        """
        self.rpc.rpcStartTrack.rcall(mode, angle)
    
    def move_angle(self, angle=0.0):
        """ Move drot to angle in STAT mode """
        self.rpc.rpcMoveAngle.rcall(angle)
    
    def move_abs(self, pos, vel):
        """ Move the drot to an absolute position in ENG mode 
        
        Args:
            pos (float): absolute position
            vel (float):   target velocity for the movement
        """
        self.rpc.rpcMoveAbs.rcall(pos, vel)
    
    def move_rel(self, pos, vel):
        """ Move the drot to a relative position in ENG mode 
        
        Args:
            pos (float): relative position
            vel (float): target velocity for the movement
        """
        self.rpc.rpcMoveRel.rcall(pos, vel)
    
    def move_vel(self, vel):
        """ move drot in velocity 
        
        Args:
           vel (float): target velocity
        """
        self.rpc.rpcMoveVel.rcall( vel)
    
    def stop(self):
        """ Stop drotator motion """
        self.rpc.rpcStop.rcall()
    
Manager.record_new_device_type('Drot', Drot)