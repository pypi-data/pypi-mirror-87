from .thread import Thread
from collections import deque, namedtuple, OrderedDict 
from .interface import kjoin, nodealias
from .interface import Node, NodeAlias, NodesReader, NodesWriter
import time
from datetime import datetime, timedelta
import traceback
import sys
import itertools 
from copy import deepcopy

__all__ = ['wait', 'Waiter', 'get_utc', 'local_utc', 
           'local_time', 'FifoNodes', 'FifoOneNode', 
            'Downloader', 'Uploader', 'Player', 'Prefixed',
            'suffix_setter', 'setitem', 'download', 'upload', 'Measurer']


def get_local_time():
    return time.time()
    
# Add a local_time node alias 
local_time = nodealias("local_time", [])(get_local_time)

def get_utc(delta=0):
    """ return the string utc time ready to be used in some PLC application  
    
        .. note:: 
        
           this is the utctime of the current computer can be shifted from PLC time
           optional delta set a number of seconds to shift from the current computer utc time  
    
    A :class:`NodeAlias` can also be use to get string utc time and local_time to get the computer time 
    
    Args:
        delta: float, optional
              number of seconds to shift the utc from.
    """
    utc = datetime.utcnow()+timedelta(seconds=delta)   
    return datetime.isoformat( utc ).replace("T","-") 

local_utc = nodealias("local_utc", [])(get_utc)

class FifoOneNode(NodeAlias):
    """ This is an :class:`NodeAlias` returning at each get() a :class:`collections.deque` 
    
    This is specially usefull to create graphical scope of on device variable
    
    Args:
       node (:class:`Node`,:class:`NodeAlias`): 
              One single node used to feed the fifo 
       maxlen (int): maximum len of the fifo 
       suffix (string, optional): suffix added to the onput node key to build 
             the alias key default is '_fifo'
    
    Exemple:
        
        ::
        
            > pos_mot = FifoOneNode( mgr.motor1.stat.pos_actual, 1000)
            > pos_mot.get()                                                                                              
            deque([10.504918148932397])
            > pos_mot.get()                                                                                              
            deque([10.504918148932397, 11.704918148932798])
            > pos_mot.get()                                                                                              
            deque([10.504918148932397, 11.704918148932798, 12.75491814893315])
            etc ... 
        
    .. seealso::  
    
        :class:`FifoNodes` : fifo from several nodes
        :class:`NodeAlias`   
    """
    def __init__(self, node, maxlen, suffix="_fifo"):
        key = node.key+suffix
        self.fifo = deque([], maxlen)
        super(FifoOneNode, self).__init__(key, [node])
    
    def fget(self, value):
        self.fifo.append(value)
        return self.fifo
    
    def clear(self, maxlen=None):
        if maxlen is None:
            self.fifo.clear()
        else:            
            self.fifo = deque([], maxlen)

class FifoNodes(NodeAlias):
    """ This is an :class:`NodeAlias` returning at each get a :class:`collections.deque` 
    
    Specially handy for live plot and scope
    
    Args:
       key (string): alias node keyword 
       nodes (list of :class:`Node`,:class:`NodeAlias`): 
              List of nodes to get()  
       maxlen (int): maximum len of the fifo 
    
    Exemple:
        
    In this exxample `local_time` is a builtin node alias returning local time 
    The first motor is moving while the second standstill at 0.0
         
    ::
    
        > from pydevmgr import local_time 
        > nodes = [local_time, mgr.motor1.stat.pos_actual, mgr.motor2.stat.pos_actual]
        > f = FifoNodes( "mot_poses", nodes, 20)
        > f.get()
        deque([(1604931613.136023, 96.44508185106795, 0.0)])
        > f.get()
        deque([(1604931613.136023, 96.44508185106795, 0.0),
        (1604931614.258859, 95.32508185106808, 0.0)])
        > f.get()
        deque([(1604931613.136023, 96.44508185106795, 0.0),
        (1604931614.258859, 95.32508185106808, 0.0),
        (1604931615.451603, 94.13508185106821, 0.0)])
        
        
    """
    def __init__(self, key, nodes, maxlen):        
        super(FifoNodes, self).__init__(key, nodes)        
        self.fifo = deque([], maxlen)
                
    def fget(self, *values):
        self.fifo.append(values)
        return self.fifo
    
    def clear(self, maxlen=None):
        if maxlen is None:
            self.fifo.clear()
        else:
            self.maxlen = maxlen
            self.fifo = deque([], maxlen)
        

