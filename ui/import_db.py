#!/usr/bin/env python
# -*- coding: utf8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu
# maintainer: Fad
from __future__ import (
    unicode_literals, absolute_import, division, print_function)

from PyQt4.QtGui import (QHBoxLayout, QGroupBox, QIcon, QPushButton, QDialog,
                         QVBoxLayout, QFormLayout, QLabel)

from PyQt4.QtCore import Qt

from Common.ui.common import FMainWindow
from Common.exports import import_backup
from configuration import Config


class ImportBDWidget(QDialog, FMainWindow):

    title_page = u"Identification"

    def __init__(self, hibernate=False):
        QDialog.__init__(self)
        self.setWindowTitle(self.set_window_title(self.title_page))
        self.hibernate = hibernate

        self.setWindowFlags(Qt.FramelessWindowHint)
        vbox = QHBoxLayout()

        self.import_db_groupBox()
        title = QLabel()
        title.setTextFormat(Qt.RichText)
        title.setText("<img src={logo}><h4>{app_name}</h4><".format(
            app_name=Config.APP_NAME, logo=Config.APP_LOGO))

        title.setStyleSheet(
            """ background:#3a4055;color:#fff;border-radius: 14px 14px 8px 8px;
             border: 10px double #c8c8c8; width: 100%; height: auto; padding: 1em;""")
        vbox.addWidget(title)
        vbox.addWidget(self.topLeftGroupBox)
        self.setLayout(vbox)

    def import_db_groupBox(self):
        self.topLeftGroupBox = QGroupBox(self.tr("Import de base de données"))
        # login button
        self.login_button = QPushButton(u"&Importer base de données")
        self.login_button.setIcon(QIcon.fromTheme(
            'save', QIcon(u"{}base.png".format(Config.img_cmedia))))
        self.login_button.clicked.connect(self.goto_import_backup)

        self.cancel_button = QPushButton(u"Ignorer")
        # self.cancel_button.setIcon(QIcon.fromTheme(
        #     'save', QIcon(u"{}exit.png".format(Config.img_cmedia))))
        self.cancel_button.clicked.connect(self.cancel)
        self.cancel_button.setFlat(True)
        hbox = QVBoxLayout()
        hbox.addWidget(QLabel(
            'Veuillez choisir une ancienne sauvegarde de la base de données.<br> Pour la restauration des données.'))
        formbox = QFormLayout()
        # grid layout
        formbox.addRow(QLabel(''), self.login_button)
        formbox.addRow(QLabel(''), self.cancel_button)
        hbox.addLayout(formbox)
        self.topLeftGroupBox.setLayout(hbox)

    def goto_import_backup(self):
        import_backup(folder=Config.des_image_record,
                      dst_folder=Config.ARMOIRE)
        self.accept()
        self.close()

    def cancel(self):
        self.accept()
