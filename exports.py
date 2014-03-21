#!/usr/bin/env python
# encoding=utf-8
# maintainer: Fad
from __future__ import (unicode_literals, absolute_import, division, print_function)

import shutil, errno
import os

from datetime import datetime

from PyQt4.QtGui import QFileDialog, QWidget
from models import DB_FILE, Version

from configuration import Config

from Common.ui.util import raise_success, raise_error

DATETIME = u"{}".format(unicode(datetime.now().strftime('%d-%m-%Y %Hh%M')))


def export_database_as_file():
    destination = QFileDialog.getSaveFileName(QWidget(),
                            u"Sauvegarder la base de Donnée.",
                            u"Sauvegarde du {} {}.db"
                            .format(DATETIME, Config.NAME_ORGA), "*.db")
    if not destination:
        return None
    try:
        shutil.copyfile(DB_FILE, destination)
        raise_success(u"Les données ont été exportées correctement.",
                      u"Conservez ce fichier précieusement car il contient \
                       toutes vos données.\n Exportez vos données régulièrement.")
    except IOError:
        raise_error(u"La base de données n'a pas pu être exportée.",
                    u"Vérifiez le chemin de destination puis re-essayez.\n\n \
                     Demandez de l'aide si le problème persiste.")


def export_backup(folder=None, dst_folder=None):

    directory = str(QFileDialog.getExistingDirectory(QWidget(), "Select Directory"))
    path_backup = u"{path}-{date}-{name}".format(path=os.path.join(directory, 'BACKUP'), date=DATETIME, name=Config.NAME_ORGA)

    if not directory:
        return None
    try:
        if folder:
            copyanything(folder, os.path.join(path_backup, dst_folder))

        copyanything(DB_FILE, os.path.join(path_backup, DB_FILE))

        raise_success(u"Le backup à été fait correctement.",
                      u"""Conservez le dossier\n {}\n précieusement car il contient
                       toutes vos données. Exportez vos données régulièrement.
                      """.format(path_backup))
    except:
        raise_error(u"Le backup n'a pas pu être fait correctement.",
                    u"Vérifiez le chemin de destination puis re-essayez.\n\n \
                     Demandez de l'aide si le problème persiste.")


def import_backup():

    directory = str(QFileDialog.getExistingDirectory(QWidget(), "Select Directory"))
    raise_error(u"Le backup n'a pas pu être import.",
                u"""La fonctionalité n'a pas été activié.\n\n
                    La version actualle est {}""".format(Version().get(id=1).display_name()))


def copyanything(src, dest):
    try:
        shutil.copytree(src, dest, ignore=None)
    except OSError as e:
        # If the error was caused because the source wasn't a directory
        if e.errno == errno.ENOTDIR:
            shutil.copy(src, dest)
        else:
            print('Directory not copied. Error: %s' % e)
