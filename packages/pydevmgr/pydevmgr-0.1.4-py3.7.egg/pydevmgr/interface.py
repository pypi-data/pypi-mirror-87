from opcua import Client as UaClient
from opcua import ua
from collections import defaultdict 
import weakref 

DEFAULT_NAME_SPACE = 4

#   ___  ____   ____      _   _   _
#  / _ \|  _ \ / ___|    | | | | / \
# | | | | |_) | |   _____| | | |/ _ \
# | |_| |  __/| |__|_____| |_| / ___ \
#  \___/|_|    \____|     \___/_/   \_\
#
DEBUG = False

def _name_attr(cl):
    names = {}
    txt = {}
    for subcl in cl.__mro__[::-1]:
        names.update( {n:k for k,n in subcl.__dict__.items() if not k.startswith('_') and isinstance(n, int)} )
        txt.update(getattr(cl, 'txt', {}))
    #cl.names = {n:k for k,n in cl.__dict__.items() if not k.startswith('_')}
    cl.names = names
    cl.txt = {**names, **txt}
    # for c,n in cl.names.items():
    #     setattr( cl, 'is_'+n, classmethod(lambda cl, v, _c_=c: v==_c_))
    return cl

_ua_clients = {}
_ua_clients_references = {}
def get_ua_client(uri):
    """ get an opc-ua client object for the given address create one if not exists """
    return UaClient(uri)
    # ## This was an attempt to share client with devices with same IP 
    # ## But this seems to be problematic
    # global _ua_clients
    # 
    # try:
    #     client = _ua_clients[uri]
    # except KeyError:
    #     if DEBUG:
    #         client = DebugClient(uri)
    #     else:
    #         client = UaClient(uri)
    #     _ua_clients[uri] = client
    # finally:
    #     _ua_clients_references.setdefault(client, {})
    # return client

def connect_ua_client(ua_client, obj):
    ua_client.connect()
    # return 
    # dc = _ua_clients_references.setdefault(ua_client, {})
    # if id(obj) not in dc:
    #     dc[id(obj)] = weakref.ref(obj)
    # ua_client.connect() # I think we can do it without problem
        
def disconnect_ua_client(ua_client, obj):
    ua_client.disconnect()
    return 
    # if not ua_client in _ua_clients_references:
    #     return
    # 
    # dc = _ua_clients_references.setdefault(ua_client, {})
    # try:
    #     dc.pop(id(obj))
    # except KeyError:
    #     pass
    # # do some clean up, remove objects that 
    # # does not exists anymore. It may be time consuming 
    # # but I am assuming that disconnection is not done in 
    # # real time.
    # for uid, ref in list(dc.items()):
    #     if ref() is None:
    #         dc.pop(uid)
    # 
    # if not len(dc):        
    #     ua_client.disconnect()
    #     _ua_clients_references.pop(ua_client)
    
    
def _ua_server_sid(client):
    return client.server_url.netloc
    
####
# Some dummy classes to work without any opc-ua server available
# This is just to debug part of the soft this is not a simulator
class DebugClient:
    log = staticmethod(print)
    def __init__(self, url):
        self.url = url
        self.values = {}
    def get_node(self, s):
        return DebugNode(s, self.values)
    def connect(self):
        self.log('connect {}'.format(self.url))
    def disconnect(self):
        self.log('disconnect {}'.format(self.url))

class DebugNode:
    log = staticmethod(print)
    def __init__(self, nodeid, values):
        self.nodeid = nodeid
        self.values = values
    def get_value(self):
        return self.values.setdefault(self.nodeid,0.0)
    def set_value(self, val):
        self.values[self.nodeid] = val
    def set_attribute(self, attrid, uaData):
        self.values[self.nodeid] = uaData.Value.Value
    def call_method(self, mid, *args):
        print( *((a, type(a)) for a in args) )
        return 0


def Int16(value):
    return ua.Variant(int(value), ua.VariantType.Int16) 
INT = Int16

def Int32(value):
    return ua.Variant(int(value), ua.VariantType.Int32)
DINT = Int32

def Int64(value):
    return ua.Variant(int(value), ua.VariantType.Int64)  
LINT = Int64

def UInt16(value):
    return ua.Variant(int(value), ua.VariantType.UInt16) 
UINT = UInt16

def UInt32(value):
    return ua.Variant(int(value), ua.VariantType.UInt32)
UDINT = UInt32

def UInt64(value):
    return ua.Variant(int(value), ua.VariantType.UInt64)        
ULINT = UInt64

def Float(value):
    return ua.Variant(int(value), ua.VariantType.Float)
REAL = Float

