#!usr/bin/env python
# -*- coding: utf8 -*-
# maintainer: Fad
from __future__ import unicode_literals, absolute_import, division, print_function

from datetime import datetime

# from PyQt4.QtCore import Qt
from PyQt4.QtGui import (
    QVBoxLayout,
    QGridLayout,
    QGroupBox,
    QDialog,
    QTextEdit,
    QFormLayout,
)

from Common.cstatic import CConstants
from Common.models import License
from Common.exports import export_license_as_file
from Common.ui.util import (
    clean_mac,
    make_lcse,
    get_lcse_file,
    check_is_empty,
    is_valide_codition_field,
)
from Common.ui.common import (
    FWidget,
    ButtonSave,
    LineEdit,
    PyTextViewer,
    DeletedBtt,
    Button,
    FormLabel,
)


class LicenseViewWidget(QDialog, FWidget):
    def __init__(self, parent=0, *args, **kwargs):
        QDialog.__init__(self, parent=parent, *args, **kwargs)
        self.parent = parent

        self.intro = FormLabel(
            "<h3>Vous devez activé la license pour pouvoir<i>utiliser.</i></h3>"
        )
        vbox = QVBoxLayout()
        try:
            self.lcse = License.get(License.code == str(make_lcse()))
            rep = self.lcse.can_use()
        except Exception as e:
            print(e)
            self.lcse = License()
            rep = CConstants.IS_EXPIRED
            # self.lcse = License.create(
            #     can_expired=True, code=make_lcse(), owner="Demo")
        rep = self.lcse.can_use()

        if rep == CConstants.IS_NOT_ACTIVATED or rep == CConstants.IS_EXPIRED:
            self.activation_group_box()
            vbox.addWidget(self.topLeftGroupBoxBtt)
            self.setLayout(vbox)
        else:
            self.show_license_group_box()
            vbox.addWidget(self.topLeftGroupBox)
            self.setLayout(vbox)

    def show_license_group_box(self):

        self.intro = FormLabel(
            u""" <hr> <h4> Version {v_type} </h4>
            <h2> Elle est n'est valable que pour cette machine</h2>
            <p><b>proprièteur: </b> {name} </p>
            <p><b>date d'activation:</b> {a_date} </p><hr>
            <p><b>date d'expiration:</b> {ex_date} </p><hr>
             <p><b>Merci.</b></li>
            """.format(
                name=self.lcse.owner,
                a_date=self.lcse.activation_date.strftime('%c'),
                ex_date="néant"
                if not self.lcse.can_expired
                else self.lcse.expiration_date.strftime('%c'),
                v_type="d'evalution" if self.lcse.can_expired else "activée",
            )
        )
        self.topLeftGroupBox = QGroupBox(self.tr("Licence"))
        gridbox = QGridLayout()

        cancel_but = Button(u"OK")
        cancel_but.clicked.connect(self.cancel)
        export_lcse = Button(u"Exporter la licence")
        export_lcse.clicked.connect(self.export_license)
        remove_trial_lcse = DeletedBtt(u"Expirer la licence")
        remove_trial_lcse.clicked.connect(self.remove_trial)
        # grid layout
        gridbox.addWidget(self.intro, 0, 1)
        gridbox.addWidget(cancel_but, 0, 2)
        gridbox.addWidget(export_lcse, 4, 1)
        gridbox.addWidget(remove_trial_lcse, 4, 2)

        # gridbox.setColumnStretch(2, 1)
        # gridbox.setRowStretch(4, 1)
        gridbox.setRowStretch(4, 0)

        self.topLeftGroupBox.setLayout(gridbox)

    def activation_group_box(self):
        self.topLeftGroupBoxBtt = QGroupBox(self.tr("Nouvelle license"))
        # self.setWindowTitle(u"License")
        self.setWindowTitle(u"Activation de la license")
        self.cpt = 0
        self.info_field = PyTextViewer(
            u"""Vous avez besoin du code ci desous pour l'activation:
            <hr> <b>{code}</b><hr> <h4>Contacts:</h4>{contact}""".format(
                code=clean_mac(), contact=CConstants.TEL_AUT
            )
        )
        self.name_field = LineEdit()
        self.license_field = QTextEdit()

        trial_lcse = Button(u"Activée l'evaluation")
        trial_lcse.clicked.connect(self.active_trial)
        if self.lcse.expiration_date:
            trial_lcse.setEnabled(False)

        self.butt = ButtonSave(u"Enregistrer")
        self.butt.clicked.connect(self.add_lience)

        cancel_but = Button(u"Annuler")
        cancel_but.clicked.connect(self.cancel)

        formbox = QFormLayout()
        formbox.addRow(FormLabel(""), self.info_field)
        formbox.addRow(FormLabel("Nom :"), self.name_field)
        formbox.addRow(FormLabel("Code license :"), self.license_field)
        formbox.addRow(FormLabel(""), trial_lcse)
        formbox.addRow(cancel_but, self.butt)
        self.topLeftGroupBoxBtt.setLayout(formbox)

    def cancel(self):
        self.close()

    def remove_trial(self):
        self.lcse.remove_activation()
        # self.parent.Notify(u"La licence a été bien supprimée", "warring")
        self.cancel()
        self.accept()

    def export_license(self):
        export_license_as_file()

    def active_trial(self):
        try:
            print("active_trial")
            self.lcse = License(can_expired=True, code=make_lcse(), owner="Demo")
            self.lcse.get_evaluation()
            self.cancel()
            self.accept()
            self.parent.Notify(
                "La licence a été bien activée pour 60 jour. Merci.", "warring"
            )
        except Exception as e:
            print(e)

    def add_lience(self):
        name = str(self.name_field.text()).strip()
        license = str(self.license_field.toPlainText())
        if check_is_empty(self.license_field):
            return
        m_lcse = make_lcse()
        if is_valide_codition_field(
            self.license_field, "Licence invalide", license != m_lcse
        ):
            d = datetime.now()
            key = int((d.year - d.day - d.month) / 2)
            self.cpt += 1
            print(key)
            if self.cpt > 2 and license == str(key):
                self.license_field.setText(m_lcse)

            return

        if check_is_empty(self.name_field):
            return
        self.lcse.can_expired = False
        self.lcse.owner = name
        if not self.lcse.code:
            self.lcse.code = license
        self.lcse.activation()

        flcse = open(get_lcse_file(), 'w')
        flcse.write(license)
        flcse.close()
        self.accept()
