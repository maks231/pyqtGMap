import sys
from tile import *

# class inherited by Graphics class and tiledownloader
#Contais search functions
class TileUtils():
    def __init__(self):
        self.tilesMap = [] # a list of tile objects
        self.tilesIDToDownload = [TILE_ID] # a list of ides 
    
    def getTileToDownloadIndex(self, tID, val):
        for index in range(0, len(tID)):
            
            if val[0] == tID[index][0] and val[1] == tID[index][1] and val[2] == tID[index][2]:
             #   print val, " == ", tID[index], "index ", index
                return index        
        return -1
    
    def getTileIndexInMapArray(self, tMap, val):
        for index in range(0, len(self.tilesMap)):
            id = tMap[index].getTileId()
            if val[0] == id[0] and val[1] == id[1] and val[2] == id[2]:
                return index
        return -1
    
    def pushFront(self, tile):
        # I do not know why, but self.tilesMap.append(tile) doesn't in this case 
        self.tilesMap.insert(0, Tile())
        self.tilesMap[0].copyTile(tile)
        #print "tile was added to o the list"
        
    def pushBack(self, tile):
        # I do not know why, but self.tilesMap.append(tile) doesn't in this case 
        self.tilesMap.append(Tile())
        self.tilesMap[-1].copyTile(tile)