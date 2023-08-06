import yaml
import os
import pkg_resources

RESPATH = 'RESPATH'
pkg_name = 'pydevmgr'

def read_map(file):
    with open(file) as f:
        return yaml.load(f.read(), Loader=yaml.CLoader)

def read_config(file):    
    with open(file) as f:
        return yaml.load(f.read(), Loader=yaml.CLoader)

def load_config(file_name):
    return read_config(find_config(file_name))

def load_extra_of(file_name):
    
    root, ext = os.path.splitext(find_config(file_name))
    
    
    file_name = os.path.join(root+"_extra"+ext)
    if not os.path.exists(file_name):
        return None
    return read_config(file_name)

def load_map(file_name):
    return read_map(find_config(file_name))

def find_config(file_name):
    path_list = os.environ.get(RESPATH, '.').split(':')
    for directory in path_list[::-1]:
        path = os.path.join(directory, file_name)
        if os.path.exists(path):
            return  path
    raise ValueError('coud not find config file %r in any of %s'%(file_name, path_list))

def find_map(dev_type):
    """ locate the map file from the pydevmgr installation and return the absolute path 

    
    Args:
        dev_type (str):  Device type as 'Motor' the map file shall be found as mapMotor.yml inside 
        the package resource directories
    """
    resource = 'map'+dev_type.capitalize()+".yml"
    if not pkg_resources.resource_exists(pkg_name, os.path.join('resources',resource)):
        raise IOError('coud not find map file of device %r from pydevmgr package'%(dev_type))        
    return pkg_resources.resource_filename(pkg_name, os.path.join('resources',resource))

_default_map_cash = {}
def load_default_map(dev_type):
    """ load a map file according to a device type 
    
    The map file is a default one comming from the package
    
    Args: 
        dev_type (str): Device type as 'Motor' the map file shall be found as mapMotor.yml inside 
        the package resource directories (see :func:`find_map`)
    Returns:
       
       map:  A dictionary
       
    Raises:
       
       ValueError: if no default map file exists
    """
    try:
        map =  _default_map_cash[dev_type]
    except KeyError:
        map_file = find_map(dev_type)
        map = read_config(map_file)
        _default_map_cash[dev_type] = map
    return map
        
        
def find_template(dev_type):
    """ locate a template file from the pydevmgr installation and return the absolute path 
    
    templates rendered by jinja2 
    
    Args:
        dev_type (str):  Device type as 'Motor' the template file shall be found as templateMotor.yml inside 
        the package resource directories
    """
    
    resource = 'template'+dev_type.capitalize()+".yml"
    if not pkg_resources.resource_exists(pkg_name, os.path.join('resources',resource)):
        raise IOError('coud not find template file of device %r from pydevmgr package'%(dev_type))        
    return pkg_resources.resource_filename(pkg_name, os.path.join('resources',resource))    
    