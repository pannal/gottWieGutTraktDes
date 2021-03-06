# -*- coding: utf-8 -*-
# 

import os
import xbmcgui,xbmcaddon,xbmc
from utilities import *
from sync_update import *
from watchlist import *
from recommend import *
from friends import *
from trending import *

__author__ = "Hanz Weener"
__credits__ = ["Ralph-Gordon Paul", "Justin Nemeth",  "Sean Rudford"]
__license__ = "GPL"
__maintainer__ = "Weener Mac Hanz"
__email__ = "gutah@rai.se"
__status__ = "Production"

#read settings
__settings__ = xbmcaddon.Addon( "script.GottWieGutTraktDes" )
__language__ = __settings__.getLocalizedString

Debug("default: " + __settings__.getAddonInfo("id") + " - version: " + __settings__.getAddonInfo("version"))

# Usermenu:
def menu():

    # check if needed settings are set
    if checkSettings() == False:
        return

    options = [__language__(1210).encode( "utf-8", "ignore" ), __language__(1211).encode( "utf-8", "ignore" ), __language__(1212).encode( "utf-8", "ignore" ), __language__(1213).encode( "utf-8", "ignore" ), __language__(1214).encode( "utf-8", "ignore" ), "Open Settings"]
    
    while True:
        select = xbmcgui.Dialog().select("Abgetrakt", options)
        Debug("Select: " + str(select))
        if select == -1:
            Debug ("menu quit by user")
            return
        else:
            if select == 0: # Watchlist
                submenuWatchlist()
            elif select == 1: # Friends
                showFriends()
            elif select == 2: # Recommendations
                submenuRecommendations()
            elif select == 3: # Trending Movies / TV Shows
                submenuTrendingMoviesTVShows()
            elif select == 4: # Update / Sync / Clean
                submenuUpdateSyncClean()
            elif select == 5: #open settings
                __settings__.openSettings()


def submenuUpdateSyncClean():

    options = [__language__(1217).encode( "utf-8", "ignore" ), __language__(1218).encode( "utf-8", "ignore" ), __language__(1219).encode( "utf-8", "ignore" ), __language__(1220).encode( "utf-8", "ignore" ), __language__(1221).encode( "utf-8", "ignore" ), __language__(1222).encode( "utf-8", "ignore" )]
    
    while True:
        select = xbmcgui.Dialog().select("Abgetrakt", options)
        Debug("Select: " + str(select))
        if select == -1:
            Debug ("menu quit by user")
            return
        elif select == 0: # Update Movie Collection
            updateMovieCollection()
        elif select == 1: # Sync seen Movies
            syncSeenMovies()
            setSyncedNow()

        elif select == 2: # Update TV Show Collection
            updateTVShowCollection()
        elif select == 3: # Sync seen TV Shows
            syncSeenTVShows()
            setSyncedNow()

        elif select == 4: # Clean Movie Collection
            cleanMovieCollection()
        elif select == 5: # Clean TV Show Collection
            cleanTVShowCollection()

def submenuTrendingMoviesTVShows():

    options = [__language__(1250).encode( "utf-8", "ignore" ), __language__(1251).encode( "utf-8", "ignore" )]
    
    while True:
        select = xbmcgui.Dialog().select(__language__(1213).encode( "utf-8", "ignore" ), options)
        Debug("Select: " + str(select))
        if select == -1:
            Debug ("menu quit by user")
            return
        if select == 0: # Trending Movies
            showTrendingMovies()
        elif select == 1: # Trending TV Shows
            showTrendingTVShows()

def submenuWatchlist():

    options = [__language__(1252).encode( "utf-8", "ignore" ), __language__(1253).encode( "utf-8", "ignore" )]
    
    while True:
        select = xbmcgui.Dialog().select(__language__(1210).encode( "utf-8", "ignore" ), options)
        Debug("Select: " + str(select))
        if select == -1:
            Debug ("menu quit by user")
            return
        if select == 0: # Watchlist Movies
            showWatchlistMovies()
        elif select == 1: # Watchlist TV Shows
            showWatchlistTVShows()

def submenuRecommendations():
    
    options = [__language__(1255).encode( "utf-8", "ignore" ), __language__(1256).encode( "utf-8", "ignore" )]
    
    while True:
        select = xbmcgui.Dialog().select(__language__(1212).encode( "utf-8", "ignore" ), options)
        Debug("Select: " + str(select))
        if select == -1:
            Debug ("menu quit by user")
            return
        if select == 0: # Watchlist Movies
            showRecommendedMovies()
        elif select == 1: # Watchlist TV Shows
            showRecommendedTVShows()

menu()
