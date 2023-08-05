from .device import Device, _name_attr, _inc, GROUP
from . import keys as K
from .manager import Manager # see at the end of file
from .interface import InterfaceProperty, nodealiasproperty, Int16, Int32
from collections import OrderedDict 
from .tools import upload
#                      _              _   
#   ___ ___  _ __  ___| |_ __ _ _ __ | |_ 
#  / __/ _ \| '_ \/ __| __/ _` | '_ \| __|
# | (_| (_) | | | \__ \ || (_| | | | | |_ 
#  \___\___/|_| |_|___/\__\__,_|_| |_|\__|
# 

##### ############
# Sequence
@_name_attr
class INITSEQ:
    END = 0
    FIND_INDEX = 1
    FIND_REF_LE = 2
    FIND_REF_UE = 3
    FIND_LHW = 4
    FIND_UHW = 5

    DELAY = 6
    MOVE_ABS = 7
    MOVE_REL = 8
    CALIB_ABS = 9
    CALIB_REL = 10
    CALIB_SWITCH = 11

##### ############
# SUBSTATE
@_name_attr
class SUBSTATE:
    NONE =  0

    NOTOP_NOTREADY =  100
    NOTOP_READY = 101
    NOTOP_INITIALIZING = 102
    NOTOP_ABORTING = 107
    NOTOP_CLEARING_NOVRAM = 108

    NOTOP_ERROR =  199

    OP_STANDSTILL =216
    OP_MOVING = 217
    OP_SETTING_POS = 218
    OP_STOPPING = 219

    OP_ERROR =299
    group = {
        NONE                   : GROUP.UNKNOWN,
        NOTOP_NOTREADY         : GROUP.NOK,
        NOTOP_READY            : GROUP.NOK,
        NOTOP_INITIALIZING     : GROUP.BUZY,
        NOTOP_ABORTING         : GROUP.BUZY,
        NOTOP_CLEARING_NOVRAM  : GROUP.BUZY,
        NOTOP_ERROR            : GROUP.ERROR, 
        OP_STANDSTILL          : GROUP.OK, 
        OP_MOVING              : GROUP.BUZY, 
        OP_SETTING_POS         : GROUP.BUZY,
        OP_STOPPING            : GROUP.BUZY,
        OP_ERROR               : GROUP.ERROR,    
    }