class Counter(NodeAlias):
    """ A simple counter NodeAlis 
    
    Args:
       key (str, optional): Node Alias key default is "counter"
       start (int, optional): Start number (first returned number) default is 0
       step (int, optional): counter increment step, default is 1
    """
    def __init__(self, key="counter", start=0, step=1):
        self.key = key
        self.counter = start        
        self.step 
    
    def fget(self):
        c = self.counter
        self.counter += self.step
        return c
    
    def reset(self, start=0):
        """ reset the counter to start value (default = 0)"""
        self.counter = start 
        

def setitem(d,k,v):
    d[k] = v

def download(nodes, data=None):
    """ read node values from servers in one call per server
    
    Args:
        nodes (iterable):
             Iterable of nodes, like [mgr.motor1.stat.pos_actual, mgr.motor2.stat.pos_actual]
        
        data (dict, optional):
             This is mostlikely a dictionary, must define a __setitem__ method
             If given the function return None and update data in place. 
             If data is None the function return a list of values 
             
        
    Returns:
       None, or list : download(nodes) -> return list of values 
                       download(nodes, data) -> return None but update the data dictionary
    
    Exemple:
    
    ::
        
        data = {n.key:n.get() for n in nodes}
    
    Is equivalent, but slower than 
    
    :: 
        
        data = {}
        download(nodes)
        
    The latest is much more efficient because only one call (per server) is done.
    
    data dictionary is optional, if not given values are returned by the function:
    
    ::
     
        pos, error = download([mgr.motor1.stat.pos_actual, mgr.motor1.stat.pos_error])
     
    
    """
    return NodesReader(nodes).read(data)

def upload(node_values):
    """ write node values to the servers
    
    Args:
        node_values (dict):
             Dictionary of node/value pairs like :
                e.g: { motor.cfg.velocity : 4.3 }
    
    .. note:: 
        
        The input dictionary has pairs of node/value and not node.key/value      
    """
    NodesWriter(node_values).write()    



def wait(node_or_func_list, logic="all_true", period=0.1, timeout=60, lag=0.0, data=None):
    """ wait until a list of function return True

    Args:
        node_or_func_list (iterable): an iterable of nodes of callable. 
                    wait will wait until all node.get and callable return True (by default)
                    
        logic (str, optional): 
              "all_true"  : stop waiting when all check function return True (default)
              "all_false" : stop waiting when all check function return False
              "any_true"  : stop waiting when one of the check function return True
              "any_false" : stop waiting when one of the check function return False
            
        period (float, optional): default is 0.1 second
            the sleep time in second in between checks
        timeout (float, optional): timeout in second, a RuntimeError is raised if conditions
                         are still false after timeout
        lag (float, optional): Add a flat time lag (in second) before starting to wait. 
                    This could be used to make sure that the last operation has been digested by server. 
                         
                    Bellow the lag is used to make sure that when ``wait`` starts the motor is moving
                          
                    ::
                             
                            >>> mgr.motor1.move_rel(1.0, 0.25)
                            >>> wait( [mgr.motor1.stat.is_standstill], lag=0.1 )
        
        data (None, dict, optional):  If given input nodes values are taken from the 
               data dictionary which is expected to be updated in someother place.

    Exemple:
        Wait until a motor initialised and an other custom function::

            > def camera_ready():
            >   # <- do stuff ->
            >   return True # if camera is ready

            > wait( [motor.is_initialised, camera_ready] )

        Or something like::
        
            > is_arrived = lambda : abs(motor.stat.pos_actual.get()-3.4)<0.01
            > wait( [is_arrived, camera_ready])

    """
    Waiter(node_or_func_list, logic=logic, period=period, timeout=timeout, data=data).wait(lag)

def _all_true(functions, node_get):
    """ all_true(lst, nodes) -> return True if all function and node in list return True """
    for func in functions:
        if not func():
            return False
    return all( node_get() )

def _all_false(functions, node_get):
    """ all_false(lst) -> return True if all function in the list return False """

    for func in functions:
        if func():
            return False
    return all( not v for v in node_get() )
    
def _any_true(functions, node_get):
    """ any_true(lst) -> return True if one of the function in the list return True """
    for func in functions:
        if func():
            return True
    return any( node_get() )

