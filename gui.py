
from mainwindow import *
from graphics import *
from defines import *
from tiledownloader import *

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):

        QtGui.QMainWindow.__init__(self)
   
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)    
      
        self.graphics = Graphics(TILESIZE_XY[0], TILESIZE_XY[1])
        self.ui.graphicsView.setScene(self.graphics.getScene())
       # self.ui.graphicsView.setViewport(QtOpenGL.QGLWidget())   
   
    def resizeEvent(self, event):
       self.graphics.setViewportSize(self.ui.graphicsView.width()-2, self.ui.graphicsView.height()-2)