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


class Notification(QtGui.QWidget):
    closed = QtCore.pyqtSignal()

    def __init__(self, mssg,  parent=None, type_mssg="", *args, **kwargs):
        super(Notification, self).__init__(parent=parent, *args, **kwargs)

        self.mssg = str(mssg)
        print(mssg)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        if type_mssg == "success":
            background = "green"
        elif type_mssg == "error":
            background = "red"
        elif type_mssg == "warring":
            background = "yellow"
        else:
            background = "black"

        css = """ color: white; background: {}; """.format(background)
        self.setStyleSheet(css)
        self.createNotification()
        self.show()

    def createNotification(self):
        # print("createNotification")
        global OS
        if (OS != 1):
            user32 = windll.user32
            # Get X coordinate of screen
            self.x = user32.GetSystemMetrics(0)
        else:
            cp = QtGui.QDesktopWidget().availableGeometry()
            self.x = cp.width()
        self.y = 2

        # Set the opacity
        self.f = 1.0

        # Start Worker
        self.workThread = WorkThread(self)
        self.connect(
            self.workThread, QtCore.SIGNAL("update(QString)"), self.animate)
        self.connect(
            self.workThread, QtCore.SIGNAL("vanish(QString)"), self.disappear)
        self.connect(self.workThread, QtCore.SIGNAL("finished()"), self.done)

        self.workThread.start()

        vbox = QtGui.QVBoxLayout()
        # Set the message
        vbox.addWidget(QtGui.QLabel(self.mssg))
        self.setLayout(vbox)

        return

    # Quit when done
    def done(self):
        self.hide()
        return

    # Reduce opacity of the window
    def disappear(self):
        self.f -= 0.02
        self.setWindowOpacity(self.f)
        return

    #Move in animation
    def animate(self):
        # print(x)
        self.move(self.x, self.y)
        self.x -= 1
        return

# The Worker


class WorkThread(QtCore.QThread):

    def __init__(self, mv):
        super(QtCore.QThread, self).__init__()

    def run(self):
        while True:
            # Bring em in :D
            for i in range(336):
                time.sleep(0.0001)
                self.emit(QtCore.SIGNAL('update(QString)'), "ping")
            # Hide u bitch :P
            for j in range(50):
                time.sleep(0.1)
                self.emit(QtCore.SIGNAL('vanish(QString)'), "ping")
            return