def _any_false(functions, node_get):
    """ any_false(lst) -> return True if one of the function in the list return False """
    for func in functions:
        if not func():
            return True
    return any( not v for v in node_get() )

""" Used in wait to define the logic applied """
_logic_loockup = {
    "all_true"  : _all_true, 
    "all_false" : _all_false, 
    "any_true"  : _any_true, 
    "any_false" : _any_false
}


class Waiter:   
    """ Object use to wait for some condition to be True 
    
    The only method of this object is :method:`Waiter.wait`
    
    Args:
        node_or_func_list (iterable): an iterable of nodes of callable. 
                    waiter.wait will wait until all node.get and callable return True (by default)
        logic (string, optional):
              "all_true"  : stop waiting when all check function return True (default)
              "all_false" : stop waiting when all check function return False
              "any_true"  : stop waiting when one of the check function return True
              "any_false" : stop waiting when one of the check function return False
            
        period : float, optional default is 0.1 second
            the sleep time in second in between checks
        timeout: float, optional second, default is 60
            if time since the call of the function exceed timeout an
            ValueError is raised.
            timeout is in second as well
        data (None, dict, optional):  If given input nodes values are taken from the 
               data dictionary which is expected to be updated in someother place.
        
    Exemple:
        
    ::
        
        >>> wait_moving = Waiter([motor.is_moving])
        >>> wait_moving.wait()
        
    wait return True and can be used as a trigger for a :class:`Download` object :
    
    :: 
            >>> data = {} 
            >>> pos_update = Downloader(data, [motor.stat.pos_actual], triger=wait_moving.wait)
            >>> t = Thread(target=pos_update.runner(0.5))
            >>> t.start()
        
    In the exemple above the thread will update the data dictionary 
    every 0.5 seconds with motor position only when the motor is moving. 
            
    Attributes:
        period (float): conditions are checks every period seconds
        timeout (float): timeout in second, a RuntimeError is raised if conditions
                         are still false after timeout.
    """
    def __init__(self, node_or_func_list, logic="all_true", period=0.1, timeout=60, data=None, stopper=lambda:None):        
        nodes = []
        functions = []
        for f in node_or_func_list:
            if isinstance(f, (Node, NodeAlias)):
                nodes.append(f)
            else:
                functions.append(f)
        
        self._functions = functions
            
        
        try:
            check = _logic_loockup[logic]
        except KeyError:
            raise ValueError("undefined logic %r must be one of %s"%(logic, ",".join(_logic_loockup.keys())))
    
        self._check = check
        
        if data is None:
            reader = NodesReader(nodes)
            node_get = reader.read
            
        else:
            def node_get():
                return [data[n.key] for n in nodes]
         
        self._node_get = node_get        
        self.period  = period
        self.timeout = timeout
        self.stopper = stopper
        
    def wait(self, lag=0.0):
        """ run the wait condition 
        
        Args:
            lag (float, optional): Add a flat time lag (in second) before starting to wait. 
                        This could be used to make sure that the last operation has been digested by server. 
                             
                        Bellow the lag is used to make sure that when ``wait`` starts the motor is moving
                              
                        ::
                                >>> waiter = Waiter([mgr.motor1.stat.is_standstill])
                                >>> mgr.motor1.move_rel(1.0, 0.25)
                                >>> waiter.wait( 0.1 )                
        """
        check     = self._check
        node_get  = self._node_get
        functions = self._functions 
        timeout   = self.timeout
        period    = self.period
        stopper   = self.stopper 
        s_time = time.time()
        if lag>0.0:
            time.sleep(lag)
            
        while not check(functions, node_get):
            stopper() # raise a SopIteration if needed to stop. The StopIteration shall be catched 
                      # at higher level like in Measure.run or Download.run  
            if (time.time()-s_time)>timeout:
                raise RuntimeError('wait timeout')
            time.sleep(period)
        
        return True
    
def getitem(d,k):
    return d[k]