### ############
# Motor ERROR
@_name_attr
class ERROR:
    OK	                   = _inc(0)
    HW_NOT_OP              = _inc()
    LOCAL                  = _inc()
    INIT_ABORTED           = _inc()
    TIMEOUT_INIT           = _inc()
    TIMEOUT_MOVE           = _inc()
    TIMEOUT_RESET          = _inc()
    TIMEOUT_SETPOS         = _inc()
    TIMEOUT_USER_PREINIT   = _inc()
    TIMEOUT_USER_POSTINIT  = _inc()
    TIMEOUT_USER_PREMOVE   = _inc()
    TIMEOUT_USER_POSTMOVE  = _inc()
    SETPOS                 = _inc()
    STOP                   = _inc()
    ABORT                  = _inc()
    SW_LIMIT_LOWER         = _inc()
    SW_LIMIT_UPPER         = _inc()
    BRAKE_ACTIVE           = _inc()
    BRAKE_ENGAGE           = _inc()
    BRAKE_DISENGAGE        = _inc()
    SWITCH_NOT_USED        = _inc()
    ENABLE                 = _inc()
    NOVRAM_READ            = _inc()
    NOVRAM_WRITE           = _inc()
    SWITCH_EXIT            = _inc()
    STOP_LIMITS_BOTH       = _inc()
    HW_LIMITS_BOTH         = _inc()
    IN_POS                 = _inc()
    LOCKED                 = _inc()
    SoE_ADS_ERROR          = _inc()
    SoE_SERCOS_ERROR       = _inc()

    # Simulator errors
    SIM_NOT_INITIALISED			= 90
    SIM_NULL_POINTER			= 100	

    # TwinCAT errors
    TC_VEL						= 16929	
    TC_NOT_READY_FOR_START		= 16933	
    TC_DISABLED_MOVE			= 16992	
    TC_BISECTION				= 17022	
    TC_MODULO_POS				= 17026	
    TC_STOP_ACTIVE				= 17135	
    TC_VEL_NEG					= 17241	
    TC_TARGET_LSW				= 17504	
    TC_TARGET_USW				= 17505	
    TC_FOLLOWING_ERROR			= 17744	
    TC_NOT_READY				= 18000	
    TC_IN_POS_6_SEC				= 19207	
    txt = {
    	OK:					  'OK',
    	HW_NOT_OP:			  'ERROR: TwinCAT not OP or CouplerState not mapped.',
    	LOCAL:				  'ERROR: Control not allowed. Motor in Local mode.',
    	INIT_ABORTED:		  'ERROR: INIT command aborted.',
    	TIMEOUT_INIT:		  'ERROR: INIT timed out.',
    	TIMEOUT_MOVE:		  'ERROR: Move timed out.',
    	TIMEOUT_RESET:		  'ERROR: Reset timed out.',
    	TIMEOUT_SETPOS:		  'ERROR: Set Position timed out.',
    	TIMEOUT_USER_PREINIT: 'ERROR: User PRE-INIT timed out.',
    	TIMEOUT_USER_POSTINIT:'ERROR: User POST-INIT timed out.',
    	TIMEOUT_USER_PREMOVE: 'ERROR: User PRE-MOVE timed out.',
    	TIMEOUT_USER_POSTMOVE:'ERROR: User POST-MOVE timed out.',
    	SETPOS:				  'ERROR: Set Position failed.',
    	STOP:				  'ERROR: STOP failed.',
    	
    	ABORT:				  'ERROR: Motion aborted.',
    	SW_LIMIT_LOWER:		  'ERROR: Lower SW Limit Exceeded.',
    	SW_LIMIT_UPPER:		  'ERROR: Upper SW Limit Exceeded.',
    	BRAKE_ACTIVE:		  'ERROR: Cannot move. Brake active.',
    	BRAKE_ENGAGE:		  'ERROR: Failed to engage brake.',
    	BRAKE_DISENGAGE:	  'ERROR: Failed to disengage brake.',
    	SWITCH_NOT_USED:	  'ERROR: Switch was not detected in previous INIT action.',
    	ENABLE:				  'ERROR: Failed to enable Axis.',
    	NOVRAM_READ:		  'ERROR: Failed to read from NOVRAM',
    	NOVRAM_WRITE:		  'ERROR: Failed to write to NOVRAM',
    	SWITCH_EXIT:		  'ERROR: Timeout on switch exit. Check nTimeoutSwitch.',
    	STOP_LIMITS_BOTH:	  'ERROR: Both LSTOP and USTOP limits active.',
    	HW_LIMITS_BOTH:		  'ERROR: Both limit switches LHW and UHW active.',
    	IN_POS:				  'ERROR: In-Pos switch not active at the end of movement.',
    	LOCKED:				  'ERROR: Motor Locked! Cannot move.',
    	SoE_ADS_ERROR:		  'ERROR: SoE ADS Error.',
    	SoE_SERCOS_ERROR:	  'ERROR: SoE Sercos Error.',

    	SIM_NOT_INITIALISED:  'ERROR: Simulator not initialised.',
    	SIM_NULL_POINTER:	  'ERROR: Simulator input parameter is a NULL pointer.',
    	
    	# Beckhoff TwinCAT most common errors
    	TC_VEL:				    'ERROR: Requested set velocity is not allowed.',
    	TC_NOT_READY_FOR_START: 'ERROR: Drive not ready during axis start. Maybe SW limits.',
    	TC_DISABLED_MOVE:		'ERROR: Motor disabled while moving. Reset required!',
    	TC_BISECTION:			'WARNING: Motion command could not be realized (BISECTION)',
    	TC_MODULO_POS:		  'ERROR: Target position >= full turn (modulo-period)',
    	TC_STOP_ACTIVE:		  'ERROR: Stop command still active. Axis locked. Reset required!',
    	TC_VEL_NEG:			  'ERROR: Set velocity not allowed (<=0)',
    	TC_TARGET_LSW:		  'ERROR: Target position beyond Lower Software Limit.',
    	TC_TARGET_USW:		  'ERROR: Target position beyond Upper Software Limit.',
    	TC_FOLLOWING_ERROR:	  'ERROR: Following error. Reset required!',
    	TC_NOT_READY:		  'ERROR: Drive not ready for operation.',
    	TC_IN_POS_6_SEC:	  'ERROR: In-position 6 sec timeout. Reset required!',
    }
# e.g. ERROR.txt.get( er_code, "Unknown Error") -> return the error text



### ##############
# RPC error
@_name_attr
class RPC_ERROR:
    OK =  0
    NOT_OP =  -1
    NOT_NOTOP_READY =  -2
    NOT_NOTOP_NOTREADY = -3
    LOCAL =  -4
    SW_LIMIT_LOWER = -5
    SW_LIMIT_UPPER = -6
    INIT_WHILE_MOVING = -7
    txt = {
        OK:					 'OK',
        NOT_OP:				 'Cannot control motor. Not in OP state.',
        NOT_NOTOP_READY:	 'Call failed. Not in NOTOP_READY.',
        NOT_NOTOP_NOTREADY:	 'Call failed. Not in NOTOP_NOTREADY/ERROR.',
        LOCAL:				 'RPC calls not allowed in Local mode.',
        SW_LIMIT_LOWER:		 'Move rejected. Target Pos < Lower SW Limit',
        SW_LIMIT_UPPER:		 'Move rejected. Target Pos > Upper SW Limit',
        INIT_WHILE_MOVING:	 'Cannot INIT moving motor. Motor stopped. Retry.',
    }
    
