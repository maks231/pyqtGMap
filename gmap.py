#!/usr/bin/env python

import sys
from gui import *
from defines import *

def main():
    app = QtGui.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    mainWindow.resize(INITIAL_WINDOW_SIZE[0], INITIAL_WINDOW_SIZE[1])
    
    app.exec_()

if __name__== '__main__':
    main()
    