class Uploader:
    """ An uploader object to upload data to the PLC 
    
    The values to upload is defined in a dictionary of node/value pairs. 
    
    Not sure their is a strong use case for this. Maybe if pydevmgr is used as server instead of client 
    
    Args:
        node_values (dict):
             Dictionary of node/value pairs like :
                e.g: { motor.cfg.velocity : 4.3 }
        callback (callable, optional): callback function after each upload
    
    Example:
        
    ::
    
        >>> values  = {mgr.motor1.velocity: 1.0, mgr.motor2.velocity: 2.0}
        >>> uploader = Uploader(values)
        >>> t = Thread(target=uploader.runner)
        >>> t.start()
        >>> uploader[mgr.motor1.velocity] = 1.4 # will be uploaded at next trhead cycle 
                
    .. seaalso::
    
       :func:`upload`:  equivalent to Uploader(node_values).upload() 
    """
    def __init__(self, node_values=None, callback=None):
        
        node_values = {} if node_values is None else node_values
        
        self.node_values = node_values 
        self.callback = callback
    
    def __has__(self, node):
        return node in self._node_values
        
    def upload(self):
        """ upload the linked node/value dictionaries """
        NodesWriter(self.node_values).write() 
        if self.callback:
            self.callback()
                  
    def run(self, period=1.0, stopsignal=lambda : False, sleepfunc=time.sleep):
        """ Run the upload infinitly or until stopsignal is True 
        
        Args:
            period (float, optional): period of each upload cycle
            stopsignal (callable, optional): A function called at each cycle, if True the loop is break
                       and run returns    
        """
        while not stopsignal():
            s_time = time.time()
            self.upload()
            sleepfunc( max( period-(time.time()-s_time), 0))
    
    def runner(self, period=1.0, stopsignal=lambda : False, sleepfunc=time.sleep): 
        """ return a function to updload 
        
        this is designed in particular to be used in a target Thread
        
        Args:
            period (float, optional): period of each upload cycle
            stopsignal (callable, optional): A function called at each cycle, if True the loop is break
                       and run returns
        
        Example:
            
            ::
                > values  = {mgr.motor1.velocity: 1.0, mgr.motor2.velocity: 2.0}
                > uploader = Uploader(values)
                > t = Thread(target=uploader.runner)
                > t.start()
                > values[mgr.motor1.velocity] = 1.2 # will be updated at next thread cycle
                               
        """           
        def run_func():
            self.run( period=period, sleepfunc=sleepfunc, stopsignal=stopsignal)
        return run_func
    
        
def suffix_setter(suffix, setfunc=setitem):
    def suffixsetfunc(obj, key, value):
        key = key.replace(suffix,'').strip('.') if key.startswith(suffix) else key
        setfunc(obj, key, value)
    return suffixsetfunc


def _dummy_callback(data):
    pass
def _dummy_trigger():
    return True


class Player:
    """ A callable object which can be used in conjonction with Downloader, Uploader 

    > p = Player()
    > d = {}
    > u = Downloader(d, [motor1.stat.pos_actual, motor1.stat.pos_error], trigger=p.wait)
    > t = Thread(target=u.runner(1.0, stopsignal=p.is_stopped))
    > t.start() 
    
    > p.pause() # pause the update of the dictionary
    > p.play()  # restart a paused update
    > p.stop()  # stop the thread

    """
    def __init__(self, period=0.1):
        self._running = True
        self._killed = False
        self._period = period
        
    def __call__(self):
        if self._killed:
            raise StopIteration('')
        return self._running
        
    def play(self):
        self._running = True
        
    def stop(self):
        self._killed = True
        
    def pause(self):
        self._running = False
    
    def is_running(self):
        return self._running
    
    def is_paused(self):
        return not self._killed and not self._running
    
    def wait(self):
        while True:
            if self.is_running():
                return True
            time.sleep(self._period) 
    
    def is_stopped(self):
        return self._killed
    