def Double(value):
    return ua.Variant(int(value), ua.VariantType.Double)
LREAL = Double
 




#  ___ _   _ _____ _____ ____  _____ _    ____ _____ ____
# |_ _| \ | |_   _| ____|  _ \|  ___/ \  / ___| ____/ ___|
#  | ||  \| | | | |  _| | |_) | |_ / _ \| |   |  _| \___ \
#  | || |\  | | | | |___|  _ <|  _/ ___ \ |___| |___ ___) |
# |___|_| \_| |_| |_____|_| \_\_|/_/   \_\____|_____|____/
#

def kjoin(*args):
    """ join key elements """
    return ".".join(a for a in args if a)

def fjoin(*args):
    """ join fits elements """
    return " ".join(a.strip() for a in args if a)

def ksplit(key):
    s, _, p = key[::-1].partition(".")
    return p[::-1], s[::-1]

def fsplit(key):
    s, _, p = key[::-1].partition(" ")
    return p[::-1], s[::-1]

def setitem(obj,k,v):
    """ setitem(obj, k, v) -> obj[k] = v"""
    obj[k] = v

class RpcError(RuntimeError):
    """ Raised when an rpc method is returning somethingelse than 0

        See rcall method of RpcNode
    """
    rpc_error = 0

## generic, default RPC_ERROR code

### ##############
# RPC error
# generic, default RPC_ERROR codes

@_name_attr
class RPC_ERROR:
    OK =  0
    NOT_OP =  -1
    NOT_NOTOP_READY =  -2
    NOT_NOTOP_NOTREADY = -3
    LOCAL =  -4
    # etc ...
    txt = {
        OK:					 'OK',
        NOT_OP:				 'Cannot control motor. Not in OP state.',
        NOT_NOTOP_READY:	 'Call failed. Not in NOTOP_READY.',
        NOT_NOTOP_NOTREADY:	 'Call failed. Not in NOTOP_NOTREADY/ERROR.',
        LOCAL:				 'RPC calls not allowed in Local mode.',
        # etc 
    }

def dummy(x):
    return x


class NodeAlias:
    """ NodeAlias mimic a real client Node. 
    
    The NodeAlias object does a little bit of computation to return a value with its `get()` method and 
    thanks to required input nodes.
     
    The NodeAlias cannot be use as such without implementing a `fget` method. This can be done by 
    implementing the fget method on the class or as an argument at init (same for the optionaly the fset method). 
    
    NodeAlias is an abstraction layer, it does not do anything complex but allows to simplify the programming 
    of GUIs for instance.  
    
    But NodeAlias object can be easely created with the @nodealias() decorator
    
    Args:
        key (str): Key of the node
        nodes (list): list of nodes necessary for the alias node. This is required because when the 
                     node alias is used in a Downloader object, the Downloader will automaticaly fetch 
                     those required nodes from server (or orher node alias). 
    Exemple: 
    
    ::
    
        >>> is_inpos_for_test = NodeAlias('is_inpos_for_test', [mgr.motor1.stat.pos_actual], fget=lambda pos: abs(pos-4.56)<0.01)
        >>> is_inpos_for_test.get()
    
    :: 
    
        @nodealias("is_all_standstill", [mgr.motor1.stat.substate, mgr.motor2.stat.substate])
        def is_all_standstill(m1_substate, m2_substate):
            return m1_substate == Motor.SUBSTATE.OP_STANDSTILL and m2_substate == Motor.SUBSTATE.OP_STANDSTILL
    
        >>> is_all_standstill.get()
        True
        
        >>> downloader = Downloader( [is_all_standstill] )
        >>> downloader.download()        
        >>> downloader.data
        {'fcs.motor1.substate': 100,
         'fcs.motor2.substate': 100,
         'is_all_standstill': False}
         
    In the exemple above one can see that the mgr.motor[12].stat.substate has been automatically added 
    to the nodes to be fetched from OPC-UA server(s). 
    
    Here is an exemple of customized NodeAlias
    
    ::
        import numpy as np 
        
        class MinMaxNode(NodeAlias):
            min = +np.inf
            max = -np.inf
            
            def fget(self, pos):
                self.min = min(pos, self.min)
                self.max = max(pos, self.max)
                return ( self.min , self.max )
            
            def reset(self):
                self.min = +np.inf
                self.max = -np.inf
                
        mot1_minmax = MinMaxNode( "minmax",  [mgr.motor1.stat.pos_actual])
                
    .. seealso::  
        :func:`nodealias`
        :func:`nodealiasproperty`
        :class:`NodeAlias`
        
    """
    
    def __init__(self, key, nodes, fget=None, fset=None):
        self._nodes = nodes
        self._key = key
        
        if fget:
            self.fget = fget
        if fset:
            self.fset = fset
    
    def __repr__(self):
        return "<{} key='{}'>".format(self.__class__.__name__, self._key)
    
    @property
    def key(self):
        return self._key
    
    @property
    def prefix(self):
        s,_,p = self.key[::-1].partition(".")
        return p[::-1]
    
    @property
    def name(self):
        s,_,p = self.key[::-1].partition(".")
        return s[::-1]
    
    @property
    def nodes(self):
        return self._nodes
        
    def get(self, data=None):
        """ get the node alias value from server or from data dictionary if given """
        if data is None:
            values = NodesReader(self._nodes).read()
        else:
            values = [data[n.key] for n in self._nodes]
        return self.fget(*values)
    
    def set(self, value, data=None):
        """ set the node alias value to server or to data dictionary if given """
        values = self.fset(value)
        if data is None:
            NodesWriter(dict(zip(self._nodes, values))).write()
        else:
            for n,v in zip(self._nodes, values):
                data[n] = v
    
    @staticmethod
    def fget(*args):
        raise NotImplementedError("Node alias get function")
    
    @staticmethod
    def fset(*args):
        raise NotImplementedError("Node alias set function")
        
