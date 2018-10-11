#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: Fad
from __future__ import (
    unicode_literals, absolute_import, division, print_function)

import shutil
import errno
import os

from datetime import datetime

from PyQt5.QtWidgets import QFileDialog, QWidget
from Common.models import DB_FILE, Version

from configuration import Config

from Common.ui.util import raise_success, raise_error, uopen_file, get_lcse_file

DATETIME = "{}".format(datetime.now().strftime('%d-%m-%Y-%Hh%M'))


def export_database_as_file():
    destination = QFileDialog.getSaveFileName(
        QWidget(), u"Sauvegarder la base de Donnée.",
        u"Sauvegarde du {} {}.db".format(DATETIME, Config.NAME_ORGA), "*.db")
    if not destination:
        return None
    try:
        shutil.copyfile(DB_FILE, destination)
        Version().get(id=1).update_v()
        raise_success(
            u"Les données ont été exportées correctement.",
            u"Conservez ce fichier précieusement car il contient \
            toutes vos données.\n Exportez vos données régulièrement.")
    except IOError:
        raise_error(u"La base de données n'a pas pu être exportée.",
                    u"Vérifiez le chemin de destination puis re-essayez.\n\n \
                     Demandez de l'aide si le problème persiste.")


def export_backup(folder=None, dst_folder=None):
    print("Exporting ...")
    directory = str(QFileDialog.getExistingDirectory(
        QWidget(), "Select Directory"))
    path_backup = u"{path}-{date}-{name}".format(path=os.path.join(
        directory, 'BACKUP'), date=DATETIME, name=Config.NAME_ORGA)

    if not directory:
        return None
    try:
        # TODO Savegarde version incremat de in db
        shutil.copyfile(DB_FILE, os.path.join(path_backup, DB_FILE))
        v = Version().get(id=1).update_v()
    except IOError:
        print("Error of copy database file")
    except Exception as e:
        print(e)

    try:
        if folder:
            copyanything(folder, os.path.join(path_backup, dst_folder))
        raise_success(u"Le backup à été fait correctement.",
                      u"""Conservez le dossier {} précieusement car il contient
                       toutes vos données. Exportez vos données régulièrement.
                      """.format(path_backup))
    except OSError as e:
        raise_error(u"Le backup n'a pas pu être fait correctement.",
                    u"Vérifiez le chemin de destination puis re-essayez.\n\n \
                     Demandez de l'aide si le problème persiste.")


def import_backup(folder=None, dst_folder=None):
    path_db_file = os.path.join(os.path.dirname(
        os.path.abspath('__file__')), DB_FILE)
    shutil.copy(path_db_file, "{}__{}.old".format(DB_FILE, DATETIME))
    name_select_f = QFileDialog.getOpenFileName(
        QWidget(), "Open Data File", "", "CSV data files (*.db)")
    shutil.copy(name_select_f, path_db_file)

    raise_error(u"Restoration des Donnée.",
                u"""Les données ont été correctement restorée
                    La version actualle de la base de donnée est {}
                    """.format(Version().get(id=1).display_name()))


def copyanything(src, dest):
    try:
        shutil.copytree(src, dest, ignore=None)
    except OSError as e:
        # If the error was caused because the source wasn't a directory
        if e.errno == errno.ENOTDIR:
            shutil.copy(src, dest)
        else:
            print(u'Directory not copied. Error: %s' % e)


def export_license_as_file():

    # from Common.models import SettingsAdmin
    # fil = os.path.join(os.path.dirname(os.path.abspath('__file__')), LICENCE)
    # settg = SettingsAdmin().get(id=1)
    fil = get_lcse_file()
    uopen_file(fil)