class Downloader:
    """ object dedicated to download nodes, feed data and run some callback 

    An application can request nodes to be downloaded and callback to be executed after each 
    success download or each failures. 
    
    Args:    
        nodes (iterable of node): An initial, always download, list of nodes 
        data (dict, optional): a dictionary to store the data. If not given, one is created and
                              accessible through the .data attribute
        callback (callable, optional): one single function with signature f(data), if given always 
                                      called after successful download. 
        trigger (callable, optional): a function taking no argument and should return True or False 
                                      If given the "download" if executed only one f() return True. 
                                      Can be used if the download object is running in a thread for instance.
    
    Exemple: 
    
        A dumy exemple, replace the print_pos by a GUI interface for instance:
        
        ::
           
            def print_pos(data):
                "An application"
                print("Position :",  data['pos_actual'], data['pos_error'] )
            
            >>> downloader = Downloader()
            >>> token = download.new_connection()
            >>> downloader.add_node(token, tins.motor1.stat.pos_actual, tins.motor1.stat.pos_error )
            >>> downloader.add_callback(token, print_pos)
            >>> downloader.download() 
            Position : 3.45 0.003
            >>> downloader.data
            {
              'fcs.motor1.pos_actual' : 3.45, 
              'fcs.motor1.pos_error' :  0.003, 
            }
            >>> downloader.disconnect(token) # disconnect the print_pos function and remove 
                                             # the pos_actual, pos_error node from the list of nodes
                                             # to download 
                                     
    """
    def __init__(self,  nodes=None,  data=None, setfunc=setitem, callback=None,
                        trigger=None):
        self._data = {} if data is None else data
        
        nodes = set() if nodes is None else set(nodes)
        callbacks = set()
        failure_callbacks = set() 
        
        
        if callback is None:
            callback = _dummy_callback
        if trigger is None:
            trigger =  _dummy_trigger
        
        self._callback = callback
        self._trigger = trigger
        
        self._dict_nodes = OrderedDict([(None,nodes)])
        self._dict_callbacks = OrderedDict([(None,callbacks)])
        self._dict_failure_callbacks = OrderedDict([(None,failure_callbacks)])
        
        self.setfunc = setfunc
        
        self.trigger = trigger
        self._next_token = 1
        
        self._rebuild_nodes()
        self._rebuild_callbacks()
        self._rebuild_failure_callbacks()
    
    def __has__(self, node):
        return node in self._nodes
    
    @property
    def data(self):
        return self._data
    
    def _rebuild_nodes(self):
        nodes = set()
        for nds in self._dict_nodes.values():
            nodes.update(nds)
        self._nodes = nodes
        self._to_read = NodesReader(nodes)

    def _rebuild_callbacks(self):
        callbacks = set()
        for clbc in self._dict_callbacks.values():
            callbacks.update(clbc)
        self._callbacks = callbacks
    
    def _rebuild_failure_callbacks(self):
        callbacks = set()
        for clbc in self._dict_failure_callbacks.values():
            callbacks.update(clbc)
        self._failure_callbacks = callbacks
    
    def new_connection(self):
        """ add a new app connection 
        
        Return:
           A token, the token and type itself is not relevant, it is just a unique ID to be used in 
                    add_node, add_callback, add_failure_callback, and disconnect methods 
        """
        token = id(self), self._next_token
        self._dict_nodes[token] = set()
        self._dict_callbacks[token] = set()
        self._dict_failure_callbacks[token] = set()
        
        self._next_token += 1
        # self._rebuild_nodes()
        # self._rebuild_callbacks()
        # self._rebuild_failure_callbacks()
        return token
    
    def disconnect(self, token):
        """ Disconnect the App with the given token 
        
        All the nodes used by the app (and not by other connected app) will be removed from the 
        download queue of nodes.
         
        Args:
            token : a Token returned by :func:`Downloader.new_connection`
        """
        if token is None:
            return 
        
        try:
            self._dict_nodes.pop(token)
            self._dict_callbacks.pop(token)
            self._dict_failure_callbacks.pop(token)
        except KeyError:
            pass
        
        self._rebuild_nodes()
        self._rebuild_callbacks()
        self._rebuild_failure_callbacks()
    
    def add_node(self, token, *nodes):
        """ Register nodes to be downloaded for an iddentified app
        
        Args:
            token: a Token returned by :func:`Downloader.new_connection`
            *nodes :  nodes to be added to the download queue, associated to the app
        """   
        self._dict_nodes[token].update(nodes)
        self._rebuild_nodes()
    
    def add_callback(self, token, *callbacks):   
        """ Register callbacks to be executed after each download 
        
        The callback must have the signature f(data)
        
        Args:
            token: a Token returned by :func:`Downloader.new_connection`
            *callbacks :  callbacks to be added to the queue of callbacks, associated to the app
        
        """ 
        self._dict_callbacks[token].update(callbacks)
        self._rebuild_callbacks()
    
    def add_failure_callback(self, token, *callbacks):  
        """ Add one or several callbacks to be executed when a download failed 
        
        The callbacks must have the signature f(e) with e the error grabbed
        
        Args:
            token: a Token returned by :func:`Downloader.new_connection`
            *callbacks :  callbacks to be added to the queue of failure callbacks, associated to the app
        
        """ 
        self._dict_failure_callbacks[token].update(callbacks)
        self._rebuild_failure_callbacks()
    
    def run(self, period=1.0, stopsignal=lambda : False, sleepfunc=time.sleep):
        """ run indefinitely or when stopsignal return True the download 
        
        Args:
            period (float, optional): period between downloads in second
            stopsignal (callable, optional): a function returning True to stop the loop or False to continue
            
        """
        try:
            while not stopsignal():
                s_time = time.time()
                self.download()
                sleepfunc( max( period-(time.time()-s_time), 0))
        except StopIteration: # any downloader call back can send a StopIteration to stop the runner 
            return 
            
    def runner(self, period=1.0, stopsignal=lambda : False, sleepfunc=time.sleep): 
        """ Create a function to run the download in a loop 
        
        It can be the input of a Thread. 
        
        Args:
            period (float, optional): period between downloads in second
            stopsignal (callable, optional): a function returning True to stop the loop or False to continue
        
        Exemple:
            
            >>> downloader = Downloader([mgr.motor1.substate, mgr.motor1.pos_actual])
            >>> t = Thread( target = downloader.runner(period=0.1) )
            >>> t.start()
            
        """       
        def run_func():
            self.run(period=period, sleepfunc=sleepfunc, stopsignal=stopsignal)
        return run_func
    
    def download(self):
        """ Execute a download 
        
        Each nodes on the queue are queried on the OPC-UA server and the .data dictionary is updated
        from new values.
        
        """
        if not self.trigger(): return 
        
        try:
            self._to_read.read(self._data, setfunc=self.setfunc)
        except Exception as e:
            if self._failure_callbacks:
                for func in self._failure_callbacks:
                    func(e)
            else:
                raise e            
        else:
            self._callback(self._data)
            for func in self._callbacks:
                func(self._data)
    
    def get_data(self, prefix=''):
        """ Return a readonly view of the data 
        
        If prefix is given the return object will be limited to items with key
        matching the prefix.  
        
        Args:
           prefix (str, optional): limit the data viewer to a given prefix
        
        Exemple:
            
            ::
                
                > downloader = Downloader([mgr.motor1.substate, mgr.motor2.substate])
                > downloader.download()
                > m1 = downloader.get_data("motor1")
                > m1['pos_actual']
                3.9898
            
        """
        return Prefixed(self._data, prefix)        
    
    def clean_data(self):
        """ Remove to the .data dictionary all keys/value pairs corresponding to nodes not in the queue
        
        """
        node_keys = [n.key for n in self._nodes]
        d = self.data
        for k in list(d):
            if not k in node_keys:
                d.pop(k, None)
            
