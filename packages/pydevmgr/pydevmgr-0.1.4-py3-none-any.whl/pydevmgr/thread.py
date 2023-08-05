from threading import Thread as _Thread
import time

class Thread(_Thread):
    """ Thread with a kill and isrunning method """
    _livesignal = True
    def __init__(self):
        self._livesignal = True
        self._lock = False
        super(Thread, self).__init__()
        

    def kill(self):
        self._livesignal = False

    def isrunning(self):
        return self._livesignal