class NodeAliasP(NodeAlias):
    """ Same as :class:`NodeAlias` exept it brings an object with it
    
    The attached object will be sent to the fget and fset method as first argument. 
    
    :class:`NodeAliasP` is returned by a :class:`NodeAliaseProperty`
    """
    def __init__(self, obj, key, nodes, fget=None, fset=None):
        self._obj = obj
        self._nodes = nodes
        
        if fget:
            self.fget = fget
        if fset:
            self.fset = fset
        self._key = key 
        
    def get(self, data=None):
        if data is None:
            values = NodesReader(self._nodes).read()
        else:
            #values = [data[n.key] for n in self._nodes]
            values = [data[n.key] for n in self._nodes]
        return self.fget(self._obj, *values)
    
    def set(self, value, data=None):
        values = self.fset(self._obj, value)
        if data is None:
            NodesWriter(dict(zip(self._nodes, values))).write()
        else:
            for n,v in zip(self._nodes, values):
                data[n] = v
    
class NodeAliasProperty:
    """ A Node Alias to be used inside a Node Interface object 
    
    This class will be mostly generated by the @nodealiasproperty() decorator. 
    The NodeAliasProperty object must be included in a class having the `get_node` method. 
     `get_node` will be used to fetch the node.
     
    Args:
        name (str): node name the key will be parent_key.name where parent_key is the host object key 
        node_names (lst): list of node names necessary for the nodeAlias. The real nodes will be fetch 
                from parent.get_node(node_name)
    
    Exemple:
    
    copy pasted from device definition:
    
    ::
    
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
     
            @nodealiasproperty("substate_txt", ["substate"])
            def substate_txt(self, substate):
                return self.SUBSTATE.txt.get(substate, "not registered substate")
    
    """
    def __init__(self, name, node_names, fget=None, fset=None):
        self.node_names = node_names
        self.fget = fget
        self.fset = fset
        self.name = name
    
    def __get__(self, obj, cls=None):
        try:
            node_alias = obj.__dict__[self.name]
        except KeyError:
            nodes = [obj.get_node(n) for n in self.node_names]
            node_alias = NodeAliasP(obj, kjoin(obj.key,self.name), nodes, fget=self.fget, fset=self.fset)
            # hopefully self.name shall be the same than the name in class definition 
            # otherwise side effects are expected 
            obj.__dict__[self.name] = node_alias
        else:
            print("BUG: nodealiaspropery of name %s have a different class Attributes")
        return node_alias
    
    def getter(self, func):
        """ decorator for the fget method """
        self.fget = func
        return self
    
    def setter(self, func):
        """ decorator for the fset method """
        self.fset = func
        return self 
    

def nodealias(key, nodes):
    """ A decorator to create a :class:`NodeAlias` object 
    
    Args:
        key (str): Key of the node
        nodes (list): list of nodes necessary for the alias node.
    
    Exemple: 
        
    :: 
    
        @nodealias("is_all_standstill", [mgr.motor1.stat.substate, mgr.motor2.stat.substate])
        def is_all_standstill(m1_substate, m2_substate):
            return m1_substate == Motor.SUBSTATE.OP_STANDSTILL and m2_substate == Motor.SUBSTATE.OP_STANDSTILL
    
        >>> is_all_standstill.get()
        True
        
        
    
    .. seealso::  
    
        :class:`NodeAlias`
    
    """
    alias = NodeAlias(key, nodes)
    def fget_setter(func):
        alias.fget = func
        return alias
    return fget_setter   