class Prefixed:
    """ this is a view of a dictionary wit prefixed keys 
    
    d = {"motor1.pos_actual" : 1.5, 
         "motor1.pos_error" : 0.002,
         
         "motor2.pos_actual" : 2.3, 
         "motor2.pos_error" : 0.001}
         
    > dp = Prefixed(d, "motor1") # without the dot
    > dp['pos_actual']
    1.5 
    
    This can be handy when one have to parse for instance a generic "motor" 
    dictionary that should work with any motors.
    
    .. note::
       
       doing dp['pos_actual'] is quite fast has only a prefix is added on the key
            however an iteration on Prefixed dictionary can be long if the root dictionary 
            is large as all keys of the root dictionary have to be checked for prefix.
            It is expected that these Prefixed dictionary will be used mostly as set/get item
    
    .. seealso::  
    
        :func:`download`
        :class:`Downloader`             
    """
    _prefix = ""
    _data = None
    
    def __init__(self, data, prefix):
        self._prefix = prefix
        self._data = data
    
    def __getitem__(self, item):
        return self._data[kjoin(self._prefix, item)]
    
    def __setitem__(self, item, value):
        self._data[kjoin(self._prefix, item)] = value
    
    def __delitem__(self, item):
        del self._data[kjoin(self._prefix, item)]
    
    def __getattr__(self, attr):
        return self._data[kjoin(self._prefix, attr)]
    
    def __has__(self, item):
        return kjoin(self._prefix, item) in self._data 
    
    def update(self, __d__={}, **kwargs):
        for k,v in dict(__d__, **kwargs).iteritems():
            self._data[kjoin(self._prefix, k)] = v
    
    def pop(self, item):
        return self._data.pop(kjoin(self._prefix, item))
    
    def popitem(self, item):
        return self._data.popitem(kjoin(self._prefix, item))
    
    def keys(self):
        """ D.keys() ->iterable on D's root keys with matching prefix
        
        Shall be avoided to use in a :class:`Prefixed` object
        """
        if not self._prefix : 
            for k in self._data.keys():
                yield k 
            return 
        
        pref = self._prefix+"."
        lp = len(pref)
        for k in self._data.keys():
            if isinstance(k, str) and k.startswith(pref):
                yield k[lp:]
    
    def items(self):
        """D.items() -> iterable on D's root items with matching prefix
        
        Shall be avoided to use in a :class:`Prefixed` object
        """
        if not self._prefix : 
            for k,v in self._data.items():
                yield k , v    
            return 
            
        pref = self._prefix+"."
        lp = len(pref)
        for k, v in self._data.items():
            if isinstance(k, str) and k.startswith(pref):
                yield k[lp:], v
    
    def values(self):
        """D.values() -> iterable on D's root  values with matching prefix
        
        Shall be avoided to use in a :class:`Prefixed` object
        """
        if not self._prefix : 
            for v in self._data.values():
                yield v    
            return 
                
        pref = self._prefix+"."
        for k, v in self._data.items():
            if isinstance(k, str) and k.startswith(pref):
                yield v
    
    def clear(self):
        """ D.clear() -> None.  Remove all items from D root with matching prefix
        
        Shall be avoided to use in a :class:`Prefixed` object
        """
        if not self._prefix:
            self._data.clear()
            return 
        
        pref = self._prefix+"."
        for k, v in list(self._data.items()):
            if isinstance(k, str) and k.startswith(pref):
                self._data.pop(k)
    
