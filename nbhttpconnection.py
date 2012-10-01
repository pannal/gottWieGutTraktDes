# -*- coding: utf-8 -*-
# 

import os, sys
import time, socket
import urllib
import thread
import threading

try:
    # Python 3.0 +
    import http.client as httplib
except ImportError:
    # Python 2.7 and earlier
    import httplib

try:
  # Python 2.6 +
  from hashlib import sha as sha
except ImportError:
  # Python 2.5 and earlier
  import sha
  
__author__ = "Hanz Weener"
__credits__ = ["Hanz Weener", "Ralph-Gordon Paul", "Adrian Cowan", "Justin Nemeth",  "Sean Rudford"]
__license__ = "GPL"
__maintainer__ = "Weener Mac Hanz"
__email__ = "gutah@rai.se"
__status__ = "Production"

# Allows non-blocking http requests
class NBHTTPConnection():    
    def __init__(self, host, port = None, strict = None, timeout = None):
        self.rawConnection = httplib.HTTPConnection(host, port, strict, timeout)
        self.responce = None
        self.responceLock = threading.Lock()
        self.closing = False
    
    def request(self, method, url, body = None, headers = {}):
        self.rawConnection.request(method, url, body, headers);
    
    def hasResult(self):
        if self.responceLock.acquire(False):
            self.responceLock.release()
            return True
        else:
            return False
        
    def getResult(self):
        while not self.hasResult() and not self.closing:
            time.sleep(1)
        return self.responce
    
    def go(self):
        self.responceLock.acquire()
        thread.start_new_thread ( NBHTTPConnection._run, ( self, ) )
        
    def _run(self):
        self.responce = self.rawConnection.getresponse()
        self.responceLock.release()
        
    def close(self):
        self.closing = True
        self.rawConnection.close()
    