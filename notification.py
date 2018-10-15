###############################
#                             #
#  Coded By: Saurabh Joshi    #
#  Original: 12/10/12         #
#  Date Modified: 20/05/18    #
#  modif by: Fadiga Ibrahima  #
#  File: Notification System  #
###############################

import sys
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import pyqtSignal, Qt, QThread
import time

global OS
try:
    from ctypes import windll
    OS = 0
except Exception as e:
    print(e)
    OS = 1


class Notification(QWidget):

    def __init__(self, mssg, parent=None, type_mssg="", *args, **kwargs):
        super(Notification, self).__init__(parent=parent, *args, **kwargs)

        self.mssg = str(mssg)
        self.setWindowFlags(Qt.FramelessWindowHint)
        if type_mssg == "success":
            background = "green"
        elif type_mssg == "error":
            background = "red"
        elif type_mssg == "warring":
            background = "grey"
        else:
            background = "black"

        css = """ color: white; background: {}; """.format(background)
        self.setStyleSheet(css)
        self.create_notification()
        self.show()

    def createNotification(self):
        # print("createNotification")
        global OS
        if (OS != 1):
            user32 = windll.user32
            # Get X coordinate of screen
            self.x = user32.GetSystemMetrics(0)
            self.x = user32.GetSystemMetrics(0) / 2

        else:
            cp = QDesktopWidget().availableGeometry()
            self.x = cp.width()
        self.y = 1
        # Set the opacity
        self.f = 1.0

        # Start Worker
        self.workThread = WorkThread(self)

        self.workThread.mySignal.connect(self.animate)
        self.workThread.mySignal.connect(self.disappear)
        self.workThread.mySignal.connect(self.done)
        # self.connect(
        #     self.workThread, pyqtSignal("update(QString)"), self.animate)
        # self.connect(
        #     self.workThread, pyqtSignal("vanish(QString)"), self.disappear)
        # self.connect(
        #     self.workThread, pyqtSignal("finished()"), self.done)

        self.workThread.start()

        vbox = QVBoxLayout()
        # Set the message
        vbox.addWidget(QLabel(self.mssg))
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
        self.move(self.x, self.y)
        self.y += 1
        return

    def animate2(self):
        self.move(self.x, self.y)
        self.y -= 1
        return

# The Worker


class WorkThread(QThread):
    mySignal = pyqtSignal(str)

    def __init__(self, mv):
        super(QThread, self).__init__()

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
