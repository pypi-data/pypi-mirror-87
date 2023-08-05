from .device import Device, _name_attr, _inc, GROUP
from . import keys as K
from .manager import Manager # see at the end of file
from .interface import nodealiasproperty, UInt32
from .tools import upload

#                      _              _   
#   ___ ___  _ __  ___| |_ __ _ _ __ | |_ 
#  / __/ _ \| '_ \/ __| __/ _` | '_ \| __|
# | (_| (_) | | | \__ \ || (_| | | | | |_ 
#  \___\___/|_| |_|___/\__\__,_|_| |_|\__|
# 


@_name_attr
class SUBSTATE:
    OFF = 0
    NOT_OP = 1
    OP = 2
    NOT_OP_NOT_READY = 100
    NOT_OP_INITIALIZING = 102
    NOT_OP_READY_CLOSED = 105
    NOT_OP_READY_OPEN = 106
    NOT_OP_FAILURE = 199
    OP_DISABLING = 205
    OP_CLOSED = 212
    OP_CLOSING = 213
    OP_OPEN = 214
    OP_OPENING = 215
    OP_FAILURE = 299
    group = {
        OFF                   : GROUP.UNKNOWN,
        OP                    : GROUP.OK,
        NOT_OP_NOT_READY      : GROUP.NOK,
        NOT_OP_READY_CLOSED   : GROUP.NOK,
        NOT_OP_READY_OPEN     : GROUP.NOK,
        NOT_OP_INITIALIZING   : GROUP.BUZY,
        NOT_OP_FAILURE        : GROUP.ERROR,
        OP_DISABLING          : GROUP.BUZY, 
        OP_CLOSING            : GROUP.BUZY, 
        OP_OPENING            : GROUP.BUZY,
        OP_FAILURE            : GROUP.ERROR,
        OP_CLOSED             : GROUP.OK, 
        OP_OPEN               : GROUP.OK,    
    }
    


@_name_attr
class ERROR:
    OK				      = _inc(0)
    HW_NOT_OP             = _inc()			
    INIT_FAILURE          = _inc()	
    UNEXPECTED_CLOSED     = _inc()	
    UNEXPECTED_NONE       = _inc()	
    UNEXPECTED_OPENED     = _inc()	
    FAULT_SIG             = _inc()	
    BOTH_SIG_ACTIVE       = _inc()
    TIMEOUT_ENABLE        = _inc()
    TIMEOUT_DISABLE       = _inc()
    TIMEOUT_INIT          = _inc()
    TIMEOUT_CLOSE         = _inc()
    TIMEOUT_OPEN          = _inc()
    
    SIM_NOT_INITIALISED		= 90
    SIM_NULL_POINTER		= 100	# Simulator error
    txt = {
        OK:				   'OK',
        HW_NOT_OP:		   'ERROR: TwinCAT not in OP state or CouplerState not mapped.',
        INIT_FAILURE:	   'ERROR: INIT command aborted due to STOP or RESET.',
        UNEXPECTED_CLOSED: 'ERROR: Shutter unexpectedly closed.',
        UNEXPECTED_NONE:   'ERROR: Unexpectedly no OPEN or CLOSED signal active.',
        UNEXPECTED_OPENED: 'ERROR: Shutter unexpectedly opened.',
        FAULT_SIG:		   'ERROR: Fault signal active.',
        BOTH_SIG_ACTIVE:   'ERROR: Both OPEN and CLOSED signals active.',
        TIMEOUT_ENABLE:	   'ERROR: ENABLE timed out.',
        TIMEOUT_DISABLE:   'ERROR: DISABLE timed out.',
        TIMEOUT_INIT:	   'ERROR: INIT timed out.',
        TIMEOUT_CLOSE:	   'ERROR: CLOSE timed out.',
        TIMEOUT_OPEN:		  'ERROR: OPEN timed out.',
        SIM_NOT_INITIALISED:  'ERROR: Shutter simulator not initialised.',
        SIM_NULL_POINTER:	  'ERROR: NULL pointer to Shutter.',
    }
@_name_attr
class RPC_ERROR:
    OK =  0
    NOT_OP				= -1			
    NOT_NOTOP_READY		= -2			
    NOT_NOTOP_NOTREADY	= -3	
    STILL_OPENING = -4
    STILL_CLOSING = -5
    LOCAL = -6
    txt = { # copy past on MgetRpcErrorTxt
        OK:					 'OK',
	    NOT_OP:				 'Cannot control shutter. Not in OP state.',
	    NOT_NOTOP_READY:	 'Call failed. Not in NOTOP_READY.',
	    NOT_NOTOP_NOTREADY:	 'Call failed. Not in NOTOP_NOTREADY/ERROR.',
	    STILL_OPENING:		 'Not allowed to close the shutter while opening.',
	    STILL_CLOSING:		 'Not allowed to open the shutter while closing.',
	    LOCAL:				 'RPC calls not allowed in Local mode.',
    }



#  _       _             __                
# (_)_ __ | |_ ___ _ __ / _| __ _  ___ ___ 
# | | '_ \| __/ _ \ '__| |_ / _` |/ __/ _ \
# | | | | | ||  __/ |  |  _| (_| | (_|  __/
# |_|_| |_|\__\___|_|  |_|  \__,_|\___\___|

class ShutterStatInterface(Device.StatInterface):
    
    
    
    ERROR = ERROR
    SUBSTATE = SUBSTATE
    
    @nodealiasproperty("is_ready", ["substate"])
    def is_ready(self, substate):
        return substate in [self.SUBSTATE.NOT_OP_READY_OPEN, self.SUBSTATE.NOT_OP_READY_CLOSED]
        
    @nodealiasproperty("is_open", ["substate"])
    def is_open(self, substate):
        return substate == self.SUBSTATE.OP_OPEN
    
    @nodealiasproperty("is_closed", ["substate"])
    def is_closed(self, substate):
        return substate == self.SUBSTATE.OP_CLOSED
    
class ShutterCfgInterface(Device.CfgInterface):
    # we can define the type to parse value directly on the class by annotation
    timeout: UInt32  

# redefine the Method interface to include the proper description of the RpcError
class ShutterRpcNode(Device.RpcInterface.RpcNode):
    RPC_ERROR = RPC_ERROR

class ShutterRpcInterface(Device.RpcInterface):
    RpcNode = ShutterRpcNode
    RPC_ERROR = RPC_ERROR
    

#      _            _          
#   __| | _____   _(_) ___ ___ 
#  / _` |/ _ \ \ / / |/ __/ _ \
# | (_| |  __/\ V /| | (_|  __/
#  \__,_|\___| \_/ |_|\___\___|
#
class Shutter(Device):
    SUBSTATE = SUBSTATE
    RpcInterface = ShutterRpcInterface
    StatInterface = ShutterStatInterface
    CfgInterface = ShutterCfgInterface

    def open(self):
        """ open the shutter """
        self.rpc.rpcOpen.rcall()    
    
    def close(self):
        """ close the shutter """
        self.rpc.rpcClose.rcall()
        
    def stop(self):
        """ stop any motion """
        self.rpc.rpcStop.rcall()
    
Manager.record_new_device_type('Shutter', Shutter)


