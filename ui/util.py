#!/usr/bin/env python
# -*- coding: utf8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu
# maintainer: Fad
from __future__ import (unicode_literals, absolute_import, division, print_function)

import os, sys
import locale
import tempfile
import subprocess
import datetime

from PyQt4 import QtGui, QtCore
from Common.ui.window import F_Window


class PDFFileUnavailable(IOError):
    pass


def uopen_prefix(platform=sys.platform):

    if platform in ('win32', 'win64'):
        return 'cmd /c start'

    if 'darwin' in platform:
        return 'open'

    if platform in ('cygwin', 'linux') or \
       platform.startswith('linux') or \
       platform.startswith('sun') or \
       'bsd' in platform:
        return 'xdg-open'

    return 'xdg-open'


def openFile(file):
    if sys.platform == 'linux2':
        subprocess.call(["xdg-open", file])
    else:
        os.startfile(file)


def uopen_file(filename):
    if not os.path.exists(filename):
        raise IOError(u"Fichier %s non valable." % filename)
    subprocess.call('%(cmd)s %(file)s' % {'cmd': uopen_prefix(), 'file': filename}, shell=True)


def get_temp_filename(extension=None):
    f = tempfile.NamedTemporaryFile(delete=False)
    if extension:
        fname = '%s.%s' % (f.name, extension)
    else:
        fname = f.name
    return fname


def raise_error(title, message):
    box = QtGui.QMessageBox(QtGui.QMessageBox.Critical, title,
                            message, QtGui.QMessageBox.Ok,
                            parent=F_Window.window)
    box.setWindowOpacity(0.9)
    box.exec_()


def raise_success(title, message):
    box = QtGui.QMessageBox(QtGui.QMessageBox.Information, title,
                            message, QtGui.QMessageBox.Ok,
                            parent=F_Window.window)
    box.setWindowOpacity(0.9)
    box.exec_()


def formatted_number(number):
    """ """

    try:
        return locale.format("%d", number, grouping=True).decode(locale.getlocale()[1])
    except:
        return "%s" % number


class SystemTrayIcon(QtGui.QSystemTrayIcon):

    def __init__(self, mss, parent=None):

        QtGui.QSystemTrayIcon.__init__(self, parent)

        self.setIcon(QtGui.QIcon.fromTheme("document-save"))

        self.activated.connect(self.click_trap)
        # self.mss = ("Confirmation", "Mali rapou!!!!")
        self.show(mss)

    def click_trap(self, value):
        #left click!
        if value == self.Trigger:
            self.left_menu.exec_(QtGui.QCursor.pos())

    def welcome(self):
        self.showMessage(self.mss[0], self.mss[1])

    def show(self, mss):
        self.mss = mss
        QtGui.QSystemTrayIcon.show(self)
        QtCore.QTimer.singleShot(1000, self.welcome)


def is_int(val):

    try:
        val = unicode(val).split()
        v = ''
        for i in val:
            v += i
        return int(v)
    except:
        return 0


def date_datetime(dat):
    "reçoit une date return une datetime"
    dat = str(unicode(dat))
    day, month, year = dat.split('/')
    dt = datetime.datetime.now()
    return datetime.datetime(int(year), int(month), int(day),
                             int(dt.hour), int(dt.minute),
                             int(dt.second), int(dt.microsecond))


def alerte():
    pass


def date_end(dat):
    dat = str(unicode(dat))
    day, month, year = dat.split('/')
    return datetime.datetime(int(year), int(month), int(day), 23, 59, 59)


def date_on(dat):
    dat = str(unicode(dat))
    day, month, year = dat.split('/')
    return datetime.datetime(int(year), int(month), int(day), 0, 0, 0)


def date_start_end(date, st):
    day, month, year = str(unicode(date)).split('/')
    # return datetime(int(year), int(month), int(day), if st: 0 else 23, if st: 0 else 59, if st: 0 59)


def format_date(dat):
    dat = str(dat)
    day, month, year = dat.split('/')
    return '-'.join([year, month, day])


def show_date(dat):
    return dat.strftime(u"%A le %d %b %Y a %Hh:%Mmn")


def to_jstimestamp(adate):
    if not adate is None:
        return int(to_timestamp(adate)) * 1000


def to_timestamp(dt):
    """
    Return a timestamp for the given datetime object.
    """
    if not dt is None:
        return (dt - datetime.datetime(1970, 1, 1)).total_seconds()


class WigglyWidget(QtGui.QWidget):
    def __init__(self, test, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.setBackgroundRole(QtGui.QPalette.Midlight)
        print(test)
        newFont = self.font()
        newFont.setPointSize(newFont.pointSize() + 20)
        self.setFont(newFont)

        self.timer = QtCore.QBasicTimer()
        self.text = QtCore.QString(test)

        self.step = 0;
        self.timer.start(60, self)

    def paintEvent(self, event):
        sineTable = [0, 38, 71, 92, 100, 92, 71, 38, 0, -38, -71, -92, -100, -92, -71, -38]

        metrics = QtGui.QFontMetrics(self.font())
        x = (self.width() - metrics.width(self.text)) / 2
        y = (self.height() + metrics.ascent() - metrics.descent()) / 2
        color = QtGui.QColor()

        painter = QtGui.QPainter(self)

        for i in xrange(self.text.size()):
            index = (self.step + i) % 16
            color.setHsv((15 - index) * 16, 255, 191)
            painter.setPen(color)
            painter.drawText(x, y - ((sineTable[index] * metrics.height()) / 400), QtCore.QString(self.text[i]))
            x += metrics.width(self.text[i])

    def setText(self, newText):
        self.text = QtCore.QString(newText)

    def timerEvent(self, event):
        if (event.timerId() == self.timer.timerId()):
            self.step = self.step + 1
            self.update()
        else:
            QtGui.QWidget.timerEvent(event)