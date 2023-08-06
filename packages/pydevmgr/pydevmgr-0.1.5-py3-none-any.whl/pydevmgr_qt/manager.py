from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QVBoxLayout, QMainWindow
from PyQt5.QtCore import Qt

from .generic import get_widget_constructor, STYLE, get_style 
from .io import find_ui
from .basic import BaseCtrl 

from pydevmgr.device import STATE
from pydevmgr import Prefixed


# TODO change the warning function to something else
warning = print




class ManagerDevices(QtWidgets.QWidget):
    _did_failed = False
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUI()
        self.devices = {}
        self.connection = None
        self.check_status = {}
        self.dev_widgets = []
        
    def initUI(self):
        uic.loadUi(find_ui('manager_main.ui'), self)
    
    def update_failure(self, er):
        """ executed when the Downloader failed. """
        self.setEnabled(False)
        self._did_failed = True    
    
    def link_failure(self):
        """ link a failure callback to the current connection """
        ## diconnect the downloader 
        if self.connection is None:
            raise ValueError("cannot link failure, widget is not connected")
        downloader, token = self.connection
        downloader.add_failure_callback(token, self.update_failure)
    
    
    
    def update_manager(self, data, mgr):
        if self._did_failed:
            self.setEnabled(True)
            self._did_failed = False
        
        state = data['state']
        
        self.state.setText("{}: {}".format(state, data['state_txt']))
        self.state.setStyleSheet(get_style(data['state_group']))
        
        
        for dev_widget in self.dev_widgets:
            if hasattr(dev_widget, "check"):
                s = self.check_status.get(dev_widget.device_key, True)
                if s != dev_widget.check.isChecked():
                    dev_widget.check.setChecked(s)
                
    def link_device(self, downloader, manager):
        
        if self.connection:
            previous_downloader, token = self.connection
            previous_downloader.disconnect(token)
        ## create a new connection 
        token = downloader.new_connection()
        self.connection = (downloader, token)
        
        
        try:
            self.state_action.currentIndexChanged.disconnect()
            self.layout_selector.disconnect()
            self.check_all.disconnect()
        except TypeError:
            pass
        
        self.state_action.clear()
        self.state_action.addItems(['', "INIT", "ENABLE", "DISABLE", "RESET"])
        self.state.setText("UNKNOWN")
        
        self.layout_selector.clear()

        self.name.setText( manager.key )

        # add the necessary nodes to the downloader
        downloader.add_node(token, manager.stat.state, manager.stat.state_txt, manager.stat.state_group)
        
        def update(data):
            return self.update_manager(downloader.get_data(manager.key), manager) 
        
        downloader.add_callback(token, update)

        def state_action(idx):
            if idx==0:
                return
            erc = 0
            if idx==1:
                for dev in manager.devices():
                    if self.check_status.get(dev.key, True):
                        dev.rpc.rpcInit.call()
            elif idx==2:
                for dev in manager.devices():
                    if self.check_status.get(dev.key, True):
                        dev.rpc.rpcEnable.call()
            elif idx==3:
                for dev in manager.devices():
                    if self.check_status.get(dev.key, True):
                        dev.rpc.rpcDisable.call()
            elif idx==4:
                for dev in manager.devices():
                    if self.check_status.get(dev.key, True):
                        dev.rpc.rpcReset.call()
            self.state_action.setCurrentIndex(0)
        self.state_action.currentIndexChanged.connect(state_action)
        
        extra = manager.extra    
        layouts = extra.get("layouts", [])
        if not layouts: 
            extra = build_standard_layout(manager)
            layouts = extra['layouts']
        
        
        self.layout_selector.clear()
        self.layout_selector.addItems(layouts)
        
        # container_layout = QtWidgets.QVBoxLayout()
        # self.device_container.setLayout(vlayout)
        self.dev_widgets = []
        if layouts:
            ly = layouts[0]
            device_layout = QtWidgets.QVBoxLayout()
            self.device_container.setLayout(device_layout)
            make_layout(device_layout, extra[ly], downloader, manager, self.dev_widgets, self.check_status)
        
        
        def layout_selector(idx):
            #self.device_container.clear()
            for dev_widget in self.dev_widgets:
                dev_widget.disconnect_downloader()
                if hasattr(dev_widget, "check"):
                    dev_widget.check.disconnect() # remove call backs 
                
            for i in reversed(range(device_layout.count())): 
                device_layout.itemAt(i).widget().setParent(None)
            self.dev_widgets.clear()
                
            make_layout(device_layout, extra[layouts[idx]], downloader, manager, self.dev_widgets, self.check_status)
        
        self.layout_selector.currentIndexChanged.connect(layout_selector)
        
        def check_all():
            s = self.check_all.isChecked()
            for dev_widget in self.dev_widgets:
                self.check_status[dev_widget.device_key] = s
        self.check_all.stateChanged.connect(check_all)
        