def nodealiasproperty(name, node_names):
    """ A :class:`NodeAliasProperty` decorator to be used inside a Node Interface object 
    
    The decorator must be included in a class with the `get_node` method. 
    `get_node` will be used to fetch the node.
     
    Args:
        name (str): node name the key will be parent_key.name where parent_key is the host object key 
        node_names (lst): list of node names necessary for the nodeAlias. The real nodes will be fetch 
                from parent.get_node(node_name)
    
    Exemple:
    
    copy pasted from device definition:
    
    ::
    
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
     
            @nodealiasproperty("substate_txt", ["substate"])
            def substate_txt(self, substate):
                return self.SUBSTATE.txt.get(substate, "not registered substate")
    
    """
    alias_property = NodeAliasProperty(name, node_names)
    return alias_property.getter          


class Node:
    """ Object representing a value node

    This is an interface representing one single value (node) in the OPC-UA server. 
    
    Node will be mostly used transparently inside :class:`Interface` object itself embeded inside 
    a :class:`pydevmgr.Device` object
        e.g. : in  `mgr.motor1.stat.pos_actual`
           
           mgr: is a :class:`pydevmgr.Manager`
           motor1: is a :class:`pydevmgr.Motor` extended from :class:`pydevmgr.Device`
           stat :  is a :class:`pydevmgr.Interface`  (group of nodes with a mapping dictionary)
           pos_actual : is a :class:`pydevmgr.Node`  
    
    Args:
        key (str): The string key representing the node in its context.
                   If key='a.b.c'  'a.b' is the `prefix` and 'c' the `name` of the node
        ua_node (opcua.Node): The opcua client node 
        vtype (callable, optional): A value parser for the set method (e.g. float, int, ...)
                This is handy for nodes representing a e.g. 16bits instegert on the server side. 
                
    Exemple:
    
    ::
      
        import pydevmgr
        import opcua
        
        client = opcua.client('url')
        current = pydevmgr.Node( 'current' client.get_node('ns=4;s=MAIN.lrCurrent') )
        substate =  pydevmgr.Node( 'substate', client.get_node('ns=4;s=MAIN.Motor1.stat.nSubstate'), vtype=pydevmgr.INT )
             
    """
    def __init__(self,  key, ua_node, vtype=None, sid=None):
        self._ua_node = ua_node
        self._key = key
        self._vtype = vtype
        self._sid = sid # server id identifier is used to group nodes together
        self._ua_variant_type = None
    
    def __repr__(self):
        return "<Node  key=%r>"%(self.key)
    
    @property
    def key(self):
        return self._key
    
    @property
    def prefix(self):
        return ksplit(self._key)[0]

    
    @property
    def name(self):
        return ksplit(self._key)[1]
        

    def get(self, data=None):
        """ get the server node value from server 
        
        If data is given the value is taken from this dictionary with its key instead of the server.
        """
        if data is None:
            return self._ua_node.get_value()
        else:
            return data[self.key]    
    
    def _parse_value_for_ua(self, value):
        
        if self._vtype:
            value = self._vtype(value)
        
        
        # this is a security net. In most of situation a python int will not work (LINT are rare in TwinCat FB)
        # this shall normally not be called and should be handled by vtype at device creation
        if isinstance(value, (int,)):
            # remove embiguity between int64 and int32, int16
            # we need to ask the variant_type on the server
            if self._ua_variant_type is None:
                self._ua_variant_type = self._ua_node.get_data_type_as_variant_type()
            datavalue = ua.DataValue(ua.Variant(value, self._ua_variant_type))
        elif isinstance(value, ua.DataValue):
            datavalue = value
        elif isinstance(value, ua.Variant):
            datavalue = ua.DataValue(value)
        else:
            datavalue = ua.DataValue(value)
        return datavalue    
        
    def set(self, value, data=None):
        """ set the server node value to server 
        
        If data is given the value is set to this dictionary with its key instead of the server.
        """
        ###
        #
        if data is None:
            datavalue = self._parse_value_for_ua(value)
            self._ua_node.set_attribute(ua.AttributeIds.Value, datavalue)
        else:
            data[self] = value
    
