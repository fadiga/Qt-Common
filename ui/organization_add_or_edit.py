#!usr/bin/env python
# -*- coding: utf8 -*-
# maintainer: Fad
from __future__ import (
    unicode_literals, absolute_import, division, print_function)

from PyQt4.QtCore import Qt
from PyQt4.QtGui import (QComboBox, QVBoxLayout, QCheckBox, QGroupBox,
                         QFormLayout, QDialog, QTextEdit)
# from peewee import IntegrityError
from Common.ui.util import check_is_empty
from Common.models import Settings

from Common.ui.common import (
    IntLineEdit, FWidget, Button_save, LineEdit, FormLabel)

try:
    unicode
except:
    unicode = str


class NewOrEditSettingsViewWidget(QDialog, FWidget):

    def __init__(self, pp=None, owner=None, parent=None, *args, **kwargs):
        QDialog.__init__(self, parent, *args, **kwargs)

        self.setWindowTitle(u"Nouvel Organisation")
        self.parent = parent
        self.pp = pp
        self.owner = owner

        vbox = QVBoxLayout()

        self.organization_group_box()
        vbox.addWidget(self.organGroupBoxBtt)
        self.setLayout(vbox)

    def organization_group_box(self):
        self.organGroupBoxBtt = QGroupBox(self.tr("Nouvelle Organisation"))

        self.liste_devise = Settings.DEVISE
        # Combobox widget
        self.box_devise = QComboBox()
        for index in self.liste_devise:
            self.box_devise.addItem("{} {}".format(
                self.liste_devise[index], index))

        self.checked = QCheckBox("Active")
        self.checked.setChecked(True)
        self.checked.setToolTip(u"""Cocher si vous voulez pour deactive
                                le login continue à utiliser le systeme""")
        # self.name_orga = LineEdit()
        self.phone = IntLineEdit()
        self.bp = LineEdit()
        self.adress_org = QTextEdit()
        self.email_org = LineEdit()

        formbox = QFormLayout()
        # formbox.addRow(FormLabel(u"Nom de l'organisation *"), self.name_orga)
        formbox.addRow(FormLabel(u"Tel *"), self.phone)
        formbox.addRow(
            FormLabel(u"Activer la saisie de mot de passe"), self.checked)
        formbox.addRow(FormLabel(u"Devise"), self.box_devise)
        formbox.addRow(FormLabel(u"B.P"), self.bp)
        formbox.addRow(FormLabel(u"E-mail:"), self.email_org)
        formbox.addRow(FormLabel(u"Adresse complete:"), self.adress_org)

        butt = Button_save(u"Enregistrer")
        butt.clicked.connect(self.save_edit)
        formbox.addRow("", butt)

        self.organGroupBoxBtt.setLayout(formbox)

    def save_edit(self):
        ''' add operation '''
        # if check_is_empty(self.name_orga):
        #     return
        # if check_is_empty(self.phone):
        #     return
        # name_orga = str(self.name_orga.text())
        device = str(self.box_devise.currentText().split()[1])
        bp = str(self.bp.text())
        email_org = str(self.email_org.text())
        phone = str(self.phone.text())
        adress_org = str(self.adress_org.toPlainText())

        org = Settings()
        org.phone = phone
        org.device = device
        # org.name_orga = name_orga
        org.email_org = email_org
        org.bp = bp
        org.adress_org = adress_org
        org.is_login = True if self.checked.checkState(
        ) == Qt.Checked else False
        org.save()
        self.accept()
