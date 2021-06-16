###############################
#                             #
#  Coded By: Saurabh Joshi    #
#  Original: 12/10/12         #
#  Date Modified: 20/05/18    #
#  modif by: Fadiga Ibrahima  #
#  File: Notification System  #
###############################

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

    def __init__(self, mssg, parent=None, type_mssg="", *args, **kwargs):
        super(Notification, self).__init__(parent=parent, *args, **kwargs)

        self.mssg = str(mssg)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        if type_mssg == "success":
            background = "green"
        elif type_mssg == "error":
            background = "red"
        elif type_mssg == "warring":
            background = "grey"
        else:
            background = "black"

        css = """ color: white;background: {}; """.format(background)
        self.setStyleSheet(css)
        self.create_notification()
        self.show()

    def create_notification(self):
        # print("create_notification")
        if OS != 1:
            user32 = windll.user32
            # Get X coordinate of screen
            # self.x = user32.GetSystemMetrics(0)
            self.x = user32.GetSystemMetrics(0) / 5

        else:
            cp = QtGui.QDesktopWidget().availableGeometry()
            self.x = cp.width()
        # self.x = 1
        self.y = 1
        # Set the opacity
        self.f = 1.0
        # Start Worker
        self.workThread = WorkThread(self)
        # self.connect(self.workThread, QtCore.SIGNAL("update(QString)"), self.animate)
        self.connect(self.workThread, QtCore.SIGNAL("update2(QString)"), self.animate2)
        self.connect(self.workThread, QtCore.SIGNAL("vanish(QString)"), self.disappear)
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

    # Move in animation

    def animate(self):
        self.move(self.x, self.y)
        self.y += 1
        return

    def animate2(self):
        self.move(self.x, self.y)
        self.y -= 1
        return


# The Worker


class WorkThread(QtCore.QThread):
    def __init__(self, mv):
        super(QtCore.QThread, self).__init__()

    def run(self):
        while True:
            # Bring em in :D
            for i in range(30):
                time.sleep(0.001)
                self.emit(QtCore.SIGNAL('update(QString)'), "ping")
            for j in range(30):
                time.sleep(0.001)
                self.emit(QtCore.SIGNAL('update2(QString)'), "ping")
            # Hide u bitch :P
            for j in range(5):
                time.sleep(0.0001)
                self.emit(QtCore.SIGNAL('vanish(QString)'), "ping")
            return
