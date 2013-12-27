#!/usr/bin/python
from threading import  Thread, Event, Lock
#import threading
import urllib2 
import urllib 
from time import sleep

from PyQt4 import QtCore, QtGui
import bitarray

from defines import *
from tile import *
from utils import *
from sys import *

class TileDownloader(QtCore.QObject, TileUtils):

    receivedSignal = QtCore.pyqtSignal()
    
    __receivedSignal__ = QtCore.pyqtSignal([int, int, int])
    
    def __init__(self, parent=None):
        super(TileDownloader, self).__init__(parent)
        TileUtils.__init__(self)
        self.tileUrl=""
        self.serverNumber = 0
        self.tile = Tile()
        self.stopThread = False
        self.event = Event()
        self.event.clear()
        self.serverName = GOOGLE
        
        self.threadLock = Lock()
        self.t = Thread(target = self.downloadThread)
        self.t.start()
        self.__receivedSignal__[int, int, int].connect(self.slotTileReceived)
        
    def slotTileReceived(self, x, y, z):
        
        tile = Tile()
        tile.setTileImage(QtGui.QPixmap("image.png"))
        id = [x, y, z]    
        tile.setTileId(id)
        self.pushFront(tile) #adds a tile to tiles list    
        self.receivedSignal.emit()
        
    def downloadThread(self):
        
        while self.stopThread == False:
            
            self.event.wait(1)
            if len(self.tilesIDToDownload) > 0:
                while len(self.tilesIDToDownload) > 0:
                    
                    tileId = self.tilesIDToDownload[0]   
                    del self.tilesIDToDownload[0]
                #    print "download tile ", tileId, len(self.tilesIDToDownload)
                    
                    if self.serverName == GOOGLE:
                        url = str("http://mt{0}.google.com/vt/lyrs=m@169000000&hl=en&x={1}&y={2}&zoom={3}").format(int(self.serverNumber), int(tileId[0]), int(tileId[1]), int(tileId[2]))
                        print url
                        
                        self.serverNumber += 1
                        self.serverNumber %= 4
                    
                        try:
                            urllib.urlretrieve(url, 'image.png')
                            self.__receivedSignal__.emit(tileId[0], tileId[1], tileId[2])
                            
                        except IOError:
                            print 'Cannot open the following link ', url
                        
                self.event.clear()
            
   
    def downloadTile(self, serverName, tileId):
        self.serverName = serverName
        self.tilesIDToDownload.append(tileId)
        self.event.set()
        
    def getTile(self):
        if len(self.tilesMap) > 0:
            tile = Tile()
            tile.copyTile(self.tilesMap[0])
            del self.tilesMap[0]
            return tile
        else:
            return Tile()
    
    def getTileImage(self):
        return QtGui.QPixmap(self.tile.getTileImage())
    
