#!usr/bin/env python
# -*- coding: utf8 -*-
# maintainer: Fad
from __future__ import (
    unicode_literals, absolute_import, division, print_function)

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QComboBox, QVBoxLayout, QCheckBox,
                             QFormLayout, QDialog)
from peewee import IntegrityError
from Common.cstatic import CConstants
from Common.ui.util import check_is_empty, field_error, check_field
from Common.models import Owner

from Common.ui.common import (
    IntLineEdit, FWidget, Button_save, LineEdit, Button, FLabel)

try:
    unicode
except:
    unicode = str


class NewOrEditUserViewWidget(QDialog, FWidget):

    def __init__(self, pp=None, owner=None, parent=None, *args, **kwargs):
        QDialog.__init__(self, parent, *args, **kwargs)

        self.setWindowTitle(u"Nouvel utilisateur")
        self.parent = parent
        self.pp = pp
        self.owner = owner

        vbox = QVBoxLayout()
        formbox = QFormLayout()
        self.checked = QCheckBox("Active")
        self.error_mssg = ""
        msg = u"Cocher si vous voulez que cet utilisateur puisse se connecter"
        if self.owner:
            self.new = False
            self.title = u"Modification de l'utilisateur {}".format(
                self.owner.username)
            self.succes_msg = u"L'utilisateur a été bien mise à jour"
            if self.owner.isactive:
                self.checked.setCheckState(Qt.Checked)
        else:
            self.checked.setCheckState(Qt.Checked)
            self.new = True
            self.succes_msg = u"L'utilisateur a été bien enregistré"
            self.title = u"Création d'un nouvel utilisateur"
            self.owner = Owner()
        # self.checked.setToolTip(msg)
        self.setWindowTitle(self.title)

        self.username_field = LineEdit(self.owner.username)
        self.username_field.setEnabled(self.new)
        self.password_field = LineEdit()
        self.password_field.setEchoMode(LineEdit.PasswordEchoOnEdit)
        self.password_field_v = LineEdit()
        self.password_field_v.setEchoMode(LineEdit.PasswordEchoOnEdit)
        self.password_field_v.textChanged.connect(
            self.check_password_is_valide)
        self.phone_field = IntLineEdit(self.owner.phone)

        self.liste_group = [Owner.ADMIN, Owner.USER]
        # Combobox widget
        self.box_group = QComboBox()
        for index in self.liste_group:
            self.box_group.addItem(u'%(group)s' % {'group': index})

        butt = Button_save(u"Enregistrer")
        butt.clicked.connect(self.add_or_edit_user)
        cancel_but = Button(u"Annuler")
        cancel_but.clicked.connect(self.cancel)

        formbox.addRow(FLabel(u"Identifiant"), self.username_field)
        formbox.addRow(FLabel(u"Mot de passe"), self.password_field)
        if self.new:
            formbox.addRow(
                FLabel(u"Verification du Mot de passe"), self.password_field_v)
        formbox.addRow(FLabel(u"Numero de Téléphone"), self.phone_field)
        formbox.addRow(FLabel(u"Groupe"), self.box_group)
        formbox.addRow(cancel_but, butt)
        vbox.addWidget(self.checked)
        vbox.addLayout(formbox)
        self.setLayout(vbox)

    def cancel(self):
        self.close()

    def is_valide(self):
        # print("isactive")
        if (check_is_empty(self.username_field)):
            return False
        if (check_is_empty(self.password_field)):
            return False
        if (self.new and check_is_empty(self.password_field_v)):
            return False
        if (not self.check_password_is_valide()):
            return False
        return True

    def check_password_is_valide(self):

        self.password = str(self.password_field.text())
        self.password_v = str(
            self.password_field_v.text()) if self.new else self.owner.password

        if check_field(self.password_field_v,
                       "Les mots de passe sont differents" if self.new else "Mot de passe incorrect", self.password != self.password_v):
            return
        return True

    def add_or_edit_user(self):
        # print(""" add User """)
        if not self.is_valide():
            print("is not valide")
            return

        username = str(self.username_field.text()).strip()
        password = str(self.password_field.text()).strip()
        phone = str(self.phone_field.text())
        group = self.liste_group[self.box_group.currentIndex()]
        status = False
        if self.checked.checkState() == Qt.Checked:
            status = True

        ow = self.owner
        ow.username = username
        ow.password = Owner().crypt_password(
            password) if self.new else password

        ow.phone = phone
        ow.group = group
        ow.isactive = status
        try:
            ow.save()
            self.close()
            self.accept()
            if self.pp:
                self.pp.refresh_()
                self.parent.Notify("L'identifiant %s a été enregistré" %
                                   ow.username, "success")
        except IntegrityError as e:
            field_error(
                self.name_field, u"L'utilisateurs %s existe déjà dans la base de donnée" % ow.username)
        # else:
        #     self.parent.Notify(
        #         "<h3>Formulaire non valide</h3> " + self.error_mssg, u"error")
