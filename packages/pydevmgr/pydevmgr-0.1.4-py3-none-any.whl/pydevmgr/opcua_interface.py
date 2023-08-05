from opcua import Client

_ua_clients = {}
def get_ua_client(uri):
    """ get an opc-ua client object for the given address create one if not exists """
    global _ua_clients
    
    try:
        client = _ua_clients[uri]
    except KeyError:
        client = UaClient(uri)
        _ua_clients[uri] = client
    
    return client    

class UaClient:
    def __init__(self, uri):
        self.uri = uri 
        self._connected = False
        self._client = Client(self.uri)            
    
    @property
    def connected(self):
        return self._connected
        
        
    def connect(self):
        self._client.connect()
        self._connected = True
        # TOD implement connection
    
    def disconnect(self):
        self._client.disconnect()
        self._connected = False
        # TODO implement disconnection
        
    def get(self, path, namespace=4):
        node = self._client.get_node("ns={};s={}".format(namespace, path))
        return node.get_value()
    
    def set(self, path, value, namespace=4):
        print("To be implemented SET %r -> %r"%(path, value))
    
    def set_several(self, keyval):
        print("To be implemented SET SEVERAL %r"%keyval)
    
    def call(self, path, args):
        print("To be implemented")

