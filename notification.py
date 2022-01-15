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
        # cp = QtGui.QDesktopWidget().availableGeometry()
        # self.x = cp.width()
        self.x = 2
        self.y = 1
        # Set the opacity
        self.f = 1.0
        # Start Worker
        self.workThread = WorkThread(self)
        self.connect(self.workThread, QtCore.SIGNAL("update(QString)"), self.animate)
        # self.connect(self.workThread, QtCore.SIGNAL("vanish(QString)"), self.disappear)
        self.connect(self.workThread, QtCore.SIGNAL("finished()"), self.done)

        self.workThread.start()

        vbox = QtGui.QVBoxLayout()
        # Set the message
        vbox.addWidget(QtGui.QLabel(self.mssg))
        self.setLayout(vbox)

        return

    # Quit when done
    def done(self):
        # self.hide()
        self.close()
        return

    # Reduce opacity of the window
    def disappear(self):
        self.f -= 0.0002
        self.setWindowOpacity(self.f)
        return

    # Move in animation

    def animate(self):
        self.move(self.x, self.y)
        self.y += 0.5
        return


# The Worker


class WorkThread(QtCore.QThread):
    def __init__(self, mv):
        super(QtCore.QThread, self).__init__()

    def run(self):
        while True:
            # Bring em in :D
            for i in range(30):
                time.sleep(0.01)
                self.emit(QtCore.SIGNAL("update(QString)"), "ping")
            # Hide u bitch :P
            time.sleep(0.1)
            self.emit(QtCore.SIGNAL("vanish(QString)"), "ping")

            time.sleep(0.1)
            self.emit(QtCore.SIGNAL("finished(QString)"), "ping")
            return
