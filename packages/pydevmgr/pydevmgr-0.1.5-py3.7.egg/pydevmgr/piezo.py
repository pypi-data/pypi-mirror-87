from .device import Device, _name_attr, GROUP
from . import keys as K
from .manager import Manager # see at the end of file
from .interface import Int16, Int32
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
class SUBSTATE:
    NONE                  =   0
    NOTOP_NOTREADY		  = 100
    NOTOP_READY		      = 101
    NOTOP_INITIALISING	  = 102
    NOTOP_ERROR			  = 199
    OP_DISABLING		  = 205
    OP_POS                = 203
    OP_AUTO               = 204
    OP_ERROR			  = 299
    group = {
        NONE                   : GROUP.UNKNOWN,
        NOTOP_NOTREADY         : GROUP.NOK,
        NOTOP_READY            : GROUP.NOK,
        NOTOP_INITIALISING     : GROUP.BUZY,
        NOTOP_ERROR            : GROUP.ERROR, 
        OP_DISABLING		   : GROUP.BUZY,
        OP_POS                 : GROUP.OK, 
        OP_AUTO                : GROUP.OK, 
        OP_ERROR               : GROUP.ERROR, 
    }

### ##############
# ERROR
@_name_attr
class ERROR:
    OK		      = 0
    HW_NOT_OP     = 1			
    ON_FAILURE    = 2
    MAXON         = 3
    OUT_OF_RANGE  = 4
    USER2BIT_ZERO = 5
	
	# Simulator errors
    NOT_INITIALISED		= 90
    ZERO_POINTER		= 100	
    txt = {
        OK:				   'OK',
        HW_NOT_OP:		   'ERROR: TwinCAT not in OP state or CouplerState not mapped.',
        ON_FAILURE:        'ERROR: Piezo HW failure',
        MAXON:             'ERROR: Maximum ON time exceeded.',
        OUT_OF_RANGE:      'ERROR: Piezo set position out of range',
        USER2BIT_ZERO:     'ERROR: cfg.lrUser2Bit has zero value.',
    }

### ##############
# RPC error
@_name_attr
class RPC_ERROR:
    OK			                =  0
    NOT_OP                      = -1
    NOT_NOTOP_READY		        = -2
    NOT_NOTOP_NOTREADY          = -3
    MOVING_USER                 = -5
    MOVING_BIT                  = -6
    LOCAL                       = -7
    txt = {
    	OK:						 'OK',
        NOT_OP:					 'Cannot control device. Not in OP state.',
        NOT_NOTOP_READY:		 'Call failed. Not in NOTOP_READY.',
        NOT_NOTOP_NOTREADY:		 'Call failed. Not in NOTOP_NOTREADY/ERROR.',
        LOCAL:					 'RPC calls not allowed in Local mode.',
        MOVING_USER:			 'Set user value out of range.',
        MOVING_BIT:				 'Set bit value out of range.',
    }


#  _       _             __                
# (_)_ __ | |_ ___ _ __ / _| __ _  ___ ___ 
# | | '_ \| __/ _ \ '__| |_ / _` |/ __/ _ \
# | | | | | ||  __/ |  |  _| (_| | (_|  __/
# |_|_| |_|\__\___|_|  |_|  \__,_|\___\___|

class PiezoStatInterface(Device.StatInterface):
    # keys used by default by update_to
    ERROR = ERROR
    SUBSTATE = SUBSTATE

class PiezoCfgInterface(Device.CfgInterface):
    # we can define the type to parse value directly on the class by annotation
    max_on : Int32 
    num_axis : Int16
    full_range1: Int16  
    full_range2: Int16  
    full_range3: Int16
    home1: Int16  
    home2: Int16  
    home3: Int16
    lower_limit1: Int16  
    lower_limit2: Int16  
    lower_limit3: Int16
    upper_limit1: Int16  
    upper_limit2: Int16  
    upper_limit3: Int16
    user_offset_input1: Int16  
    user_offset_input2: Int16  
    user_offset_input3: Int16
    user_offset_output1: Int16  
    user_offset_output2: Int16  
    user_offset_output3: Int16
    

# redefine the Method interface to include the proper description of the RpcError
class PiezoRpcNode(Device.RpcInterface.RpcNode):
    RPC_ERROR = RPC_ERROR

class PiezoRpcInterface(Device.RpcInterface):
    RpcNode = PiezoRpcNode
    RPC_ERROR = RPC_ERROR
    ##
    # the type of rpcMethod argument can be defined by annotation
    # All args types must be defined in a tuple
    
    rpcMoveBits : (Int16,)*3
    rpcMoveUser : (float,)*3


#      _            _          
#   __| | _____   _(_) ___ ___ 
#  / _` |/ _ \ \ / / |/ __/ _ \
# | (_| |  __/\ V /| | (_|  __/
#  \__,_|\___| \_/ |_|\___\___|
#
class Piezo(Device):
    SUBSTATE = SUBSTATE
    ERROR = ERROR

    RpcInterface = PiezoRpcInterface
    StatInterface = PiezoStatInterface
    CfgInterface = PiezoCfgInterface

         
    def auto(self):
        """ turn on auto mode """
        self.rpc.rpcAuto.rcall()   
    
    def home(self):
        """ send  piezos home  """
        self.rpc.rpcHome.rcall()
    
    def move_bits(self, pos1=0, pos2=0, pos3=0):
        """ move piezos to bits position 
        
        Args:
            pos1 (int): piezo 1 position (bits)
            pos2 (int): piezo 2 position (bits) 
            pos3 (int): piezo 3 position (bits)
        """
        # pos1, pos2, pos3 are piezo set positions in bits - integers.
        self.rpc.rpcMoveBits.rcall(pos1, pos2, pos3)
    
    def move_user(self, pos1=0.0, pos2=0.0, pos3=0.0):
        """ move piezos to user  position 
        
        Args:
            pos1 (float): piezo 1 position (user)
            pos2 (float): piezo 2 position (user) 
            pos3 (float): piezo 3 position (user)
        """
        # pos1, pos2, pos3 are piezo set positions in UU - float.
        self.rpc.rpcMoveUser.rcall(pos1, pos2, pos3)
    
    def pos(self):
        self.rpc.rpcPos.rcall()
    
    def stop(self):
        """ stop movement """
        self.rpc.rpcStop.rcall()
    

Manager.record_new_device_type('Piezo', Piezo)
