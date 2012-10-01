# -*- coding: utf-8 -*-
# 

import xbmc,xbmcaddon,xbmcgui
import telnetlib, time

try: import simplejson as json
except ImportError: import json

import threading
from utilities import *
from instant_sync import *

__author__ = "Hanz Weener"
__credits__ = ["Hanz Weener", "Ralph-Gordon Paul", "Adrian Cowan", "Justin Nemeth",  "Sean Rudford"]
__license__ = "GPL"
__maintainer__ = "Weener Mac Hanz"
__email__ = "gutah@rai.se"
__status__ = "Production"

__settings__ = xbmcaddon.Addon( "script.GottWieGutTraktDes" )
__language__ = __settings__.getLocalizedString

# Move this to its own file
def instantSyncPlayCount(data):
    if data['params']['data']['item']['type'] == 'episode':
        info = getEpisodeDetailsFromXbmc(data['params']['data']['item']['id'], ['showtitle', 'season', 'episode', 'runtime'])
        if info == None: return
        Debug("[Instant-sync] (episode playcount): "+str(info))
        if data['params']['data']['playcount'] == 0:
            res = setEpisodesUnseenOnTrakt(None, info['showtitle'], None, [{'season':info['season'], 'episode':info['episode'], 'runtime': info['runtime']}])
        elif data['params']['data']['playcount'] == 1:
            res = setEpisodesSeenOnTrakt(None, info['showtitle'], None, [{'season':info['season'], 'episode':info['episode'], 'runtime': info['runtime']}])
        else:
            return
        Debug("[Instant-sync] (episode playcount): responce "+str(res))
    if data['params']['data']['item']['type'] == 'movie':
        info = getMovieDetailsFromXbmc(data['params']['data']['item']['id'], ['imdbnumber', 'title', 'year', 'playcount', 'lastplayed', 'runtime'])
        if info == None: return
        Debug("[Instant-sync] (movie playcount): "+str(info))
        if 'lastplayed' not in info: info['lastplayed'] = None
        if data['params']['data']['playcount'] == 0:
            res = setMoviesUnseenOnTrakt([{'imdb_id':info['imdbnumber'], 'title':info['title'], 'year':info['year'], 'plays':data['params']['data']['playcount'], 'last_played':info['lastplayed'], 'runtime': info['runtime']}])
        elif data['params']['data']['playcount'] == 1:
            res = setMoviesSeenOnTrakt([{'imdb_id':info['imdbnumber'], 'title':info['title'], 'year':info['year'], 'plays':data['params']['data']['playcount'], 'last_played':info['lastplayed'], 'runtime': info['runtime']}])
        else:
            return
        Debug("[Instant-sync] (movie playcount): responce "+str(res))