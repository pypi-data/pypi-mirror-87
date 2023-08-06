from . import keys as K
from .device import Device, kjoin, fjoin, GROUP
from . import io
from .interface import NodeAlias, Interface, nodealiasproperty, ksplit, fsplit, fjoin
import os

warning = print # for now will see later

def setitem(obj,k,v):
    """ setitem(obj, k, v) -> obj[k] = v"""
    obj[k] = v

def open_manager(file_name, key='', extra_file=None):
    """ Create a :class:`Manager` object from its yaml configuration file 
    
    Args:
        file_name (str) : This is the relative path trought the yml file defining the manager. 
                The file shall be present inside one of the directories defined by the 
                $RESPATH environmnet variable.
        key (str, optional):  The key of the manager (which will be the prefix of all devices)
               If not given key will be the 'server_id' keyword has defined in the configuration file
        extra_file (str): This is the path to an extra yml file where some specific pydevmgr configuration 
               are writen. If not given an eventual FILE_NAME_extra.yml file will be load. 
               FILE_NAME_extra.yml must be on the same directory than FILE_NAME.yml
               So far in the _extra file is defined GUI configurations.
                 
    """
    return Manager.from_config(file_name, key=key, extra_file=extra_file)

def open_device(file_name, cfg_name=None, key=None, fits_prefix=''):
    """ read a device configuration file and return a :class:`Device` like object to handle it 
    
    Args:
        file_name (str): relative path to a configuration file 
                  The path is relative to one of the directory defined in the
                  $RESPATH environmnet variable
        cfg_name (str, None): The device name in the config file. 
                  If None the first device in the configuration is taken 
                
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
    if key is None:
        key = cfg_name
    
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
    try:
        cl = Manager.get_device_type(dtype)
    except ValueError:
        warning("The type %r is not implemented, %r will have a generic Device class"%(dtype, cfg_name))
        cl = Manager.Device
        
    return cl( key, config, map, fits_prefix=fits_prefix, config_file=file_name)  


## #######################################################
#
#   Some NodeAlias for the manager 
#   These are created in the stat attribute 
#

class SubstateNodeAlias(NodeAlias):
    SUBSTATE = Device.SUBSTATE
    def fget(self, *substates):
        if not substates: return self.SUBSTATE.UNKNOWN
        first = substates[0]
        if all( s==first for s in substates):
            return first 
        return self.SUBSTATE.UNKNOWN

class StateNodeAlias(NodeAlias):
    STATE = Device.STATE
    def fget(self, *states):
        if all( s==self.STATE.OP for s in states):
            return self.STATE.OP
        return self.STATE.NOTOP
        
class InitialisedNodeAlias(NodeAlias):    
    def fget(self, *init_flags):
        return all(f for f in init_flags)



##
# The stat manager for stat interface will be build of NodeAliases
#  !!!!!!!!!!!  
#      ManagerStatInterface must be initialised by Manager.stat property
#       Manager.stat should fill the NodeAlias(es) after devices list has been built
#  !!!!!!!!!!
class ManagerStatInterface(Interface):
    
    STATE = Device.STATE
    @nodealiasproperty("state_txt", ["state"])
    def state_txt(self, state):
        return self.STATE.txt.get(state, "not registered state")
    
    @nodealiasproperty("state_group", ["state"])
    def state_group(self, state):
        return self.STATE.group.get(state, GROUP.UNKNOWN)
    
        
class Manager:
    """ Manager object handling several devices 
    
    .. note::
    
        Most likely the Manager will be initialized by :func:`Manager.from_config` or its alias :func:`open_manager`
    
    If :func:`Manager.from_config` or :func:`open_manager` is used all the device prefixes will be
    the key of the device manager.  
    
    Args:
        key (str): the key (prefix of all devices) of the manager
                If None key is the 'server_id' defined inside the config dictionary
        devices (dic): name/:class:`Device` pair dictionary 
        fits_key (str, optional): the Fits keyword (if ever used) of the manager. 
                   
    
    """
    # yes this dictionary is intended to be set on the class
    __device_types__ = {}
    Device = Device # default device class
    
    StatInterface = ManagerStatInterface    
    _stat = None
    
    
    def __init__(self, key, devices, fits_key='', cmdtout=60000, extra=None):
        self._key = key 
        self._fits_key = fits_key
        self._devices = dict(devices)
        self._extra = {} if extra is None else extra
        
    def __getattr__(self,attr):
        try:
            return self.__dict__[attr]
        except KeyError:
            try:
                return self.get_device(attr)
            except ValueError:
                raise AttributeError("%r"%attr)
    
    def __dir__(self):
        lst = [d.name for d in self.devices()]
        for sub in self.__class__.__mro__:
            for k in sub.__dict__:
                if not k.startswith('_'):
                    lst.append(k)
        return lst 
    
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
    def extra(self):
        return self._extra
    
    @property
    def stat(self):
        if self._stat is None:
            # TODO add the parser functions dictionay
            self._stat = self.StatInterface(self.key, None, {}, '')
            
            self._stat.state = StateNodeAlias(kjoin(self.key,"state"), [d.stat.state for d in self.devices()])
            
        return self._stat
    
    
    @classmethod
    def from_config(cl, file_name, key=None, extra_file=None, fits_prefix=''):
        """ Create a :class:`Manager` object from its yaml configuration file 
        
        Args:
            file_name (str): This is the relative path trought the yml file defining the manager. 
                    The file shall be present inside one of the directories defined by the 
                    $RESPATH environmnet variable.
            key (str, optional):  The key of the manager (which will be the prefix of all devices)
                   If not given key will be the 'server_id' keyword has defined in the configuration file
            extra_file (str): This is the path to an extra yml file where some specific pydevmgr configuration 
                   are writen. If not given an eventual FILE_NAME_extra.yml file will be load. 
                   FILE_NAME_extra.yml must be on the same directory than FILE_NAME.yml
                   So far in the _extra file is defined GUI configurations.
                     
        """
        config = io.load_config(file_name)
        if extra_file:
            extra = io.load_config(extra_file)
        else:
            extra = io.load_extra_of(file_name)
        
        server_id = config[K.SERVER_ID]
        key = server_id if key is None else key
        server_config = config[server_id]
        
        fits_key = fjoin(fits_prefix, server_config.get(K.FITS_PREFIX, ''))
        device_names = server_config[K.DEVICES]
        devices = {}
        
        for device_name in device_names:
            try:
                dev_info = config[device_name]
            except KeyError:
                raise ValueError('device %r is not defined in the configuration file'%device_name)
            dev_type = dev_info[K.TYPE]
            cfg_gile = dev_info[K.CFGFILE]
            try:
                Devcl = cl.get_device_type(dev_type)
            except ValueError:
                warning("The type %r is not implemented, %r will have a generic Device class"%(dev_type, device_name))
                Devcl = cl.Device
                
            devices[device_name] = Devcl.from_config(cfg_gile, device_name, key=kjoin(key, device_name), fits_prefix=fits_key)
            
        return cl(key, devices, fits_key=fits_key, cmdtout=server_config.get('cmdtout',60000), extra=extra) 
        #return cl(key, config, config_file=file_name, extra=extra)
        
    @classmethod
    def record_new_device_type(cl, type_name, dev_cls):
        """ record a new device to the Manager class
        WARNING: the recorded or overwriten type will have effect on all new instance
                  of Manager
        """
        if not hasattr(dev_cls, 'from_config'):
            raise ValueError('class must have the `from_config` method')
        cl.__device_types__[type_name] = dev_cls
        
    
    @classmethod
    def get_device_type(cl, type_name):
        try:
            return cl.__device_types__[type_name]
        except KeyError:
            raise ValueError('Unknown device type %r '%type_name)
    
    def connect_all(self):
        """ Connect all the opc-ua client of the devices """
        for device in self._devices.values():
            device.connect()

    def disconnect_all(self):
        """ disconnect all the opc-ua client of the devices """
        for device in self._devices.values():
            device.disconnect()
            
    def get_device(self, name):
        """ get device matching the name Raise ValueError if not found """
        try:
            return self._devices[name]
        except KeyError:
            raise ValueError('Unknown device %r'%name)
    
    @property
    def devices(self):
        """ return the list of children :class:`Device` like object """
        return DeviceIterator(self._devices)
        #return list(self._devices.values())

    def device_names(self):
        """ return a list of child device names """
        return list(self._devices.keys())

    ## These RPC should be on all devices
    def init_all(self):
        """ Init all child devices """
        for device in self.devices():
            device.init()

    def enable_all(self):
        """ Enable all child devices """
        for device in self.devices():
            device.enable()

    def disable_all(self):
        """ Disable all child devices """
        for device in self.devices():
            device.disable()

    def reset_all(self):
        """ Reset all child devices """
        for device in self.devices():
            device.reset()
    
    def configure_all(self):
        """ Configure all child devices """
        for device in self.devices():
            device.configure()

class DeviceIterator:
    def __init__(self, devices):
        self._devices = devices
    
    def __iter__(self):
        return iter(self._devices.values())
    
    def __getitem__(self, item):
        return self._devices[item]
    
    def __call__(self):
        return list(self._devices.values())
    
    def names(self):
        return list(self._devices)
    
    