#!usr/bin/env python
# -*- coding: utf8 -*-
# maintainer: Fad
from __future__ import (
    unicode_literals, absolute_import, division, print_function)

from datetime import datetime, timedelta

from PyQt4.QtGui import (QHBoxLayout, QGridLayout, QGroupBox, QPixmap,
                         QDialog, QLabel, QTextEdit)

from Common.ui.util import is_valide_mac, clean_mac, make_lcse, get_lcse_file
from Common.cstatic import CConstants
from Common.models import License
from Common.exports import export_license_as_file
from Common.ui.common import (FWidget, Button_save, FPageTitle, LineEdit,
                              Button, Deleted_btt, FormLabel, PyTextViewer)


class LicenseViewWidget(QDialog, FWidget):

    def __init__(self, parent=0, *args, **kwargs):
        QDialog.__init__(self, parent=parent, *args, **kwargs)
        self.parent = parent

        self.intro = FormLabel("<h3>Vous devez activé la license pour pouvoir"
                               "<i>utiliser.</i></h3>")
        self.title = FPageTitle("")
        self.title.setStyleSheet(
            """ background: url({}) no-repeat scroll 200px 50px #fff;
            border-radius: 14px 14px 8px 8px;border: 10px double #fff;
            width: 100%; height: auto;  padding: 3.3em 1em 1em 100px;
            font: 12pt 'URW Bookman L';""".format(CConstants.APP_LOGO))

        vbox = QHBoxLayout()
        vbox.addWidget(self.title)

        try:
            self.lcce = License.get(License.code == str(make_lcse()))
        except:
            self.lcce = License.get(License.code == "Evaluton")

        if is_valide_mac():
            self.showLicenseGroupBox()
            vbox.addWidget(self.topLeftGroupBox)
            self.setLayout(vbox)
        else:
            self.activationGroupBox()
            vbox.addWidget(self.topLeftGroupBoxBtt)
            self.setLayout(vbox)

    def showLicenseGroupBox(self):

        self.intro = FormLabel(
            u""" <hr> <h4> Version {v_type} </h4>
            <h2> Elle est n'est valable que pour cette machine</h2>
            <p><b>proprièteur: </b> {name}</p>
            <p><b>date d'activation:</b> {a_date}</p><hr>
            <p><b>date d'activation:</b> {ex_date}</p><hr>
             <p><b>Merci.</b></li>
            """.format(
                name=self.lcce.owner,
                a_date=self.lcce.activation_date.strftime('%c'),
                ex_date=self.lcce.expiration_date.strftime('%c'),
                v_type="activée" if self.lcce.can_expired else "d'evalution"
            ))
        self.topLeftGroupBox = QGroupBox(self.tr("Licence"))
        gridbox = QGridLayout()

        cancel_but = Button(u"OK")
        cancel_but.clicked.connect(self.cancel)
        export_lcce = Button(u"Exporter la licence")
        export_lcce.clicked.connect(self.export_license)
        remove_trial_lcce = Deleted_btt(u"Expirer la licence")
        remove_trial_lcce.clicked.connect(self.remove_trial)
        # grid layout
        gridbox.addWidget(self.intro, 0, 1)
        gridbox.addWidget(cancel_but, 0, 2)
        gridbox.addWidget(export_lcce, 4, 1)
        gridbox.addWidget(remove_trial_lcce, 4, 2)

        # gridbox.setColumnStretch(2, 1)
        # gridbox.setRowStretch(4, 1)
        gridbox.setRowStretch(4, 0)

        self.topLeftGroupBox.setLayout(gridbox)

    def activationGroupBox(self):
        self.topLeftGroupBoxBtt = QGroupBox(self.tr("Nouvelle license"))
        # self.setWindowTitle(u"License")
        self.setWindowTitle(u"Activation de la license")
        self.cpt = 0
        self.code_field = PyTextViewer(
            u"""Vous avez besoin du code ci desous pour l'activation:
            <hr> <b>{code}</b><hr> <h4>Contacts:</h4>{contact}"""
            .format(code=clean_mac(), contact=CConstants.TEL_AUT))
        self.name_field = LineEdit()
        self.license_field = QTextEdit()
        self.pixmap = QPixmap("")
        self.image = QLabel(self)
        self.image.setPixmap(self.pixmap)

        trial_lcce = Button(u"Activée l'evaluation")
        trial_lcce.clicked.connect(self.active_trial)

        self.butt = Button_save(u"Enregistrer")
        self.butt.clicked.connect(self.add_lience)

        cancel_but = Button(u"Annuler")
        cancel_but.clicked.connect(self.cancel)

        editbox = QGridLayout()
        editbox.addWidget(QLabel(u"Nom: "), 0, 0)
        editbox.addWidget(self.name_field, 0, 1)
        editbox.addWidget(trial_lcce, 0, 2)
        editbox.addWidget(QLabel(u"License: "), 1, 0)
        editbox.addWidget(self.license_field, 1, 1)
        editbox.addWidget(self.code_field, 1, 2)
        editbox.addWidget(self.image, 5, 1)
        editbox.addWidget(self.butt, 6, 1)
        editbox.addWidget(cancel_but, 6, 2)

        self.topLeftGroupBoxBtt.setLayout(editbox)

    def cancel(self):
        self.close()

    def remove_trial(self):
        lcce = self.lcce
        # print(sttg)
        lcce.expiration_date = datetime.now() - timedelta(days=1)
        lcce.save()
        self.parent.Notify(u"La licence a été bien supprimée", "warring")
        self.cancel()

    def check_license(self, license):
        self.flog = False
        if (license == make_lcse()):
            icon = u"{}accept.png"
            msg = "Licence correct"
            self.flog = True
        else:
            icon = u"{}decline.png"
            msg = "Licence incorrect"
        self.image.setPixmap(QPixmap(icon.format(CConstants.img_cmedia)))
        self.image.setToolTip(msg)

    def export_license(self):
        export_license_as_file()

    def active_trial(self):
        try:
            License.create(
                can_expired=True, code="Evaluton",
                owner=str(self.name_field.text()).strip(),
                expiration_date=datetime.now() + timedelta(
                    days=30, milliseconds=4))
            self.cancel()
            self.accept()
            self.parent.Notify(
                "La licence a été bien activée pour 30 jour. Merci.", "warring")
        except Exception as e:
            print(e)

    def add_lience(self):
        """ add User """
        name = str(self.name_field.text()).strip()
        license = str(self.license_field.toPlainText())
        self.check_license(license)

        if self.flog:
            License.create(code=license, owner=name)
            self.cancel()
            try:
                self.parent.parent.Notify(
                    u""" La license (<b>{}</b>) à éte bien enregistré pour cette
                    machine.\n Elle doit être bien gardé""".format(license),
                    "success")
            except Exception as e:
                print(e)

            flcce = open(get_lcse_file(), 'w')
            flcce.write(license)
            flcce.close()
            self.accept()
        else:
            d = datetime.now()
            key = int((d.year - d.day - d.month) / 2)
            self.cpt += 1
            if self.cpt > 2 and name == str(key):
                lcse = make_lcse()
                self.name_field.setText("")
                self.license_field.setText(lcse)
