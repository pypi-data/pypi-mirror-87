import os
import pkg_resources

pkg_name = 'pydevmgr_qt'

def find_ui(resource):
    if not pkg_resources.resource_exists(pkg_name, os.path.join('uis',resource)):
        raise IOError('coud not find ui file %r'%(resource))        
    return pkg_resources.resource_filename(pkg_name, os.path.join('uis',resource))   