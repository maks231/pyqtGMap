
from PyQt4 import QtCore, QtGui, QtOpenGL
from tile import *
from tiledownloader import TileDownloader
from sys import *
from defines import *
from utils import *
from math import *

class Graphics(QtGui.QGraphicsScene, TileUtils):
    
    def __init__(self, width, height):
        
        TileUtils.__init__(self)
        QtGui.QGraphicsScene.__init__(self) # for signals and slots operations
        
        self.pic = QtGui.QPixmap(TILESIZE_XY[0], TILESIZE_XY[1])
        self.noImage = QtGui.QPixmap()   # an image "there is an error or no data"
        self.noImage.load("./icons/missing.png")  # loads the image from the given full path
            
        self.setSceneRect(0, 0, width, height)
               
        self.mainPixmap = QtGui.QPixmap(width, height)
        self.mainItem = QtGui.QGraphicsPixmapItem();
        self.mainItem.setPixmap(self.mainPixmap)
        
        self.addItem(self.mainItem)
        
        self.updateTimer = QtCore.QTimer(self)
        self.updateTimer.setInterval(UPDATE_GRAPHIC_RATE)
        self.updateTimer.timeout.connect(self.updateScene)
        self.updateTimer.start()

        self.offsetFromCenter = [0, 0]
        self.initialOffsetFromCenter = [0, 0]
        
        self.centralTileID = [50, 80]
        self.center = XY_PIX_COORD
        self.tilesNumbXY = XY_PIX_COORD
        
        self.setCenter()
        
        self.tileDownloader = TileDownloader()
        self.tileDownloader.receivedSignal.connect(self.slotTileReceived)
    
        self.tileDownloader.downloadTile(GOOGLE, [50, 80, 9])
        
    def updateScene(self):
        if len(self.tilesMap) > 0:
            self.update()
    
    def slotTileReceived(self):
        tile = Tile()
        tile.copyTile(self.tileDownloader.getTile())
        if tile.isEmpty() == False:
            index = self.getTileIndexInMapArray(self.tilesMap, tile.getTileId())
            if index == -1: #if tile was not found in the list of tiles
                self.pushFront(tile) #adds a tile to tiles list
              
    def setCenter(self):
        self.center = self.width()/2, self.height()/2 # the center of view area
        self.tilesNumbXY = int(ceil(self.width()/TILESIZE_XY[0]))+1, int(ceil(self.height()/TILESIZE_XY[1]))+1 # number of tiles along X and Y axes
        
    def update (self):
        
        qp = QtGui.QPainter()
        qp.begin(self.mainPixmap)
        
        self.mainPixmap.fill(QtCore.Qt.black)
        
        # the id of the first (top left) tile to display
        tileID = [self.centralTileID[0] - ceil(int(self.tilesNumbXY[0]/2)), self.centralTileID[1] - ceil(int(self.tilesNumbXY[1]/2))]
            
        for x in range(0, self.tilesNumbXY[0]):
            for y in range(0, self.tilesNumbXY[1]):
                
                tempTileID = [tileID[0] + x, tileID[1] + y, 9]
                #     (offcet from the center in pixels) - offcet id from the current centeral tile  *  x size of a tile
                xx = (self.center[0] - HALFTILESIZE_XY[0]) + ((tempTileID[0] - self.centralTileID[0]) * TILESIZE_XY[0]) + self.offsetFromCenter[0]
                yy = (self.center[1] - HALFTILESIZE_XY[1]) + ((tempTileID[1] - self.centralTileID[1]) * TILESIZE_XY[1]) + self.offsetFromCenter[1]
               
                index = self.getTileIndexInMapArray(self.tilesMap, tempTileID)
                
                if  index > -1 and self.tilesMap[index].isEmpty() == False:
                    
                    qp.drawPixmap(xx, yy, self.tilesMap[index].getTileImage())
                    qp.drawText(xx+10, yy+15, QtCore.QString("%1, %2").arg(tempTileID[0]).arg(tempTileID[1]))
                else:
                    if index > -1:
                        del self.tilesMap[index]
                        index = self.getTileToDownloadIndex(self.tilesIDToDownload, tempTileID)
                        if index > -1:
                            del tilesIDToDownload[index]
                            self.tilesIDToDownload.append(tempTileID)
                            self.tileDownloader.downloadTile(GOOGLE, tempTileID)
                    else:        
                        #fills the array with the tile's idexes to download 
                        if self.getTileToDownloadIndex(self.tilesIDToDownload, tempTileID) == -1:
                            self.tilesIDToDownload.append(tempTileID)
                            self.tileDownloader.downloadTile(GOOGLE, tempTileID)
                        qp.drawPixmap(xx, yy, self.noImage)
                        qp.drawText(xx+10, yy+15, QtCore.QString("%1, %2").arg(tempTileID[0]).arg(tempTileID[1]))
                    
        qp.end()
    
        self.mainItem.setPixmap(self.mainPixmap);
        
    def getScene(self):        #returns pointer on the QGraphicsScene 
        return self
    
    def mousePressEvent(self, event):
        
        self.initialOffsetFromCenter = event.scenePos().x(), event.scenePos().y()
       # self.update()
       
    def mouseMoveEvent(self, event):
        
        position = event.scenePos().x(), event.scenePos().y()
        
        self.offsetFromCenter[0] = position[0] - self.initialOffsetFromCenter[0]   
        self.offsetFromCenter[1] = position[1] - self.initialOffsetFromCenter[1]
        self.update()
    
    def mouseReleaseEvent(self, event):
        
#        idX = ceil(self.offsetFromCenter[0] % HALFTILESIZE_XY[0])
#        if idX >= 0:
#            self.centralTileID[0] += idX
#        else:
#            self.centralTileID[0] -= idX
            
#        idY = ceil(self.offsetFromCenter[1] % (HALFTILESIZE_XY[1]))
#        if idY >= 0:
#            self.centralTileID[1]+=idY
#        else:
#            self.centralTileID[1]-=idY
        
        self.update()
        
    def setViewportSize(self, width, height):
        self.setSceneRect(0, 0, width, height)
        self.setCenter()
        self.mainPixmap = QtGui.QPixmap(width, height)
        self.update()