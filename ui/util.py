#!/usr/bin/env python
# -*- coding: utf8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu
# maintainer: Fad
from __future__ import (
    unicode_literals, absolute_import, division, print_function)

import os
import sys
import locale
import tempfile
import subprocess
import hashlib
from time import mktime, strptime

from uuid import getnode

from datetime import datetime

from PyQt4 import QtGui, QtCore
from Common.ui.window import FWindow
from Common.cstatic import CConstants

try:
    unicode
except NameError:
    unicode = str


def device_amount(value, dvs=None):

    from Common.models import Organization
    if dvs:
        return "{} {}".format(formatted_number(value), dvs)

    try:
        organ = Organization().get(id=1)
    except Exception as e:
        print(e)
    d = organ.DEVISE[organ.devise]
    v = formatted_number(value)
    if organ.devise == organ.USA:
        return "{d}{v}".format(v=v, d=d)
    else:
        return "{v} {d}".format(v=v, d=d)


def check_is_empty(field):
    stylerreur = ""
    flag = False
    containt = ""
    # if isinstance(field, )
    field.setToolTip("")
    if isinstance(field, QtGui.QTextEdit):
        containt = field.toPlainText()
    else:
        containt = field.text()

    if len(containt) == 0:
        field.setToolTip("Champs requis")
        stylerreur = "background-color: #fff79a;"
        flag = True
    field.setStyleSheet(stylerreur)
    return flag


def field_error(field, msg):
    field.setStyleSheet("background-color: #fff79a;")
    field.setToolTip("%s" % msg)
    return False


def is_valide_codition_field(field, msg, condition):
    stylerreur = ""
    flag = False
    field.setToolTip("")
    if condition:
        field.setToolTip(msg)
        stylerreur = "background-color: #fff79a;"
        flag = True
    field.setStyleSheet(stylerreur)
    return flag


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
    subprocess.call('%(cmd)s %(file)s' %
                    {'cmd': uopen_prefix(), 'file': filename}, shell=True)


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
                            parent=FWindow.window)
    box.setWindowOpacity(0.9)

    box.exec_()


def raise_success(title, message):
    box = QtGui.QMessageBox(QtGui.QMessageBox.Information, title,
                            message, QtGui.QMessageBox.Ok,
                            parent=FWindow.window)
    box.setWindowOpacity(0.9)
    box.exec_()


def formatted_number(number, sep="."):
    """ """
    locale_name, encoding = locale.getlocale()
    locale.setlocale(locale.LC_ALL, 'fra')
    fmt = "%s"
    if (isinstance(number, int)):
        fmt = u"%d"
    elif(isinstance(number, float)):
        fmt = u"%.2f"

    try:
        return locale.format(fmt, number, grouping=True).decode(encoding)
    except AttributeError:
        return locale.format(fmt, number, grouping=True)
    except Exception as e:
        print(e)
        return "%s" % number


class SystemTrayIcon(QtGui.QSystemTrayIcon):

    def __init__(self, mss, parent=None):

        QtGui.QSystemTrayIcon.__init__(self, parent)

        self.setIcon(QtGui.QIcon.fromTheme("document-save"))

        self.activated.connect(self.click_trap)
        # self.mss = ("Confirmation", "Mali rapou!!!!")
        self.show(mss)

    def click_trap(self, value):
        # left click!
        if value == self.Trigger:
            self.left_menu.exec_(QtGui.QCursor.pos())

    def welcome(self):
        self.showMessage(self.mss[0], self.mss[1])

    def show(self, mss):
        self.mss = mss
        QtGui.QSystemTrayIcon.show(self)
        QtCore.QTimer.singleShot(1000, self.welcome)


def is_float(val):
    try:
        val = val.replace(',', '.').replace(' ', '').replace('\xa0', '')
        return float(val)
    except Exception as e:
        print("is_float", e)
        return 0


def is_int(val):

    try:
        val = str(val).split()
        v = ''
        for i in val:
            v += i
        return int(v)
    except Exception as e:
        # print("is_int", e)
        return 0


def alerte():
    pass


def format_date(dat):
    dat = str(dat)
    day, month, year = dat.split('/')
    return '-'.join([year, month, day])


def date_to_ts(date):
    return mktime(strptime(date.strftime(
        "%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S"))


def to_jstimestamp(adate):
    if not adate:
        return int(to_timestamp(adate)) * 1000


def to_timestamp(dt):
    """
    Return a timestamp for the given datetime object.
    """
    if not dt:
        return (dt - datetime(1970, 1, 1)).total_seconds()


def copy_file(dest, path_filename):
    """ Copy the file, rename file in banc and return new name of the doc
        created folder banc doc if not existe
    """
    import shutil
    dest = os.path.join(os.path.dirname(os.path.abspath('__file__')), dest)
    filename = os.path.basename(path_filename)
    if not os.path.exists(dest):
        os.makedirs(dest)
    shutil.copyfile(path_filename, get_path(dest, filename))

    return rename_file(dest, filename, slug_mane_file(filename))


def rename_file(path, old_filename, new_filename):
    """ Rename file in banc docs  params: old_filename, new_filename
        return newname"""
    os.rename(get_path(path, old_filename),
              get_path(path, new_filename))
    return new_filename


def get_path(path, filename):
    return os.path.join(path, filename)


def slug_mane_file(file_name):
    return u"{timestamp}_{fname}".format(
        fname=file_name.replace(" ", "_"),
        timestamp=to_jstimestamp(datetime.now()))


def normalize(s):
    if type(s) == unicode:
        return s.encode('utf8', 'ignore')
    else:
        return str(s)


def str_date_split(date):
    try:
        return date.split('/')
    except AttributeError:
        return date.day, date.month, date.year


def date_on_or_end(dat, on=True):
    day, month, year = str_date_split(dat)
    if on:
        hour, second, micro_second = 0, 0, 0
    else:
        hour, second, micro_second = 23, 59, 59
    return datetime(int(year), int(month), int(day), int(hour),
                    int(second), int(micro_second))


def show_date(dat, time=True):
    if isinstance(dat, str):
        dat = date_to_datetime(dat)
    if not dat:
        return "pas de date"
    return dat.strftime(
        u"%d %b %Y à %Hh:%Mmn") if time else dat.strftime("%d %b %Y")


def date_to_datetime(dat):
    "reçoit une date return une datetime"
    day, month, year = str_date_split(dat)
    dt = datetime.now()
    return datetime(int(year), int(month), int(day),
                    int(dt.hour), int(dt.minute),
                    int(dt.second), int(dt.microsecond))


def getlog(text):
    return "Log-{}".format(text)


def internet_on(url):
    from urllib.request import urlopen, URLError
    try:
        urlopen(url, timeout=1)
        return True
    except URLError as err:
        print(err)
        return False
    except Exception as e:
        print(e)


def is_valide_mac():
    """ check de license """
    from Common.models import License
    lcse = CConstants.IS_EXPIRED
    try:
        lcse = License.get(License.code == str(make_lcse())).can_use()
    except Exception as e:
        print("/!\ invalide license.")
        print(e)

    return lcse


def clean_mac():
    return getnode()


def make_lcse(lcse=clean_mac()):
    # print("lcse:", lcse)
    lcse = hashlib.md5(str(lcse).encode('utf-8')).hexdigest()
    return lcse


def get_lcse_of_file():
    return open("{}".format(get_lcse_file()), 'r').read()


def get_lcse_file():
    return os.path.join(os.path.dirname(
        os.path.abspath('__file__')), 'LICENCE')
