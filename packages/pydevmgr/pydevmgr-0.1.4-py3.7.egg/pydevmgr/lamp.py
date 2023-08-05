from .device import Device, _name_attr, _inc,  GROUP
from . import keys as K
from .manager import Manager # see at the end of file
from .interface import UInt32, Int32, nodealiasproperty
from .tools import upload

#                      _              _   
#   ___ ___  _ __  ___| |_ __ _ _ __ | |_ 
#  / __/ _ \| '_ \/ __| __/ _` | '_ \| __|
# | (_| (_) | | | \__ \ || (_| | | | | |_ 
#  \___\___/|_| |_|___/\__\__,_|_| |_|\__|
# ##### ###########
## SUBSTATE
@_name_attr
class SUBSTATE:    
    NONE                  =   0    
    NOTOP_NOTREADY        = 100    
    NOTOP_INITIALISING    = 102    
    NOTOP_READY_OFF       = 103    
    NOTOP_READY_ON        = 104    
    NOTOP_ERROR           = 199    
    OP_DISABLING          = 205    
    OP_OFF                = 206    
    OP_SWITCHING_OFF      = 207    
    OP_COOLING            = 208    
    OP_ON                 = 209    
    OP_SWITCHING_ON       = 210    
    OP_WARMING            = 211    
    OP_ERROR              = 299
    group = {
        NONE                   : GROUP.UNKNOWN,
        NOTOP_NOTREADY         : GROUP.NOK,
        NOTOP_READY_OFF        : GROUP.NOK,
        NOTOP_READY_ON         : GROUP.NOK,
        NOTOP_INITIALISING     : GROUP.BUZY,
        NOTOP_ERROR            : GROUP.ERROR, 
  
        OP_DISABLING            : GROUP.BUZY, 
        OP_SWITCHING_OFF        : GROUP.BUZY,
        OP_SWITCHING_ON         : GROUP.BUZY,

        OP_COOLING              : GROUP.BUZY,
        OP_WARMING              : GROUP.BUZY,
        OP_ON                   : GROUP.OK,
        OP_OFF                  : GROUP.OK,
        OP_ERROR                : GROUP.ERROR,    
    }


### #############
# ERROR
@_name_attr
class ERROR:
  
    OK					= _inc(0)
    HW_NOT_OP           = _inc()
    INIT_FAILURE        = _inc()		
    UNEXPECTED_OFF      = _inc()
    UNEXPECTED_ON       = _inc()
    FAULT_SIG           = _inc()
    MAXON               = _inc()
    STILL_COOLING       = _inc()
    TIMEOUT_DISABLE     = _inc()
    TIMEOUT_INIT        = _inc()
    TIMEOUT_OFF         = _inc()
    TIMEOUT_ON          = _inc()
    # Simulator errors
    SIM_NOT_INITIALISED	= 90
    SIM_NULL_POINTER    = 100	
    txt = {
        OK:					 'OK',
	    HW_NOT_OP:			 'ERROR: TwinCAT not in OP state or CouplerState not mapped.',
	    INIT_FAILURE:		 'ERROR: INIT command aborted due to STOP or RESET.',
	    UNEXPECTED_OFF:		 'ERROR: Lamp unexpectedly switched OFF.',
	    UNEXPECTED_ON:		 'ERROR: Lamp unexpectedly switched ON.',
	    FAULT_SIG:			 'ERROR: Fault signal active.',
	    MAXON:				 'ERROR: Lamp maximum ON time exceeded.',
	    STILL_COOLING:		 'ERROR: ON command not allowed while cooling.',
	    TIMEOUT_DISABLE:	 'ERROR: Disable timed out.',
	    TIMEOUT_INIT:		 'ERROR: Init timed out.',
	    TIMEOUT_OFF:		 'ERROR: Switching OFF timed out.',
	    TIMEOUT_ON:			 'ERROR: Switching ON timed out.',
	    SIM_NOT_INITIALISED: 'ERROR: Lamp simulator not initialised.',
	    SIM_NULL_POINTER:	 'ERROR: NULL pointer to Lamp.',
    }

