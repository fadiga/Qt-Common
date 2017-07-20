#!/usr/bin/env python
# -*- coding: utf8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu
# maintainer: Fad
from __future__ import (
    unicode_literals, absolute_import, division, print_function)

from PyQt4.QtGui import (QHBoxLayout, QGridLayout, QGroupBox, QIcon, QPixmap,
                         QPushButton, QDialog, QLabel, QComboBox, QTextEdit, QFormLayout)

from PyQt4.QtCore import Qt

from Common.cstatic import CConstants
from Common.ui.common import (FMainWindow, FPageTitle, FormLabel, PyTextViewer,
                              EnterTabbedLineEdit, ErrorLabel, FLabel,
                              Button_save, LineEdit, Button)
from Common.ui.util import check_is_empty, field_error
from Common.models import Owner, SettingsAdmin
from configuration import Config


class LoginWidget(QDialog, FMainWindow):

    title_page = u"Identification"

    def __init__(self, hibernate=False):
        QDialog.__init__(self)
        self.setWindowTitle(Config.NAME_ORGA + "    " + self.title_page)
        self.hibernate = hibernate

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.intro = FormLabel(u"<h3>Vous devez vous identifier pour pouvoir<h3>"
                               u"<i>utiliser {}.</i>".format(Config.NAME_ORGA))
        self.title = FPageTitle(u"""<h4>{app_org}</h4>
                                 <b><li>{app_name}</li> </b>
                                 <ol><li>{org}</li><li><b>Version:
                                 </b> {version}</li></ol>
                                 """.format(app_org=Config.NAME_ORGA,
                                            org=Config.ORG_AUT,
                                            version=Config.APP_VERSION,
                                            app_name=Config.APP_NAME))
        self.title.setStyleSheet(""" background:
                                 url({}) no-repeat scroll 200px 50px #fff;
                                 border-radius: 14px 14px 8px 8px;
                                 border: 10px double #fff;
                                 width: 100%; height: auto;
                                 padding: 3.3em 1em 1em 100px;
                                 font: 12pt 'URW Bookman L';""".format(Config.APP_LOGO))
        vbox = QHBoxLayout()

        # self.sttg = SettingsAdmin.select().where(SettingsAdmin.id == 1).get()
        # if not self.sttg.can_use:
        #     self.activationGroupBox()
        #     vbox.addWidget(self.topLeftGroupBoxBtt)
        #     self.setLayout(vbox)
        # else:
        self.loginUserGroupBox()
        vbox.addWidget(self.topLeftGroupBox)
        # set focus to username field
        self.setFocusProxy(self.username_field)
        self.setLayout(vbox)

    # def activationGroupBox(self):
    #     self.topLeftGroupBoxBtt = QGroupBox(self.tr("Nouvelle license"))
    #     self.setWindowTitle(u"License")
    #     self.setWindowTitle(u"Activation de la license")

    #     self.code_field = PyTextViewer(u"""Vous avez besoin du code ci desous
    #                                        pour l'activation:<hr> <b>{code}</b><hr>
    #                                        <h4>Contacts:</h4>{contact}"""
    #                                    .format(code=SettingsAdmin().select().get().clean_mac,
    #                                            contact=CConstants.TEL_AUT))
    #     self.name_field = LineEdit()
    #     self.license_field = QTextEdit()
    #     self.pixmap = QPixmap("")
    #     self.image = QLabel(self)
    #     self.image.setPixmap(self.pixmap)

    #     butt = Button_save(u"Enregistrer")
    #     butt.clicked.connect(self.add_lience)

    #     cancel_but = Button(u"Annuler")
    #     cancel_but.clicked.connect(self.cancel)

    #     editbox = QGridLayout()
    #     editbox.addWidget(QLabel(u"Nom: "), 0, 0)
    #     editbox.addWidget(self.name_field, 0, 1)
    #     editbox.addWidget(QLabel(u"License: "), 1, 0)
    #     editbox.addWidget(self.license_field, 1, 1)
    #     editbox.addWidget(self.code_field, 1, 2)
    #     editbox.addWidget(self.image, 5, 1)
    #     editbox.addWidget(butt, 6, 1)
    #     editbox.addWidget(cancel_but, 6, 0)

    #     self.topLeftGroupBoxBtt.setLayout(editbox)

    def loginUserGroupBox(self):
        self.topLeftGroupBox = QGroupBox(self.tr("Identification"))

        self.liste_username = Owner.select().where((Owner.isactive == True))
        # Combobox widget
        self.box_username = QComboBox()
        for index in self.liste_username:
            self.box_username.addItem(u'%(username)s' % {'username': index})

        # username field
        self.username_field = self.box_username
        # password field
        self.password_field = EnterTabbedLineEdit()
        self.password_field.setEchoMode(LineEdit.Password)
        self.password_field.setFocus()
        # login button
        self.login_button = QPushButton(u"&S'identifier")
        self.login_button.setIcon(
            QIcon.fromTheme('save', QIcon(u"{}login.png".format(Config.img_cmedia))))
        self.login_button.clicked.connect(self.login)

        self.cancel_button = QPushButton(u"&Fermer")
        self.cancel_button.clicked.connect(self.cancel)
        self.cancel_button.setFlat(True)

        # login error
        self.login_error = ErrorLabel("")

        formbox = QFormLayout()

        # grid layout
        formbox.addRow(FormLabel(u"Identifiant"), self.username_field)
        formbox.addRow(FormLabel(u"Mot de passe"), self.password_field)
        formbox.addRow(FormLabel(''), self.login_button)
        formbox.addRow(FormLabel(''), self.cancel_button)
        if self.hibernate:
            self.cancel_button.setEnabled(False)

        self.topLeftGroupBox.setLayout(formbox)

    def is_valide(self):
        if check_is_empty(self.password_field):
            return False
        return True

    def cancel(self):
        self.close()

    def login(self):
        """ """
        if not self.is_valide():
            print("is not valide")
            return

        username = str(self.liste_username[self.box_username.currentIndex()])
        password = Owner().crypt_password(
            str(self.password_field.text()).strip())
        # check completeness
        for ow in Owner.select().where(Owner.islog == True):
            ow.islog = False
            ow.save()
        try:
            owner = Owner.get(Owner.username == username,
                              Owner.password == password)
            owner.islog = True
            owner.save()
        except Exception as e:
            print(e)
            field_error(self.password_field, "Mot de passe incorrect")
            return False
        self.accept()

    # def add_lience(self):
    #     """ add User """
    #     name = str(self.name_field.text()).strip()
    #     license = str(self.license_field.toPlainText())
    #     self.check_license(license)

    #     if self.flog:
    #         License.create(code=license, owner=name)
    #         self.cancel()
    #         self.parent.Notify(u"""La license (<b>{}</b>) à éte bien enregistré pour cette
    #                     machine.\n Elle doit être bien gardé""".format(license), "success")
    #         # file_lience = open("licence.txt", "r")

    # def check_license(self, license):

    #     self.flog = False

    #     if (SettingsAdmin().is_valide_mac(license)):
    #         self.pixmap = QPixmap(
    #             u"{}accept.png".format(CConstants.img_cmedia))
    #         self.image.setToolTip("License correct")
    #         self.flog = True
    #     else:
    #         self.pixmap = QPixmap(
    #             u"{}decline.png".format(CConstants.img_cmedia))
    #         self.image.setToolTip("License incorrect")
    #     self.image.setPixmap(self.pixmap)
