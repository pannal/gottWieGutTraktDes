# -*- coding: utf-8 -*-
# 

import xbmc,xbmcaddon,xbmcgui
import telnetlib, time, datetime

try: import simplejson as json
except ImportError: import json

import threading
from utilities import *
from rating import *
from sync_update import *
from instant_sync import *
from scrobbler import Scrobbler

__author__ = "Hanz Weener"
__credits__ = ["Hanz Weener", "Ralph-Gordon Paul", "Adrian Cowan", "Justin Nemeth",  "Sean Rudford"]
__license__ = "GPL"
__maintainer__ = "Weener Mac Hanz"
__email__ = "gutah@rai.se"
__status__ = "Production"


# Receives XBMC notifications and passes them off to the rating functions
class NotificationService(threading.Thread):
    abortRequested = False
    def run(self):        
        #while xbmc is running
        scrobbler = Scrobbler()
        scrobbler.start()
        
        while (not (self.abortRequested or xbmc.abortRequested)):
            time.sleep(1)
            try:
                tn = telnetlib.Telnet('localhost', 9090, 10)
            except IOError as (errno, strerror):
                #connection failed, try again soon
                Debug("[Notification Service] Telnet too soon? ("+str(errno)+") "+strerror)
                time.sleep(1)
                continue
            
            Debug("[Notification Service] Waiting~");
            bCount = 0
            
            while (not (self.abortRequested or xbmc.abortRequested)):
                try:
                    if bCount == 0:
                        notification = ""
                        inString = False
                    [index, match, raw] = tn.expect(["(\\\\)|(\\\")|[{\"}]"], 0.2) #note, pre-compiled regex might be faster here
                    notification += raw
                    if index == -1: # Timeout
                        continue
                    if index == 0: # Found escaped quote
                        match = match.group(0)
                        if match == "\"":
                            inString = not inString
                            continue
                        if match == "{":
                            bCount += 1
                        if match == "}":
                            bCount -= 1
                    if bCount > 0:
                        continue
                    if bCount < 0:
                        bCount = 0
                except EOFError:
                    break #go out to the other loop to restart the connection
                
                Debug("[Notification Service] message: " + str(notification))
                
                # Parse recieved notification
                data = json.loads(notification)

                # Forward notification to functions
                if 'method' in data and 'params' in data and 'sender' in data['params'] and data['params']['sender'] == 'xbmc':
                    if data['method'] == 'Player.OnStop':
                        Debug("pb ended, %s" % getSync_after_x())
                        scrobbler.playbackEnded(data=data) # this is using syncIncreasePlayCount already

                    elif data['method'] == 'Player.OnPlay':
                        if 'data' in data['params'] and 'item' in data['params']['data'] and 'id' in data['params']['data']['item'] and 'type' in data['params']['data']['item']:
                            #fixme: look here for current position?
                            scrobbler.playbackStarted(data['params']['data'])
                    elif data['method'] == 'Player.OnPause':
                        scrobbler.playbackPaused()
                    elif data['method'] == 'VideoLibrary.OnUpdate':
                        Debug("OnUpdate %s" % data)
                        if 'data' in data['params'] and 'playcount' in data['params']['data']:
                            # 'playcount' in data indicates that playcount has changed. so we received a seen status on the item
                            if getSync_after_x() and data['params']['data']["playcount"] >= 1:
                                # we've played a file and consider it seen
                                syncIncreasePlayCount()
                                Debug("syncing, playcount: %s" % data['params']['data']["playcount"])
                                syncAfterX()

                            onlyOnUnwatchMark = getInstantOnlyOnUnwatchMark()
                            Debug("instantUpdateOnWatchMark: %s, %s" % (getInstantUpdateOnWatchMark(), onlyOnUnwatchMark))
                            if (getInstantUpdateOnWatchMark() and not onlyOnUnwatchMark) or (data['params']['data']["playcount"] == 0 and onlyOnUnwatchMark):
                                instantSyncPlayCount(data)

                    elif data['method'] == 'System.OnQuit':
                        self.abortRequested = True

        try:
            tn.close()
        except:
            Debug("[NotificationService] Encountered error attempting to close the telnet connection")
            raise
        scrobbler.abortRequested = True
        Debug("Notification service stopping")