class Measurer:
    """ A base class tool to take sequence of measurements 
    
    The class does not do that much but offer a structure for measurements  
    
    
    
    Args:
        nodes (iterable): a list of nodes          
        measurements (list, optional):  This is the output list of measurements. 
                !! warning the list is cleared int the default init function
        data (dict, optional): If given the measurement are taken from this data. This is only used when 
                data is fed in an other process. 
                
                
                
    Exemple:
       
       Take measurement of motor position after a sequence of movement. 
       
       class MeasureMotorPos(Measurer):
            def __init__(self, motor, file):
                self.motor = motor
                self.file = file
                self.f = None        
                self.counter = 0 
                
                super(Measurer, self).__init__( [motor.stat.pos_actual, motor.stat.pos_error] )
            
            def init(self): 
                self.measurements.clear()           
                self.counter = 0    
                self.f = open(self.file)
                self.f.write( "#pos_target velocity pos pos_error image\n")
               
            def before(self, pos_vel):
               self.motor.move_rel(*pos_vel)
               wait( [self.motor.stat.is_standstill], lag=0.1 )
              
            def after(self, pos_vel, data):
                # Do something, for instance take an image from a camera
                time.sleep(0.2)
                self.counter += 1 
                img_file = "image_%03d.tiff"%self.counter
                # image = take_image_of_my_lab_cam()
                # save_image(image, img_file)
                data['image'] = img_file
            
            def end(self):
                pass
                     
                
               
               
    
    """
    def __init__(self, nodes, measurements=None,  data=None):    
        
        self.last_data  = {}
        self.measurements = [] if measurements is None else measurements        
        self.data = data
        self.nodes = nodes 
        self.aborded = False
    
    def stopper(self):
        """ A stop function which may raise a SoptIteration to stop the loop """
        pass
    
    def before(self, arg):
        """ Action to be executed before measurements. Must be defined by user """
        pass
    
    def after(self, arg, data):
        """ Action to be executed after measurements. Must be defined by user """
        pass
        
    def init(self):
        """ called when a sequence of measurements is started. Must be defined by user 
        
        Buy default this just clear the measurements list 
        """
        self.measurements.clear()
        
    def end(self):
        """ end a sequence of measurements, must be defined by user """
        pass
    
    def measure(self, arg):
        
        self.before(arg)
        
        last_data = {}
        
        if self.data:
            last_data = {n.key:self.data[n.key] for n in self.nodes}
        else:
            last_data = {}
            download(self.nodes, last_data)
            
        self.after(arg, last_data)
        self.measurements.append(last_data)    
        return last_data
    
    def run(self, args, delay=0.01):
        self.init()
        self.aborded = False
        try:
            for arg in args:
                self.measure(arg)
                time.sleep(delay)
        except StopIteration:
            self.aborded = True
            self.end()
        else:
            self.end() 
        return self.measurements
    
                
            
        
        
