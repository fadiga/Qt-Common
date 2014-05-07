#!usr/bin/env python
# -*- coding: utf8 -*-
# maintainer: Fad
from __future__ import (unicode_literals, absolute_import, division, print_function)

# from sqlite3 import IntegrityError
from PyQt4.QtGui import (QHBoxLayout, QGridLayout, QGroupBox, QPixmap,
                         QDialog, QLabel, QTextEdit)

from Common.cstatic import CConstants
from Common.models import SettingsAdmin
from Common.exports import export_license_as_file
from Common.ui.util import raise_success
from Common.ui.common import (F_Widget, Button_save, F_PageTitle,
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
        if self.sttg.can_use:
            self.showLicenseGroupBox()
            vbox.addWidget(self.topLeftGroupBox)
            self.setLayout(vbox)
        else:
            self.activationGroupBox()
            vbox.addWidget(self.topLeftGroupBoxBtt)
            self.setLayout(vbox)

    def showLicenseGroupBox(self):

        self.intro = FormLabel(u"""<hr> <i> Elle est n'est valable que pour cette machine</i>
                                        <p><b>proprièteur: </b> {name}</p>
                                        <p><b>date d'activation:</b> {date}</p><hr>
                                        <p><b>Merci.</b></li>
                                """.format(name=self.sttg.user,
                                           date=self.sttg.date.strftime('%c')))
        self.topLeftGroupBox = QGroupBox(self.tr("License est activé"))
        gridbox = QGridLayout()

        cancel_but = Button(u"OK")
        cancel_but.clicked.connect(self.cancel)
        remove_lcce = Button(u"Supprimer la license")
        remove_lcce.clicked.connect(self.remove_license)
        export_lcce = Button(u"Exporter la license")
        export_lcce.clicked.connect(self.export_license)
        # grid layout
        gridbox.addWidget(self.intro, 0, 1)
        gridbox.addWidget(cancel_but, 0, 2)
        gridbox.addWidget(export_lcce, 4, 1)
        gridbox.addWidget(remove_lcce, 4, 2)

        # gridbox.setColumnStretch(2, 1)
        # gridbox.setRowStretch(4, 1)
        gridbox.setRowStretch(4, 0)

        self.topLeftGroupBox.setLayout(gridbox)

    def activationGroupBox(self):
        self.topLeftGroupBoxBtt = QGroupBox(self.tr("Nouvelle license"))
        self.setWindowTitle(u"License")
        # self.parentWidget().setWindowTitle(u"Activation de la license")

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

    def remove_license(self):
        sttg = self.sttg
        print(sttg)
        sttg.tolerance = 0
        sttg.license = None
        sttg.save()
        self.cancel()
        raise_success("Suppression de la license",
                     u"La license a été bien supprimée")

    def check_license(self, license):

        self.flog = False
        if (SettingsAdmin().is_valide_mac(license)):
            icon = u"{}accept.png"
            msg = "License correct"
            self.flog = True
        else:
            icon = u"{}decline.png"
            msg = "License incorrect"
        self.image.setPixmap(QPixmap(icon.format(CConstants.img_cmedia)))
        self.image.setToolTip(msg)

    def export_license(self):
        export_license_as_file()

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
                           machine.\n Elle doit être bien gardé""".format(license))
            open("licence.txt", "r")
            self.accept()