@_name_attr
class AXIS_TYPE:
    LINEAR= 1
    CIRCULAR=2
    CIRCULAR_OPTIMISED = 3

def axis_type(value):
    """ return always a axis_type int number from a number or a string
    
    Raise a ValueError if the input string does not match axis type
    Example:
        axis_type('LINEAR') == 1
        axis_type(1) == 1
    """
    try:
        val = getattr(AXIS_TYPE, value) if isinstance(value, str) else value
    except AttributeError:
        raise ValueError('Unknown AXIS type %r'%value)
    return Int32(val)
# 
#   __                  _   _                 
#  / _|_   _ _ __   ___| |_(_) ___  _ __  ___ 
# | |_| | | | '_ \ / __| __| |/ _ \| '_ \/ __|
# |  _| |_| | | | | (__| |_| | (_) | | | \__ \
# |_|  \__,_|_| |_|\___|\__|_|\___/|_| |_|___/
# 

def init_sequence_to_cfg(initialisation, INITSEQ=INITSEQ):
    """ from a config initialisation dict return a dictionary of key/value for .cfg interface """            
    # set the init sequence
    
    cfg_dict = {} 
        
    sequence = initialisation['sequence']
    
    # reset all sequence variable
    for i in range(1,11):
        cfg_dict["init_seq{}_action".format(i)] = INITSEQ.END
        cfg_dict["init_seq{}_value1".format(i)] = 0.0
        cfg_dict["init_seq{}_value2".format(i)] = 0.0
        
    # in mapping file the sequence number start from 1
    for seqnum, action_name in enumerate(sequence, start=1):
        try:
            action_number = getattr(INITSEQ, action_name)
        except AttributeError:
            raise ValueError('Unknown init sequence action %r'%action_name)

        try:
            action_def = initialisation[action_name]
        except KeyError:
            raise ValueError("Definition of init sequence action %r is missing"%action_name)

        try:
            value1 = action_def['value1']
        except KeyError:
            raise ValueError("Could not find 'value1' in inisequence at action %r"%action_name)

        try:
            value2 = action_def['value2']
        except KeyError:
            raise ValueError("Could not find 'value2' in inisequence at action %r"%action_name)

        cfg_dict["init_seq%d_action"%seqnum] = action_number
        cfg_dict["init_seq%d_value1"%seqnum] = value1
        cfg_dict["init_seq%d_value2"%seqnum] = value2        
    return cfg_dict




#  _       _             __                
# (_)_ __ | |_ ___ _ __ / _| __ _  ___ ___ 
# | | '_ \| __/ _ \ '__| |_ / _` |/ __/ _ \
# | | | | | ||  __/ |  |  _| (_| | (_|  __/
# |_|_| |_|\__\___|_|  |_|  \__,_|\___\___|

class MotorStatInterface(Device.StatInterface): 
    ERROR = ERROR
    SUBSTATE = SUBSTATE
    
    @nodealiasproperty("is_moving", ["substate"])
    def is_moving(self, substate):
        """ -> True is axis is moving """
        return substate == self.SUBSTATE.OP_MOVING

    @nodealiasproperty("is_standstill", ["substate"])
    def is_standstill(self,  substate):
        """ -> True is axis is standstill """
        return substate == self.SUBSTATE.OP_STANDSTILL
    
    _mot_positions = None# will be overwriten by motor 
    @nodealiasproperty("pos_name", ["pos_actual"])
    def pos_name(self, pos_actual):
        if not self._mot_positions: return ''
        positions = self._mot_positions
        tol = positions['tolerance']
        for pname in positions['posnames']:
            if abs(positions[pname]-pos_actual)<tol:
                return pname
        return ''
    
class MotorCfgInterface(Device.CfgInterface):
    # we can define the type to parse value directly on the class by annotation
    axis_type : axis_type
    tout_init: Int32 
    tout_move: Int32        
    tout_switch: Int32
    init_seq1_action: Int32
    init_seq2_action: Int32
    init_seq3_action: Int32
    init_seq4_action: Int32
    init_seq5_action: Int32
    init_seq6_action: Int32
    init_seq7_action: Int32
    init_seq8_action: Int32
    init_seq9_action: Int32
    init_seq10_action: Int32

# redefine the Method interface to include the proper description of the RpcError
class MotorRpcNode(Device.RpcInterface.RpcNode):
    RPC_ERROR = RPC_ERROR

