###############################
#                             #
#  Coded By: Saurabh Joshi    #
#  Original: 12/10/12         #
#  Date Modified: 24/07/15    #
#  modif by: Fadiga Ibrahima  #
#  File: Notification System  #
###############################

import sys
from PyQt4 import QtCore, QtGui
import time

global OS
try:
    from ctypes import windll
    OS = 0
except Exception as e:
    print(e)
    OS = 1


class Notification(QtGui.QDialog):
    closed = QtCore.pyqtSignal()

    def __init__(self, mssg='' ,parent=None):
        QtGui.QDialog.__init__(self,parent)
        # self.parent = parent
        self.mssg = mssg
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.createNotification(self.mssg)
        css = """
                color: white;
                background: black;
              """
        self.setStyleSheet(css)

    def createNotification(self, mssg):
        global OS
        if (OS!= 1):
            user32 = windll.user32
            #Get X coordinate of screen
            self.x = user32.GetSystemMetrics(0)
        else:
            cp = QtGui.QDesktopWidget().availableGeometry()
            self.x = cp.width()

        #Set the opacity
        self.f = 1.0

        #Set the message
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(QtGui.QLabel(mssg))
        self.setLayout(vbox)

        #Start Worker
        self.workThread = WorkThread()
        self.connect(self.workThread, QtCore.SIGNAL("update(QString)"),
                     self.animate)
        self.connect(self.workThread, QtCore.SIGNAL("vanish(QString)"),
                     self.disappear)
        self.connect(self.workThread, QtCore.SIGNAL("finished()"),
                     self.done)

        self.workThread.start()
        return

    #Quit when done
    def done(self):
        self.hide()
        return

    #Reduce opacity of the window
    def disappear(self):
        self.f -= 0.02
        self.setWindowOpacity(self.f)
        return

    #Move in animation
    def animate(self):
        self.move(self.x,0)
        self.x -= 1
        return


#The Worker
class WorkThread(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__(self)

    def run(self):
        #Bring em in :D
        for i in range(336):
            time.sleep(0.0001)
            self.emit(QtCore.SIGNAL('update(QString)'), "ping")
        #Hide u bitch :P
        for j in range(50):
            time.sleep(0.1)
            self.emit(QtCore.SIGNAL('vanish(QString)'), "ping")
        return