### #############
## RPC error
@_name_attr
class RPC_ERROR:    
    OK                 =  0     
    NOT_OP             = -1    
    NOT_NOTOP_READY    = -2    
    NOT_NOTOP_NOTREADY = -3    
    SWITCHING_ON       = -4    
    SWITCHING_OFF      = -5    
    COOLING            = -6    
    LOCAL              = -7
    txt = {
        OK:						 'OK',
	    NOT_OP:					 'Cannot control lamp. Not in OP state.',
	    NOT_NOTOP_READY:		 'Call failed. Not in NOTOP_READY.',
	    NOT_NOTOP_NOTREADY:		 'Call failed. Not in NOTOP_NOTREADY/ERROR.',
	    SWITCHING_ON:			 'Lamp OFF failed. Still switching ON.',
	    SWITCHING_OFF:			 'Lamp ON failed. Still switching OFF.',
	    COOLING:				 'Lamp ON failed. Still cooling down.',
	    LOCAL:					 'RPC calls not allowed in Local mode',
    }

#  _       _             __                
# (_)_ __ | |_ ___ _ __ / _| __ _  ___ ___ 
# | | '_ \| __/ _ \ '__| |_ / _` |/ __/ _ \
# | | | | | ||  __/ |  |  _| (_| | (_|  __/
# |_|_| |_|\__\___|_|  |_|  \__,_|\___\___|

class LampStatInterface(Device.StatInterface):
    ERROR = ERROR
    SUBSTATE = SUBSTATE
    
    @nodealiasproperty("is_ready", ["substate"])
    def is_ready(self, substate):
        return substate in [self.SUBSTATE.NOTOP_READY_ON, self.SUBSTATE.NOTOP_READY_OFF]
    
    @nodealiasproperty("is_off", ["substate"])
    def is_off(self, substate):
        return substate == Lamp.SUBSTATE.OP_OFF
    
    @nodealiasproperty("is_on", ["substate"])
    def is_on(self, substate):
        return substate == Lamp.SUBSTATE.OP_ON
    
class LampCfgInterface(Device.CfgInterface):    
    # we can define the type to parse value directly on the class by annotation    
    analog_threshold : Int32
    analog_range : UInt32
    cooldown: UInt32
    maxon : UInt32 
    warmup : UInt32
    timeout : UInt32
    
    # redefine the Method interface to include the proper description of the RpcError
class LampRpcNode(Device.RpcInterface.RpcNode):
    RPC_ERROR = RPC_ERROR

class LampRpcInterface(Device.RpcInterface):    
    RpcNode = LampRpcNode    
    RPC_ERROR = RPC_ERROR    
    ##    # the type of rpcMethod argument can be defined by annotation    
    # All args types must be defined in a tuple    
    rpcSwitchOn : (float, UInt32)    
    
#      _            _          
#   __| | _____   _(_) ___ ___ 
#  / _` |/ _ \ \ / / |/ __/ _ \
# | (_| |  __/\ V /| | (_|  __/
#  \__,_|\___| \_/ |_|\___\___|
#
class Lamp(Device):    
    SUBSTATE = SUBSTATE    
    ERROR = ERROR
      
    RpcInterface = LampRpcInterface    
    StatInterface = LampStatInterface    
    CfgInterface = LampCfgInterface
    
    def switch_on(self, intensity, time_limit): 
        """ switch on the lamp 
        
        Args:
            intensity (float): in % 
            time_limit (float): number of second the lamp will stay on
        """       
        # intensity - float, onTimeLimit - integer        
        self.rpc.rpcSwitchOn.rcall(intensity, onTimeLimit)
        
    def switch_off(self):
        """ switch off the lamp """        
        self.rpc.rpcSwitchOff.rcall()
        

Manager.record_new_device_type('Lamp', Lamp)