class MotorRpcInterface(Device.RpcInterface):
    RpcNode = MotorRpcNode
    RPC_ERROR = RPC_ERROR
    
    
    ##
    # the type of rpcMethod argument can be defined by annotation
    # All args types must be defined in a tuple
    rpcMoveAbs : (float, float)
    rpcMoveRel : (float, float)
    rpcMoveVel : (float,)

#      _            _          
#   __| | _____   _(_) ___ ___ 
#  / _` |/ _ \ \ / / |/ __/ _ \
# | (_| |  __/\ V /| | (_|  __/
#  \__,_|\___| \_/ |_|\___\___|
#
class Motor(Device):
    SUBSTATE = SUBSTATE
    ERROR = ERROR
    
    INITSEQ = INITSEQ
    AXIS_TYPE = AXIS_TYPE

    RpcInterface = MotorRpcInterface
    StatInterface = MotorStatInterface
    CfgInterface = MotorCfgInterface
    
    def get_configuration(self, **kwargs):
        """  return a node/value pair dictionary ready to be uploaded 
        
        The node/value dictionary represent the device configuration. 
        
        Args:
            **kwargs : name/value pairs pointing to cfg.name node
                      This allow to change configuration on the fly
                      without changing the config file. 
        """
        
        config = self._config 
        
        ctrl_config = config.get(K.CTRL_CONFIG, {})  
        # just update what is in ctrl_config, this should work for motor 
        # one may need to check parse some variable more carefully       
        cfg_dict = {self.cfg.get_node(k):v for k,v in  ctrl_config.items() }
        cfg_dict.update({self.cfg.get_node(k):v for k,v in  kwargs.items() })
        
        
        try:
            initialisation = config[K.INITIALISATION]
        except KeyError:
            pass
        else:
            init_cfg = init_sequence_to_cfg(initialisation, self.INITSEQ)
            cfg_dict.update({self.cfg.get_node(k):v for k,v in init_cfg.items()})
        
        ###
        # Set the new config value to the device 
        return cfg_dict
          
    
    ### redefine stat property to include positions
    stat = InterfaceProperty('stat', 'StatInterface')
    @stat.finalizer
    def stat(self, interface):
        interface._mot_positions = self._config.get('positions', None)
    
    @property
    def posnames(self):
        """ configured position names in a name:(pos, tol) dictionary """
        try:
            return self.__dict__['posnames']
        except KeyError:                             
            try:
                positions = self._config['positions']
                tol = positions['tolerance']
                posnames = OrderedDict( (name,(positions[name], tol)) for name in positions['posnames'])
            except KeyError as e:
                posnames = {}
            # cash the posnames
            self.__dict__['posnames'] =  posnames    
            return posnames          
        
    
    def clear(self):
        """ Clear cashed values """
        super(Motor, self).clear()
        self.__dict__.pop('posnames', None)
    
    def move_abs(self, absPos, vel):
        """ move motor to an absolute position 
        
        self.move_abs(pos, vel) <-> self.rpc.rpcMoveAbs(pos, vel)
        
        Args:
            absPos (float): absolute position
            vel (float):   target velocity for the movement
            
        """
        self.rpc.rpcMoveAbs.rcall(absPos, vel)
    
    def move_name(self, name, vel):
        """ move motor to a named position 
        
        Args:
           name (str): named position
           vel (float):   target velocity for the movement
        """
        absPos = self.get_pos_target_of_name(name)
        self.rpc.rpcMoveAbs.rcall(absPos, vel)
        
    def move_rel(self, relPos, vel):
        """ Move motor relative position
        
        Args:
           relPos (float): relative position
           vel (float):   target velocity for the movement
        """
        self.rpc.rpcMoveRel.rcall(relPos, vel)

    def move_vel(self, vel):
        """ Move motor in velocity mode 
        
        Args:
           vel (float): target velocity
        """
        self.rpc.rpcMoveVel.rcall(vel)

    def stop(self):
        """ Stop the motor """
        self.rpc.rpcStop.rcall()

    
    def get_pos_target_of_name(self, name):
        """return the configured target position of a given pos name or raise error"""
        try:
            position = self._config['positions'][name]
        except KeyError:
            raise ValueError('unknown posname %r'%name)
        return position

    def get_name_of_pos(self, pos_actual):
        """ Retrun the name of a position from a position as input or ''
        
        Example:
            m.get_name_of( m.stat.pos_actual.get() )
        """
        try:
            positions = self._config['positions']
        except KeyError:
            return ''

        tol = positions['tolerance']
        for pname in positions['posnames']:
            if abs(positions[pname]-pos_actual)<tol:
                return pname
        return ''
        
    def is_near(self, pos, tol, data=None):
        """ -> True when abs(pos_actual-pos)<tol """
        apos = self.stat.pos_actual.get(data) 
        return abs(apos-pos)<tol
    
Manager.record_new_device_type('Motor', Motor)