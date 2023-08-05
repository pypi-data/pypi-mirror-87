from pydevmgr import Device, RpcError, GROUP


_enum = -1 
def _inc(i=None):
    """ number increment to use in frontend 
    
    _inc(0) # reset increment to 0 and return 0 
    _inc()  # increment and return incremented number 
    """
    global _enum
    _enum = _enum+1 if i is None else i
    return _enum

# TODO: change this by a real logging system 
error = print

class STYLE(GROUP):
    """ A collection of style IDs derived from GROUPs in pydevmgr + extra stuff """
    NORMAL  = "NORMAL"
    ODD     = "ODD"
    EVEN    = "EVEN"
    ERROR_TXT = "ERROR_TXT"
    OK_TXT =    "OK_TXT"
    
""" Associate STYLE IDs to qt stylSheet """
qt_style_loockup = {
    STYLE.NORMAL  : "background-color: white;",
    STYLE.IDL  : "background-color: white;",
    STYLE.WARNING : "background-color: #ff9966;",
    STYLE.ERROR   : "background-color: #cc3300;",
    STYLE.OK      : "background-color: #99cc33;",
    STYLE.NOK     : "background-color: #ff9966;",
    STYLE.BUZY    : "background-color: #ffcc00;",
    STYLE.UNKNOWN : "",
    STYLE.ODD     : "background-color: #E0E0E0;",
    STYLE.EVEN    : "background-color: #F8F8F8;",
    STYLE.ERROR_TXT : "color: #cc3300;",
    STYLE.OK_TXT : "color: black;",
}

def get_style(style):
    return qt_style_loockup.get(style, "")

""" Associate a state to a style """
state_style_loockup = {
   Device.STATE.NONE  : STYLE.UNKNOWN, 
   Device.STATE.OP    : STYLE.OK, 
   Device.STATE.NOTOP : STYLE.NOK,
}


def method_setup(combo, items):
    """ Does the same thing than combo_box.setItems 
    
    except that input is a list of (name, func, input_func) as for  method_switcher
    
    """
    output= []
    idx = combo.count()
    for item in items:
        if isinstance(item, str):
            if item == "---":
                combo.insertSeparator(idx)
                # inserting a separator increase the index so add a dummy action
                output.append(("", None, []))
                
            else:
                name = item
                item = (name, None, [])
                combo.addItem(name)
                output.append(item)
        else:
            name, _, _ = item
            combo.addItem(name)
            output.append(item)
        idx = combo.count()
    return output 

def method_caller(func, input_funcs, feedback=None):
    """ Build a method to togle a function 
    
    Args:
        func (callable): function to call
        input_funcs (list of callable): each member return an argument for the function
        feedbac: func with signature func(er, txt)
    
    Returns:
        method : a callable obect with signature func()
        
    """
    if feedback:        
        def call_method():
                      
            try:
                func(*(fi() for fi in input_funcs))
            except (RpcError,TypeError,ValueError) as e:
                feedback(True, str(e))
            else:
                feedback(False, '')
    else:
        def call_method():
            try:
                func(*(fi() for fi in input_funcs))
            except (RpcError,TypeError,ValueError) as e:
                error(str(e))    
    return  call_method
    
def method_switcher( func_inputs, feedback=None, reset=None):
    """ Build method that take an index number and trigger the associated method 
    
    
    Args:
        func_inputs: list of (func, inputs), inputs is alist of callable 
                     each member return an argument for the function
        feedbac: (optional): func with signature func(er,txt)
        reset (callable, optional): to execute after each call
    
    Returns:
        method : a callable obect with signature func(i)
        
    """
    if feedback:    
        def call_method(idx):
            _, func, input_funcs = func_inputs[idx]
            if func is None:
                return 
            
            try:
                func(*(fi() for fi in input_funcs))
            except (RpcError,TypeError,ValueError) as e:
                feedback(True, str(e))
            else:
                feedback(False, '')
            if reset: reset()
    else:
        def call_method(idx):
            func, input_funcs = func_inputs[idx]
            if func is None:
                return 
            try:
                func(*(fi() for fi in input_funcs))
            except (RpcError,TypeError,ValueError) as e:
                error(str(e))
            if reset: reset()
    
    return  call_method                           


_pydevmgr_widgets = {}
def record_widget(widget_type, dev_type, constructor):
    """ Record a new global widget 
    
    Args:
        widget_type (string): description of the widget like "ctrl"
        dev_type (:class:`Device`): A device class 
        constructor: A constructor for the widget  
    """
    _pydevmgr_widgets[(widget_type, dev_type)] = constructor

def get_widget_constructor(widget_type, dev_type):
    try:
        return _pydevmgr_widgets[(widget_type, dev_type)]
    except KeyError:
        raise ValueError("Unknown widget of type {} for a {}".format(widget_type, dev_type))