## ########################################
def build_standard_layout(manager):
    """ Build a standard layout for a given manager 
    
    This is used when no *_extra.yml file was given 
    """
    extra = {}
    devices = [dev.name for dev in manager.devices()]
    extra['layouts'] = ["One Line", "Basic Ctrl"]
    extra['One Line'] = {
          "type": "tabs",
          "children":[{"type":"tab", 
                       "name":"Devices",
                       "children":[{
                           "type"   :"devices",
                           "devices" :devices, 
                           "widget_type": "line"
                           }]
                    }]
    }
    extra['Basic Ctrl'] = {
          "type": "tabs",
          "children":[{"type":"tab", 
                       "name":"Devices",
                       "children":[{
                           "type"    :"devices",
                           "devices" :devices, 
                           "widget_type": "ctrl"
                           }]
                    }]    
    }
    return extra



class ManagerCtrl(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUI()
        self.connection = None

    def initUI(self):
        uic.loadUi(find_ui('manager_ctrl.ui'), self)
        #self.show()

    def update_device(self, data, mgr):
        state = data['state']
        self.state.setText("{}: {}".format(state, data['state_txt']))
        self.state.setStyleSheet(get_style(data['state_group']))
        
    def link_device(self, downloader, manager):
        
        if self.connection:
            previous_downloader, token = self.connection
            previous_downloader.disconnect(token)
        ## create a new connection 
        token = downloader.new_connection()
        self.connection = (downloader, token)
        
        
        try:
            self.state_action.currentIndexChanged.disconnect()
        except TypeError:
            pass
        
        self.state_action.clear()
        self.state_action.addItems(['', "INIT", "ENABLE", "DISABLE", "RESET"])
        self.state.setText("UNKNOWN")

        # add the necessary nodes to the downloader
        downloader.add_node(token, manager.stat.state, manager.stat.state_txt, manager.stat.state_group)
        
        def update(data):
            return self.update_device(downloader.get_data(manager.key), manager) 
        
        downloader.add_callback(token, update)

        def state_action(idx):
            if idx==0:
                return
            erc = 0
            if idx==1:
                for dev in manager.devices():
                    dev.rpc.rpcInit.call()
            elif idx==2:
                for dev in manager.devices():
                    dev.rpc.rpcEnable.call()
            elif idx==3:
                for dev in manager.devices():
                    dev.rpc.rpcDisable.call()
            elif idx==4:
                for dev in manager.devices():
                    dev.rpc.rpcReset.call()
            self.state_action.setCurrentIndex(0)
        self.state_action.currentIndexChanged.connect(state_action)


class ManagerMainWindow(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUI()

    def initUI(self):
        self.top = 100
        self.left = 100
        self.width = 600
        self.height = 600
        #self.setGeometry(self.left, self.top, self.width, self.height)
        self.setMinimumSize(600,300)
        self.layout = QVBoxLayout(self)

        self.ctrl = ManagerCtrl()
        #self.ctrl.move(0, 0)

        self.devices = ManagerDevices()

        #self.devices.move(0,0)
        self.layout.addWidget(self.ctrl)
        self.layout.addWidget(self.devices)

        #self.layout.setAlignment(Qt.AlignTop)
        #self.layout.addStretch()
        #self.layout.addStretch()
        #self.setLayout(self.layout)

        #self.show()

    def link_device(self, downloader, manager):
        self.ctrl.link_device(downloader, manager)
        self.devices.link_device(downloader, manager)
        
        
def make_layout(layout, laydef, downloader, manager, dev_widgets, check_status):
    _make_layout_walk(layout, laydef, downloader, manager, 0, dev_widgets, check_status)
    
def _make_layout_walk(layout, lydef, downloader, manager, child_num, dev_widgets, check_status):
    
    tpe = lydef['type']
    if tpe == "vertical":
        
        container = QtWidgets.QWidget()        
        child_layout = QtWidgets.QVBoxLayout()
        container.setLayout(child_layout)
        layout.addWidget(container)
        
        for i, lydef in enumerate(lydef['children']):
             _make_layout_walk(child_layout, lydef, downloader, manager, i, dev_widgets, check_status)
        child_layout.addStretch()
    
    elif tpe == "horizontal":
        
        container = QtWidgets.QWidget()        
        child_layout = QtWidgets.QHBoxLayout()
        container.setLayout(child_layout)
        layout.addWidget(container)
        
        for i, lydef in enumerate(lydef['children']):
             _make_layout_walk(child_layout, lydef, downloader, manager, i, dev_widgets, check_status)
        #child_layout.addStretch()


        
    elif tpe == "tabs":
        
        tabs = QtWidgets.QTabWidget()
        layout.addWidget(tabs)
        for i, lydef in enumerate(lydef['children']):
            if lydef['type'] != "tab":
                raise ValueError("Only tab are allowed inside tabs")
            
            tab = QtWidgets.QScrollArea()
            
            child_container = QtWidgets.QWidget()
            child_layout = QtWidgets.QVBoxLayout()
            child_container.setLayout(child_layout)
            
            tab.setWidgetResizable(True)
            tab.setWidget(child_container)
            
            tabs.addTab(tab, lydef.get('name', 'tab %d'%(i+1)))
            for j, lydef in enumerate(lydef['children']):
                _make_layout_walk(child_layout, lydef, downloader, manager, j, dev_widgets, check_status)
            child_layout.addStretch()    
        
    
    elif tpe == "device":
        device = manager.get_device(lydef['device'])
        try:
            Widget = get_widget_constructor(lydef['widget_type'], device.dev_type)
        except ValueError:
            
            warning("Cannot find a %r widget for device of type %r"%(lydef['widget_type'], device.dev_type))
            Widget =   get_widget_constructor(lydef['widget_type'], 'Device')
        
        widget = Widget()
        layout.addWidget(widget)
        if hasattr(widget, "check"):
            widget.check.show()
            def checkChanged():
                check_status[device.key] = widget.check.isChecked()
            widget.check.stateChanged.connect(checkChanged)    
        
        dev_widgets.append(widget)
        widget.link_device(downloader, device, altname=device.name)
    
    elif tpe == "all_devices":
        devices = manager.devices()
        widget_type = lydef['widget_type']
        for i,device in enumerate(devices):
            nlydef = {**lydef, 
                "type":"device", "device":device.name
            }
            _make_layout_walk(layout, nlydef, downloader, manager, i, dev_widgets, check_status)
    
    elif tpe == "devices":
        devices = lydef['devices']
        widget_type = lydef['widget_type']
        for i,device in enumerate(devices):
            nlydef = {**lydef, 
                      "type":"device", "device":device,
                     }
            _make_layout_walk(layout, nlydef, downloader, manager, i, dev_widgets, check_status)
    
    elif tpe == "device_types":
        devices = manager.devices()
        dev_types = lydef['device_types']
        
        for i,device in enumerate(devices):
            if device.dev_type in dev_types:
                nlydef = {**lydef, 
                    "type":"device", "device":device.name,
                }
                _make_layout_walk(layout, nlydef, downloader, manager, i, dev_widgets, check_status) 
                
    elif tpe == "device_type":  
        nlydef = {**lydef, "type":"device_types", "device_types":[lydef['device_type']]}
        _make_layout_walk(layout, nlydef, downloader, manager, i, dev_widgets, check_status)      
        
    else:
        raise ValueError("Unknown type %r"%tpe)