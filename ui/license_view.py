#!usr/bin/env python
# -*- coding: utf8 -*-
# maintainer: Fad
from __future__ import (unicode_literals, absolute_import, division, print_function)

from sqlite3 import IntegrityError
from PyQt4.QtGui import (QHBoxLayout, QGridLayout, QGroupBox, QIcon, QPixmap,
                         QDialog, QLabel, QTextEdit)

from Common.cstatic import CConstants
from model import SettingsAdmin
from Common.ui.util import raise_success, raise_error
from Common.ui.common import (IntLineEdit, F_Widget, Button_save, F_PageTitle,
                              LineEdit, Button, FormLabel, PyTextViewer)


class LicenseViewWidget(QDialog, F_Widget):
    def __init__(self, parent=0, *args, **kwargs):
        QDialog.__init__(self, parent, *args, **kwargs)

        self.intro = FormLabel(u"<h3>Vous devez activé la license pour pouvoir"
                               u"<i>utiliser.</i></h3>")
        self.title = F_PageTitle("")
        self.title.setStyleSheet(""" background:
                                 url({}) no-repeat scroll 200px 50px #fff;
                                 border-radius: 14px 14px 8px 8px;
                                 border: 10px double #fff;
                                 width: 100%; height: auto;
                                 padding: 3.3em 1em 1em 100px;
                                 font: 12pt 'URW Bookman L';""".format(CConstants.APP_LOGO))

        vbox = QHBoxLayout()
        vbox.addWidget(self.title)
        self.sttg = SettingsAdmin().select().where(SettingsAdmin.id==1).get()
        if self.sttg.can_use():
            self.showLicenseGroupBox()
            vbox.addWidget(self.topLeftGroupBox)
            self.setLayout(vbox)
        else:
            self.activationGroupBox()
            vbox.addWidget(self.topLeftGroupBoxBtt)
            self.setLayout(vbox)

    def showLicenseGroupBox(self):

        self.intro = FormLabel(u"""<hr> <i> Elle est n'est valable que pour cette machine</i>
                                        <p><b>proprièteur:</b> {name}</p>
                                        <p><b>date d'activation:</b> {date}</p><hr>
                                        <p><b>License:</b> {license}</p>
                                        <p><b>Merci.</b></li>
                                """.format(name=self.sttg.user,
                                           date=self.sttg.date.strftime('%x'),
                                           license=self.sttg.license))
        self.topLeftGroupBox = QGroupBox(self.tr("License est activé"))
        gridbox = QGridLayout()

        cancel_but = Button(u"Ok")
        cancel_but.clicked.connect(self.cancel)
        # grid layout
        gridbox.addWidget(self.intro, 0, 1)
        gridbox.addWidget(cancel_but, 4, 1)

        # gridbox.setColumnStretch(2, 1)
        # gridbox.setRowStretch(0, 2)
        gridbox.setRowStretch(4, 0)

        self.topLeftGroupBox.setLayout(gridbox)

    def activationGroupBox(self):
        self.topLeftGroupBoxBtt = QGroupBox(self.tr("Nouvelle license"))
        self.setWindowTitle(u"License")
        self.parentWidget().setWindowTitle(u"Activation de la license")

        self.code_field = PyTextViewer(u"""Vous avez besoin du code ci desous
                                           pour l'activation:<hr> <b>{code}</b><hr>
                                           <h4>Contacts:</h4>{contact}"""
                                        .format(code=SettingsAdmin().select().get().clean_mac,
                                         contact=CConstants.TEL_AUT))
        self.name_field = LineEdit()
        self.license_field = QTextEdit()
        self.pixmap = QPixmap("")
        self.image = QLabel(self)
        self.image.setPixmap(self.pixmap)

        butt = Button_save(u"Enregistrer")
        butt.clicked.connect(self.add_lience)

        cancel_but = Button(u"Annuler")
        cancel_but.clicked.connect(self.cancel)

        editbox = QGridLayout()
        editbox.addWidget(QLabel(u"Nom: "), 0, 0)
        editbox.addWidget(self.name_field, 0, 1)
        editbox.addWidget(QLabel(u"License: "), 1, 0)
        editbox.addWidget(self.license_field, 1, 1)
        editbox.addWidget(self.code_field, 1, 2)
        editbox.addWidget(self.image, 5, 1)
        editbox.addWidget(butt, 6, 1)
        editbox.addWidget(cancel_but, 6, 0)

        self.topLeftGroupBoxBtt.setLayout(editbox)

    def cancel(self):
        self.close()

    def check_license(self, license):

        self.flog = False

        if (SettingsAdmin().is_valide_mac(license)):
            self.pixmap = QPixmap(u"{}accept.png".format(CConstants.img_cmedia))
            self.image.setToolTip("License correct")
            self.flog = True
        else:
            self.pixmap = QPixmap(u"{}decline.png".format(CConstants.img_cmedia))
            self.image.setToolTip("License incorrect")
        self.image.setPixmap(self.pixmap)

    def add_lience(self):
        """ add User """
        name = unicode(self.name_field.text()).strip()
        license = unicode(self.license_field.toPlainText())
        self.check_license(license)

        if self.flog:
            sttg = self.sttg
            sttg.user = name
            sttg.license = license
            sttg.save()
            self.cancel()
            raise_success(u"Confirmation",
                          u"""La license (<b>{}</b>) à éte bien enregistré pour cette
                           machine.\n
                           Elle doit être bien gardé""".format(license))
