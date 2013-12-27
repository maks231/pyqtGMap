from PyQt4 import QtCore, QtGui
from sys import *
from defines import *

#It is a tile object, contais an image , the "ID" and the map's zoom level of the tile 
class Tile():
    
    def __init__ (self):
        self.image = QtGui.QPixmap()
        self.tileId = TILE_ID #tile's id on the global map

    def tileReset(self):
        self.image = QtGui.QPixmap()
        self.tileId = TILE_ID #tile's id on the global map
        
    def isEmpty(self):
        return self.image.isNull()
    
    def setTileId(self, tileId):
        self.tileId = tileId
        
    def getTileId(self):
        return self.tileId
    
    def getAllData(self):
        return self.tileId, self.image
    
    def setAllData(self, tileId, image):
        self.tileId = tileId
        self.image = image
    
    def setTileImage(self, image):
        self.image = image
    
    def copyTile(self, val):
        self.tileId = val.tileId
        self.image = val.image
    
    def getTileImage(self):
        return self.image

        
