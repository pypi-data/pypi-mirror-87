""" Not a device but define some share methods end constant for tracking devices """
from .device import _name_attr, GROUP
from .motor import Motor
from .tools import upload

##### ############
# SUBSTATE
@_name_attr
class SUBSTATE:
    NONE =  0

    NOTOP_NOTREADY =  100
    NOTOP_READY = 101
    NOTOP_INITIALIZING = 102
    NOTOP_ABORTING = 107
    NOTOP_RESETTING = 109
    NOTOP_ENABLING = 110
    
    NOTOP_ERROR =  199

    OP_DISABLING 	= 205
    OP_STANDSTILL	= 216
    OP_MOVING		= 217
    OP_SETTING_POS	= 218
    OP_STOPPING		= 219
    OP_TRACKING		= 220
    OP_PRESETTING	= 221

    OP_ERROR =299
    group = {
        NOTOP_NOTREADY     :  GROUP.NOK, 
        NOTOP_READY        :  GROUP.NOK,
        NOTOP_INITIALIZING :  GROUP.BUZY, 
        NOTOP_ABORTING     :  GROUP.BUZY, 
        NOTOP_RESETTING    :  GROUP.BUZY, 
        NOTOP_ENABLING     :  GROUP.BUZY, 
        NOTOP_ERROR        :  GROUP.ERROR, 
        OP_DISABLING 	  :  GROUP.BUZY, 
        OP_STANDSTILL	  :  GROUP.OK,
        OP_MOVING		  :  GROUP.BUZY, 
        OP_SETTING_POS	  :  GROUP.BUZY, 
        OP_STOPPING		  :  GROUP.BUZY, 
        OP_TRACKING		  :  GROUP.OK, 
        OP_PRESETTING	  :  GROUP.BUZY, 
        OP_ERROR          :  GROUP.ERROR,   
    }

SUBSTATE.GROUP_BUZY = (SUBSTATE.NOTOP_INITIALIZING, SUBSTATE.OP_MOVING, 
                       SUBSTATE.OP_STOPPING,SUBSTATE.OP_PRESETTING)
SUBSTATE.GROUP_ERROR = (SUBSTATE.NOTOP_ERROR, SUBSTATE.OP_ERROR)
SUBSTATE.GROUP_OK = (SUBSTATE.OP_STANDSTILL,SUBSTATE.OP_TRACKING)



### ##############
# ERROR
@_name_attr
class ERROR(Motor.ERROR):
    # add more error if necessary 
    txt = dict(Motor.ERROR.txt, **{
        # add more error description here if necessary 
    })

### ##############
# RPC error
@_name_attr
class RPC_ERROR(Motor.RpcInterface.RPC_ERROR):
    # add rpc error if necessary
    txt = dict(Motor.RpcInterface.RPC_ERROR.txt, **{
        # add more rpc error description here if necessary
    })

    
class Trk:
    # note start_track not defined here 
    # because specific (Adc.start_track take one arg Drot.start_track two)
        
    def stop_track(self):
        self.rpc.rpcStopTrack.rcall()
    
    def is_moving(self, data=None):
        """ -> True is axis is moving """
        substate =  self.stat.substate.get() if data is None else data[self.stat.substate.key]
        return substate == self.SUBSTATE.OP_MOVING

    def is_standstill(self, data=None):
        """ -> True is axis is standing still """
        substate =  self.stat.substate.get() if data is None else data[self.stat.substate.key]
        return substate == self.SUBSTATE.OP_STANDSTILL
    
    def is_tracking(self, data=None):
        """ -> True if device is tracking """
        substate =  self.stat.substate.get() if data is None else data[self.stat.substate.key]
        return substate == self.SUBSTATE.OP_TRACKING
    
    def is_presetting(self, data=None):
        """ -> True if device is presetting """
        substate = self.stat.substate.get() if data is None else data[self.stat.substate.key]
        return substate == self.SUBSTATE.OP_PRESETTING