class NodeProperty:
    def __init__(self, name, ua_name, vtype=None):
        self.name = name
        self.ua_name = ua_name
        self.vtype = vtype
    
    def __get__(self, parent, cls=None):
        if parent is None:
            return self
        try:
            node =  parent.__dict__[self.name]
        except KeyError:    
            sid = "ns={};s={}".format(parent._ua_namespace, kjoin(parent._ua_prefix, self.ua_name))
            uaNode = parent._ua_client.get_node(sid)
            node = parent.Node(kjoin(parent.key, self.name),uaNode, vtype=self.vtype, sid=_ua_server_sid(parent._ua_client))
            parent.__dict__[self.name] = node
        return node
    
    def __set__(self, val):
        raise AttributeError('readonly attribute')          
    
class RpcNode:
    """ Object representing an OPC-UA Rpc method 

    It does the interce between a python method and the OPC-UA
    
    Both methods  :func:`RpcNode.call` and :func:`RpcNode.rcall` are calling the server Rpc. The first one is returning 
    an rpc_error code, the second return nothing but raise an :class:`RpcError` exception in case of error.
    
    In rare case user will use the RpcNode as it is automatically created from :class:`RpcInterface` containing 
    all the mapping.
    
    Args:
        key (str): shall be unic in its context  
        ua_node (opcua.Node): an opcua client node (see opcua library)
                   !! This is the node of the structure containing the method
                   
        ua_method_id(str): the ua method id
        atypes (None, lst, optional): a list of callable parser for the method. If given the number 
                of `atypes` shall match the number of arguments in the server Rpc Method. (no chec is done)
    
    Exemple:
        
    ::
        
        import opcua 
        from pydevmgr import RpcNode
        
        client = opcua.Client('..url..')
        move_abs = RpcNode('mot1.move_abs', client.get_node('ns=4;s=MAIN.Motor1'), '4:RPC_MoveAbs', atypes=(float, float))         
    
    """
    RPC_ERROR = RPC_ERROR

    def __init__(self, key, ua_node, ua_method_id, atypes=None):
        self._ua_node = ua_node
        self._ua_method_id = ua_method_id
        self._atypes = atypes
        self._key = key
    
    def __repr__(self):
        return "<RpcNode prefix=%r name=%r>"%(self.prefix, self.name)
    
    @property
    def key(self):
        return self._key
    
    @property
    def prefix(self):
        return ksplit(self._key)[0]

    
    @property
    def name(self):
        return ksplit(self._key)[1]
    
    def get_rpc_error_txt(self, rpc_error):
        """ get a txt description of the rpc_error code 
        
        Args:
            rpc_error (int): rpc error code  
        """
        return self.RPC_ERROR.txt.get(rpc_error,'Unregistered RPC error')
    
    def call(self, *args):
        """ Call the method and return what return the server 
        
        this shall return an integer rpc_error which shall be 0 if success
        """
        return self._ua_node.call_method(self._ua_method_id, *self._parse_args(args))

    def rcall(self, *args):
        """ Call the Rpc Method but raised an exception in case of an error code is returned """
        rpc_error = self.call(*args)
        if rpc_error:
            e = RpcError("RPC ({}): {}".format(rpc_error, self.get_rpc_error_txt(rpc_error)))
            e.rpc_error = rpc_error
            raise e
            
    def _parse_args(self, args):
        if self._atypes:
            return ( tpe(a) for a,tpe in zip(args, self._atypes) )
        return args

    def __call__(self, *args):
        self.rcall(*args)



class RpcProperty:
    def __init__(self, name, ua_name, atypes=None):
        self.name= name 
        self.ua_name, self.ua_method = ksplit(ua_name)
        self.atypes = atypes
    
    def __get__(self, parent, cls=None):
        if parent is None:
            return self
        try:
            node =  parent.__dict__[self.name]
        except KeyError:    
            sid = "ns={};s={}".format(parent._ua_namespace, kjoin(parent._ua_prefix, self.ua_name))
            mid = "{}:{}".format(parent._ua_namespace, self.ua_method)
            uaNode = parent._ua_client.get_node(sid)
            node = parent.RpcNode(kjoin(parent.key, self.name), uaNode, mid,  atypes=self.atypes)
            parent.__dict__[self.name] = node
        return node
    
    def __set__(self, val):
        raise AttributeError('readonly attribute')          

def getkey(obj):
    return obj.key

class NodesWriter:
    def __init__(self, node_values):
        self._dispatch, self._all_wv = _dispatch_node_to_write(dict(node_values))
    
    def write(self, altdata=None):
        _write_dispatch(self._dispatch, self._all_wv, altdata)
        
