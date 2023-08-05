from . import io
from . import keys as K
from .tools import upload
from .io import load_default_map
from .interface import (kjoin, fjoin, Interface, RpcInterface, InterfaceProperty, 
                         get_ua_client, connect_ua_client, disconnect_ua_client, 
                         DEFAULT_NAME_SPACE, _name_attr, nodealiasproperty, ksplit, fsplit, fjoin)


# this is a global mapping allowing to change the opc.tcp address on the fly 
# usefull when switching from real PLC to simulated one without having to 
# edit the config files. The key should be the full address to replce (including port)
# e.g. host_mapping = {"opc.tcp://134.171.59.99:4840": "opc.tcp://192.168.1.28:4840"}
host_mapping = {}

_enum = -1 
def _inc(i=None):
    """ number increment to use in frontend 
    
    _inc(0) # reset increment to 0 and return 0 
    _inc()  # increment and return incremented number 
    """
    global _enum
    _enum = _enum+1 if i is None else i
    return _enum

class GROUP:
    """ Constants holder GROUP are used to classify state and substates
    
    This class is not intended to be instancied but only to hold constants
    
    An application if for widget styling for instance : one style per group
    
        SUBSTATE.group[SUBSTATE.NOTOP_NOTREADY] == GROUP.NOK
    """
    # for substate 
    IDL      = "IDL"
    WARNING  = "WARNING"
    ERROR    = "ERROR"
    OK       = "OK"
    NOK      = "NOK"
    BUZY     = "BUZY"
    UNKNOWN  = "UNKNOWN"
    
    # for modes 
    STATIC = "STATIC",
    TRACKING = "TRACKING", 
    ENG = "ENG"
    
    
@_name_attr
class STATE:
    """ constant holder for device STATEs """
    NONE = 0
    NOTOP = 1
    OP = 2
    group = {
       NONE : GROUP.UNKNOWN,
       NOTOP : GROUP.NOK,
       OP    : GROUP.OK,
    }

@_name_attr
class SUBSTATE:
    """ constant holder for device SUBSTATEs """
    # SUBSTATE are specific to each device
    # :TODO: is their common SUBSTATE for each device ? NOTOP_NOTREADY =  100
    #  NOTOP_READY = 101  ?
    NONE = 0
    NOTOP_NOTREADY = 100 # not sure these number are the same accros devices
    NOTOP_READY    = 101
    NOTOP_ERROR    = 199
    
    OP_ERROR =299
    
    UNKNONW = 99999 # add a unknown substate for special cases
    group = {
        NONE                   : GROUP.UNKNOWN,
        NOTOP_NOTREADY         : GROUP.NOK,
        NOTOP_READY            : GROUP.NOK,
        NOTOP_ERROR            : GROUP.ERROR, 
        OP_ERROR               : GROUP.ERROR, 
    }
    
    
    
@_name_attr
class ERROR:
    """ constant holder for device ERRORs """
    OK	                   = 0
    HW_NOT_OP              = 1
    LOCAL                  = 2
    # etc...
    txt = {
    	OK:					  'OK',
    	HW_NOT_OP:			  'ERROR: TwinCAT not OP or CouplerState not mapped.',
    	LOCAL:				  'ERROR: Control not allowed. Motor in Local mode.',
        # etc ...
    }


class DeviceStatInterface(Interface):
    ERROR = ERROR # needed for error_txt alias 
    SUBSTATE = SUBSTATE # needed for substate_txt node alias
    STATE = STATE 
    
    @nodealiasproperty("is_operational", ["state"])
    def is_operational(self, state):
        return state == STATE.OP
    
    @nodealiasproperty("is_ready", ["substate"])
    def is_ready(self, substate):
        return substate == self.SUBSTATE.NOTOP_READY
    
    @nodealiasproperty("is_in_error", ["substate"])
    def is_in_error(self, substate):
        """ -> True is axis is sin error state:  NOP_ERROR or OP_ERROR """
        return substate in [self.SUBSTATE.NOTOP_ERROR, self.SUBSTATE.OP_ERROR]
    
    @nodealiasproperty("substate_txt", ["substate"])
    def substate_txt(self, substate):
        return self.SUBSTATE.txt.get(substate, "not registered substate")
    
    @nodealiasproperty("substate_group", ["substate"])
    def substate_group(self, substate):
        return self.SUBSTATE.group.get(substate, GROUP.UNKNOWN)
    
    
    
    @nodealiasproperty("state_txt", ["state"])
    def state_txt(self, state):
        return self.STATE.txt.get(state, "not registered state")
    
    @nodealiasproperty("state_group", ["state"])
    def state_group(self, state):
        return self.STATE.group.get(state, GROUP.UNKNOWN)
    
    @nodealiasproperty("error_txt", ["error_code"])
    def error_txt(self, error_code):
        return self.ERROR.txt.get(error_code, "No registered Error")
        
