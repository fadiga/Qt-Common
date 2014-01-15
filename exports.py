#!/usr/bin/env python
# encoding=utf-8
# maintainer: Fad
from __future__ import (unicode_literals, absolute_import, division, print_function)

import shutil
from datetime import datetime

from PyQt4 import QtGui
from models import DB_FILE

from configuration import Config

from common.ui.util import raise_success, raise_error

DATETIME = u"{}".format(unicode(datetime.now().strftime('%d-%m-%Y %Hh%M')))


def export_database_as_file():
    destination = QtGui.QFileDialog \
                       .getSaveFileName(QtGui.QWidget(),
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


# def export_as_excel(name, data):
#     try:
#         from tools.export_xls import main_as_excel
#     except ImportError:
#         raise_error("/!\ Import Erreur d'import", "Vérifiez si la fonction \
#                     'main_as_excel existe dans le export_xls'")

#     destination = QtGui.QFileDialog \
#                        .getSaveFileName(QtGui.QWidget(), u"Save Excel Export as...",
#                                         u"{} {}.xls".format(DATETIME,  Config.NAME_ORGA), "*.xls")
#     if not destination:
#         return False
#     try:
#         main_as_excel(destination, name, data)
#         raise_success(u"Success", u"La facture a été exportées correctement.")
#     except IOError:
#         raise_error(u"La facture n'a pas pu être exportée.",
#                     u"Vérifiez le chemin de destination puis re-essayez.\n\n \
#                      Demandez de l'aide si le problème persiste.")