def _dispatch_node_to_write(nodes_values):
    disptach = {} # None is for aliases 
    all_wv = {}
    # Threat Aliases first and then the real client/server nodes
    for node, value in nodes_values.items():
        if not isinstance(node, Node):
            node.set(nodes_values)
    
    for node, value in nodes_values.items():
        if isinstance(node, Node):
            _add_node_to_dispatch_writer(disptach,  all_wv, node, value)
    return disptach, all_wv

def _add_node_to_dispatch_writer(disptach, all_wv, node, value):
    
    try:
        params = disptach[node._sid]
    except KeyError:
        params =  ua.WriteParameters()
        params.uaclient = node._ua_node.server
        params.NodesToWrite = []
        disptach[node._sid] = params
    
    wv = ua.WriteValue()
    wv.NodeId = node._ua_node.nodeid
    wv.AttributeId = ua.AttributeIds.Value
    wv.vparser= node._parse_value_for_ua
    wv.Value = wv.vparser(value)
    params.NodesToWrite.append(wv)
    all_wv[node.key] = wv

def _write_dispatch(dispatch, all_wv, altdata):
    if altdata:
        for k,v in altdata.items():
            wv = all_wv[k]
            wv.Value = wv.vparser(v)
    
    for params in  dispatch.values():
        result = params.uaclient.write(params)
        for r in result: r.check()

class NodesReader:
    def __init__(self, nodes):
        self._input_nodes = nodes # need to save to remenber the order
        self._dispatch, self._aliases =  _dispatch_node_reader(nodes)
    
    def _read_to(self, data, setfunc):
        _read_dispatch_to_data(data, self._dispatch, self._aliases, setfunc)    
    
    def read(self, data=None, setfunc=setitem):
        if data is None:
            data = {}
            self._read_to(data, setfunc)
            return [data[n.key] for n in self._input_nodes]
        
        self._read_to(data, setfunc)
        return None

            
def _dispatch_node_reader(nodes):
    disptach = {} # None is for aliases 
    aliases = []
    for node in nodes:
        _add_node_to_dispatch_reader(disptach, aliases, node) 
    return disptach, aliases

def _add_node_to_dispatch_reader(disptach, aliases, node):
    
    if not isinstance(node, Node):
        aliases.append( node )
        for n in getattr(node, "nodes", []):            
            _add_node_to_dispatch_reader(disptach,  aliases, n)
        return 
    
    try:
        params = disptach[node._sid]
    except KeyError:
        params =  ua.ReadParameters()
        params.uaclient = node._ua_node.server
        params.keys = list()
        disptach[node._sid] = params
        
    rv = ua.ReadValueId()
    rv.NodeId = node._ua_node.nodeid
    rv.AttributeId = ua.AttributeIds.Value
    params.NodesToRead.append(rv)
    params.keys.append(node.key)


def _read_dispatch_to_data(data, dispatch, aliases, setfunc):
    for sid, params in dispatch.items():
        
        result = params.uaclient.read(params)
        for key,r in zip(params.keys, result):
            r.StatusCode.check()
            setfunc(data, key, r.Value.Value)        
    
    # aliases are treated at the end, data should have all necessary real nodes for 
    # the alias 
    # We need to start from the last as Aliases at with lower index can depend 
    # of aliases with higher index
    flags = [False]*len(aliases)
    for i, alias in reversed(list(enumerate(aliases))):
        if not flags[i]:        
            setfunc(data, alias.key, alias.get(data))
            flags[i]= True
  


def getitem(d,k):
    return d[k]


def get_values(uaclient, nodes):
    """ get values of several nodes 
    
    All nodes shall be on the same server
    
    Args:
        uaclient : opcua.Client 
        nodes : list of :class:`Node`
    """
    params = ua.ReadParameters()
    for node in nodes:
        _add_node_to_rparams(params, node)
    result = uaclient.read(params)
    #result[0].StatusCode.check()
    for r in result:
        r.StatusCode.check()
    return [r.Value.Value for r in result]

def _add_node_to_rparams(params, node):
    if isinstance(node, NodeAlias):
        for n in node.nodes:
            _add_node_to_rparams(params, n)
        return 
    rv = ua.ReadValueId()
    rv.NodeId = node._ua_node.nodeid
    rv.AttributeId = ua.AttributeIds.Value
    params.NodesToRead.append(rv)



def set_values(uaclient, node_values):
    """ set values of several nodes 
    
    All nodes shall be on the same server
    
    Args:
        uaclient : opcua.Client 
        node_values : dictionary of :class:`Node`/value pairs 
    """
    # for node, value in node_values:
    #     node.set(value)
    # return 
    for node, value in node_values.items():
        if isinstance(node, NodeAlias):
            node.set(node_values)
    
    params = ua.WriteParameters()
    for node, value in node_values.items():
        if not isinstance(node, NodeAlias):
            _add_node_to_wparams(params, node, value)
    
    result = uaclient.write(params)
    for r in result: r.check()
    