class Device:
    """ Base class for Device object 
    
    Most likely a Device will be created by :func:`Device.from_config` from a yml config file
    
    Args:
        key (str): device key (prefix of all nodes)
        config (dict): Dictionary descibing the configuration of the device. (as red from the yml file)
                       See the ESO ICF framework description. 
                       At minima the config must have 'address' keyword and 'prefix' keyword. 
        map (dict): Mapping dictionary of the device. If not given a default, according to device type 
                    is loadded. If no default is found a basic one is made with empty 'stat', 'cfg', 'rpc'
                    interface. 
        fits_prefix (str): string prefix for fits keywords
        **kwargs :  any other config parameters inside keyword, they will erase any similar item in the 
                   input config dictionary. 
    """
    STATE = STATE
    SUBSTATE = SUBSTATE
    ERROR = ERROR
    
    _cfg  = None
    _stat = None
    _rpc  = None
    _ua_client = None
    
    CfgInterface  =  Interface
    StatInterface =  DeviceStatInterface
    RpcInterface  =  RpcInterface


    def __init__(self, key, config=None, map=None, fits_prefix='', config_file='', **kwargs):
        
        
        self._config = {} if config is None else config 
        self._config.update(kwargs)
        
        self._key =  key or ''
        
        if map is None:
            try:
                map = load_default_map(self._config.get(K.TYPE , self.__class__.__name__))
            except ValueError:
                map = {} 
        self._map = map
                
        # what is called prefix in config is actually a name here
        self._fits_key = fjoin(fits_prefix, self._config.get(K.FITS_PREFIX, ''))
        
        self._config_file = config_file
        # get a client
        # use get_ua_client so we can use an already made connection
        self._init_client()
    
    def __repr__(self):
        return "<{} key='{}'>".format(self.__class__.__name__, self._key)
    
    
    def _init_client(self): 
        uaClient = get_ua_client(self.address)
        self._ua_client = uaClient
        
        
    @classmethod
    def from_config(cl, file_name, cfg_name=None, key=None, fits_prefix=''):
        """ read a device configuration file and return a :class:`Device` like object to handle it 
        
        Args:
            file_name (str): relative path to a configuration file 
                      The path is relative to one of the directory defined in the
                      $RESPATH environmnet variable
            cfg_name (str,None): The device name in the config file. 
                      If None take the first device of the configuration file
                    
                For instance in config file like
                    
                    :: 
                         
                        motor1:
                          type: Motor
                          interface: Softing
                          identifier: PLC1
                          etc... 
                
                'motor1' is the `cfg_name`
            
            key (str, optional): The device key. If not given cfg_name is taken
            fits_prefix (str, optional): The fits prefix string for this device
        """
        allconfig = io.load_config(file_name)
        if cfg_name is None:
            # get the first key 
            cfg_name = next(iter(allconfig))
        try:
            config = allconfig[cfg_name]
        except KeyError:
            raise ValueError("Device %r does not exists on device definition file %r"%(cfg_name, file_name))
        try:
            mapfile = config[K.MAPFILE]
        except KeyError:
            raise ValueError("Could not find mapfile in device definition %r at %r"%(cfg_name, file_name))
        map_d = io.load_map(mapfile)

        try:
            dtype = config[K.TYPE]
        except KeyError:
            raise ValueError("config file does not define device 'type'")

        try:
            map = map_d[dtype]
        except KeyError:
            raise ValueError("The associated map file does not contain type %r"%dtype)
        
        if key is None:
            key = cfg_name
            
        return cl(key, config, map, fits_prefix=fits_prefix, config_file=file_name)
    
    @property
    def config(self):
        return self._config
        
    @property
    def key(self):
        return self._key
    
    @property
    def prefix(self):
        return ksplit(self._key)[0]

    
    @property
    def name(self):
        return ksplit(self._key)[1]
        
    @property
    def fits_key(self):
        return self._fits_key
    
    @property
    def fits_name(self):
        return fsplit(self._fits_key)[1]

    @property
    def fits_prefix(self):
        return fsplit(self._fits_key)[0]
    
    @property
    def address(self):        
        address = self._config.get(K.ADDRESS, '')
        return host_mapping.get(address, address)  # can change address on the fly
    
    @property
    def ua_prefix(self):
        return self._config.get(K.PREFIX, '')
        
    @property
    def ua_namespace(self):
        return self._config.get(K.NAMESPACE, DEFAULT_NAME_SPACE)

    @property
    def dev_type(self):
        return self._config[K.TYPE]
    
    def connect(self, uaClient=None):
        """ Establish a client connection to OPC-UA server """
        connect_ua_client(self._ua_client, self)
        #self._ua_client.connect()

    def disconnect(self):
        """ disconnect the OPC-UA client """
        disconnect_ua_client(self._ua_client, self)
        # self._ua_client = None
        # return         
        # if self._ua_client is None:
        #     return
        # if self.is_connected():
        #     self._ua_client.disconnect()
            
    def is_connected(self):
        """ Return True if the current device is connected """
        # TODO: check the best way to check a connection from opcua
        if self._ua_client.uaclient and self._ua_client.uaclient._uasocket:
            t = self._ua_client.uaclient._uasocket._thread
            return t and t.is_alive()
        return False
    
    @property
    def map(self):
        """ map dictionary """
        return self._map
    
    stat = InterfaceProperty('stat', 'StatInterface')    
    cfg  = InterfaceProperty('cfg',   'CfgInterface')
    rpc  = InterfaceProperty('rpc',   'RpcInterface')
    
    def clear(self): 
        """ clear some cached values """ 
        for k,v in list(self.__dict__.items()):
            if isinstance(v, (Interface, RpcInterface)):
                v.clear()
                self.__dict__.pop(k)
    
    ## These RPC should be on all devices
    def init(self):
        """ init the device """
        self.rpc.rpcInit.rcall()

    def enable(self):
        """ enable the device """ 
        self.rpc.rpcEnable.rcall()

    def disable(self):
        """ disable the device """
        self.rpc.rpcDisable.rcall()

    def reset(self):
        """ reset the device """
        self.rpc.rpcReset.rcall()

    def get_error_txt(self, errcode):
        """ Get a text description of the given error code number """
        return self.ERROR.txt.get(errcode, 'UNKNOWN ERROR')
    
    def get_rpc_error_txt(self, rpc_errcode):
        """ Get a text description of the given rpc error code number """
        return self.RpcInterface.RPC_ERROR.txt.get(rpc_errcode, 'UNKNOWN RPC ERROR')
    
    def get_configuration(self, **kwargs):
        """ return a node/value pair dictionary ready to be uploaded 
        
        The node/value dictionary represent the device configuration. 
        This is directly use by :func:`Device.configure` method. 
        
        This is a generic configuration dictionary and may not work on all devices. 
        This method need to be updated for each device.   
        
        Args:
            **kwargs : name/value pairs pointing to cfg.name node
                      This allow to change configuration on the fly
                      without changing the config file.             
        
        ::
        
            >>> upload( dev.get_configuration() ) 
        """
        cfg_dict = {self.cfg.get_node(k):v for k,v in self._config.get(K.CTRL_CONFIG, {}).items()}
        cfg_dict.update({self.cfg.get_node(k):v for k,v in kwargs.items()})
        return cfg_dict
    
    def configure(self, **kwargs):
        """ Configure the whole device in the PLC according to what is defined in the config dictionary 
        
        Quick changes on configuration value can be done by keyword where keys must point to a .cfg.name 
        node. Note that the configuration (as written in file) is always loaded first before being 
        overwritten by **kwargs.  
        
        Args:
            **kwargs :  name/value pairs pointing to cfg.name node
                        This allow to quickly change configuration on the fly
                        without changing the config file.
                        Note that when running configure the configuration is always 
                          
        
        this is just:
        
        ::
        
           >>> upload( self.get_condifuration() ) 
        """
        # by default just copy the "ctrl_config" into cfg. This may not work for
        # all devices and should be customized  
        upload(self.get_configuration(**kwargs))
    