def _add_node_to_wparams(params, node, value):
    attr = ua.WriteValue()
    attr.NodeId = node._ua_node.nodeid
    attr.AttributeId = ua.AttributeIds.Value
    
    datavalue = node._parse_value_for_ua(value)
    attr.Value = datavalue           
     
    params.NodesToWrite.append(attr)


class Interface:
    """ Interface between opc-ua nodes and pydevmgr set of :class:`Nodes` 
    
    Args:
        
        key (str): a unique key defining the interface. This is generally the same key as the host 
                  :class:`Device`. e.g. mgr.motor1.key ==  mgr.motor1.stat.key == mgr.motor1.cfg.key
        ua_client (opcua.Client): opcua client connected to some servers
        map (dict): a dictionnary of name/node_suffix pairs 
            Like:     
            
                ::
                  
                    {'velocity' :     'cfg.lrDefaultVelocity',
                     'max_pos' :      'cfg.lrMaxPosition',
                     'min_pos' :      'cfg.lrMinPosition',
                     'check_inpos' :  'cfg.bCheckInPos', 
                     # etc...
                     }
        ua_prefix (str): The prefix for the OPC-UA path like for instance 'MAIN.Motor1.stat'
        ua_namespace (int,str, optional): The ua name space default is 4
    """
    _ua_client = None
    _map = None
    _ua_prefix = None
    _prefix = None
    _name = None
    
    
    Node = Node
    __cashed_alias__ = False
    
    def __init__(self, key, ua_client, map, ua_prefix, ua_namespace=DEFAULT_NAME_SPACE):
        self._ua_client = ua_client
        self._map = map

        self._ua_prefix = ua_prefix
        self._key = key
        
        self._ua_namespace = ua_namespace


    def __getattr__(self, attr):
        try:
            return object.__getattribute__(self, attr)
        except AttributeError:
            try:
                return self.get_node(attr)
            except KeyError:
                raise AttributeError(attr)

    def __dir__(self):
        return ['get', 'set', 'gat_value_node'] + list(self._map.keys())
        
    @classmethod
    def _get_vtype(cl, key):
        """ look in class __annotations__ to find any parser for a given key """

        for subcl in cl.__mro__:
            try:
                return subcl.__annotations__[key]
            except (KeyError,AttributeError):
                continue
        return None
    
        
    @property
    def all_native_nodes(self):
        """ a list nodes of the interface """
        return [self.get_node(k) for k in self.map.keys()]
    
    @property
    def all_nodes(self):
        """ a list nodes of the interface """
        _ = self.all_native_nodes # make sure all native nodes are cashed 
        if not self.__cashed_alias__:
            for sub in self.__class__.__mro__:
                for k,v in sub.__dict__.items():
                    if isinstance(v, (NodeAliasProperty)):
                        getattr(self, k)
            self.__cashed_alias__ = True
        
        return [v for v in self.__dict__.values() if isinstance(v, (Node,NodeAlias))]
        #return [self.get_node(k) for k in self.map.keys()]
    
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
    def map(self):
        return self._map
        
    def _get_ua_id(self, name):
        """ return a node id of a given name in the python space """
        try:
            ua_name = self._map[name]
        except KeyError:
            raise KeyError('Unknown node %r'%name)
        return "ns={};s={}".format(self._ua_namespace, kjoin(self._ua_prefix, ua_name))
        
    def _get_ua_node(self, name):
        uaNode = self._ua_client.get_node(self._get_ua_id(name))
        return uaNode
    
    def clear(self):
        """ clear all cashed intermediate objects """
        for k,v in list(self.__dict__.items()):
            if isinstance(v, (Node, NodeAlias)):
                self.__dict__.pop(k)
        self.__cashed_alias__ = False
    
    def get_nodes(self, node_names=None):
        """ return a list of :class:`Node` from a list of names 
        
        if node_names is None all the nodes (inluding aliases) are return. 
        If one want only the "native" nodes use the ``.all_native_nodes`` property
        
        
        !!! Warning if a given name startwith '_' this method may return something which is not 
           a :class:`Node` or :class:`NodeAlias`. No check is done for performance raison.  
        """
        if node_names is None:
            return self.all_nodes
        return [self.get_node(n) for n in node_names]
    
    def get_node(self, name):
        """ Return a Node for the given key

        key must be on of the keys in the mapping file.
        
        !!! Warning if the given name startwith '_' this method may return something which is not 
           a :class:`Node`. No check is done for performance raison.  

        Exemple:
        
            > pos = motor1.stat.get_node('pos_actual')
            Is equivalent to
            > pos = motor1.stat.pos_actual
            > pos.get()
        """
        try:
            vNode = self.__dict__[name]
        except KeyError:
            try:
                uaNode = self._get_ua_node(name)
            
            except KeyError:
                # it can be an alias
                try:
                    vNode = object.__getattribute__(self, name)
                except AttributeError:
                    raise KeyError('Unknown node %r'%name)
            
            else:
                vNode = self.Node(kjoin(self.key, name), uaNode, vtype=self._get_vtype(name), sid=_ua_server_sid(self._ua_client))
                # cash the object inside __dict__
                self.__dict__[name] = vNode
                return vNode
        
        return vNode


class InterfaceProperty:
    def __init__(self, map_key, cls=Interface):
        self.map_key = map_key
        self.cls = cls
    
    def finalize(self, device, interface):
        pass
    
    def finalizer(self, func):
        self.finalize = func
        return self
    
    def __get__(self, device, cls=None):
        if device is None:
            return self
        try:
            interface = device.__dict__[self.map_key]
        except KeyError:
            if isinstance(self.cls, str):
                cls = getattr(device, self.cls)
            else:
                cls = self.cls
            
            interface = cls(device.key, device._ua_client, device.map.get(self.map_key, {}), device.ua_prefix, ua_namespace=device.ua_namespace)
            self.finalize(device, interface)
            device.__dict__[self.map_key] = interface
        return interface        

class RpcInterface:
    """ Interface between opc-ua nodes of rpc method and pydevmgr set of :class:`RpcNodes` 
    
    Args:
        
        key (str): a unique key defining the interface. This is generally the same key as the host 
                  :class:`Device`. e.g. mgr.motor1.key ==  mgr.motor1.rpc.key
                  key for rpc method interface is not as relevent as for :class:`Interface`
        ua_client (opcua.Client): opcua client connected to some servers
        map (dict): a dictionnary of name/rpc_node pairs 
            Like:     
            
                ::
                  
                    {   'rpcInit'    : 'RPC_Init',
                        'rpcEnable'  : 'RPC_Enable',
                        'rpcDisable' : 'RPC_Disable',
                    # etc ...
                    }
                    
        ua_prefix (str): The prefix for the OPC-UA path like for instance 'MAIN.Motor1'
        ua_namespace (int,str, optional): The ua name space default is 4
    """
    _ua_client = None
    _map = None
    _ua_prefix = None
    _prefix = None
    _name = None
    
    RpcNode = RpcNode
    RPC_ERROR = RPC_ERROR
    
    def __init__(self, key, ua_client, map, ua_prefix,  ua_namespace=DEFAULT_NAME_SPACE):
        self._ua_client = ua_client
        self._map = map

        self._ua_prefix = ua_prefix
        self._key = key
        
        self._ua_namespace = ua_namespace

    def __getattr__(self, attr):
        try:
            return object.__getattribute__(self, attr)
        except AttributeError:
            try:
                return self.get_method(attr)
            except KeyError:
                raise AttributeError(attr)
    
    
    @classmethod
    def _get_atypes(cl, key):
        """ look in class __annotations__ to find any parser for a given key """

        for subcl in cl.__mro__:
            try:
                return subcl.__annotations__[key]
            except (KeyError,AttributeError):
                continue
        return None
    
    def clear(self):
        """ clear all cashed data """
        for k,v in list(self.__dict__.items()):
            if isinstance(v, RpcNode):
                self.__dict__.pop(k)
                
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
    def map(self):
        return self._map

    def _get_ua_id(self):
        return "ns={};s={}".format(self._ua_namespace, self._ua_prefix)

    def _get_method_id(self, name):
        try:
            ua_name = self._map[name]
        except KeyError:
            raise KeyError('Unknown method %r'%name)
        return "{}:{}".format(self._ua_namespace, ua_name)


    def _get_ua_node(self):
        uaNode = self._ua_client.get_node(self._get_ua_id())
        return uaNode

    def get_method(self, name):
        """ get a rpc method object :class:`RpcNode`
        
        Args:
            name (str): name of the rpc method
        
        !!! Warning if the given name startwith '_' this method may return something which is not a :class:`RpcNode`. No check is done.    
        """
        try:
            m = self.__dict__[name]
        except KeyError:
            m = self.RpcNode( kjoin(self.key, name), self._get_ua_node(), self._get_method_id(name), atypes=self._get_atypes(name))
            self.__dict__[name] = m
        return m
