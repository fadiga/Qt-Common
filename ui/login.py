#!/usr/bin/env python
# -*- coding: utf8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu
# maintainer: Fad
from __future__ import (unicode_literals, absolute_import, division, print_function)

from sqlite3 import IntegrityError
from PyQt4.QtGui import (QHBoxLayout, QGridLayout, QGroupBox, QIcon, QPixmap,
                         QPushButton, QDialog, QLabel, QComboBox, QTextEdit)

from Common.cstatic import CConstants
from Common.ui.common import (FMainWindow, F_PageTitle, FormLabel, PyTextViewer,
                              EnterTabbedLineEdit, ErrorLabel,
                              Button_save, LineEdit, Button)
from Common.ui.util import raise_error, raise_success
from models import Owner, SettingsAdmin
from configuration import Config


class LoginWidget(QDialog, FMainWindow):

    title = u"Identification"

    def __init__(self):
        QDialog.__init__(self)
        self.setWindowTitle(Config.NAME_ORGA + u"    LOGIN")

        self.intro = FormLabel(u"<h3>Vous devez vous identifier pour pouvoir<h3>"
                               u"<i>utiliser {}.</i>".format(Config.NAME_ORGA))
        self.title = F_PageTitle(u"""<h4>{app_org}</h4>
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
        vbox.addWidget(self.title)

        self.sttg = SettingsAdmin.select().where(SettingsAdmin.id==1).get()
        if not self.sttg.can_use():
            self.activationGroupBox()
            vbox.addWidget(self.topLeftGroupBoxBtt)
            self.setLayout(vbox)

        elif Owner().filter(isvisible=True, isactive=True).count() == 0:
            self.createNewUserGroupBox()
            vbox.addWidget(self.topLeftGroupBoxBtt)
            self.setLayout(vbox)
        else:
            self.loginUserGroupBox()
            vbox.addWidget(self.topLeftGroupBox)
            # set focus to username field
            self.setFocusProxy(self.username_field)
            self.setLayout(vbox)

    def activationGroupBox(self):
        self.topLeftGroupBoxBtt = QGroupBox(self.tr("Nouvelle license"))
        self.setWindowTitle(u"License")
        self.setWindowTitle(u"Activation de la license")

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

    def loginUserGroupBox(self):
        self.topLeftGroupBox = QGroupBox(self.tr("Identification"))

        self.liste_username = Owner.select().where((Owner.isvisible==True))
        #Combobox widget
        self.box_username = QComboBox()
        for index in self.liste_username:
            self.box_username.addItem(u'%(username)s' % {'username': index})

        # username field
        # self.username_field = EnterTabbedLineEdit()
        self.username_field = self.box_username
        self.username_label = FormLabel(u"&Identifiant")
        self.username_label.setBuddy(self.username_field)
        self.username_error = ErrorLabel(u"")

        # password field
        self.password_field = EnterTabbedLineEdit()
        self.password_field.setEchoMode(LineEdit.Password)
        # self.password_field.setEchoMode(LineEdit.PasswordEchoOnEdit)
        self.password_label = FormLabel(u"&Mot de &passe")
        self.password_label.setBuddy(self.password_field)
        self.password_error = ErrorLabel(u"")

        # login button
        self.login_button = QPushButton(u"&S'identifier")
        self.login_button.setIcon(QIcon.fromTheme('save',
                                  QIcon(u"{}login.png".format(Config.img_cmedia))))
        self.login_button.setAutoDefault(True)
        self.login_button.clicked.connect(self.ckecklogin)

        # login error
        self.login_error = ErrorLabel("")

        gridbox = QGridLayout()

        # grid layout
        # gridbox.addWidget(self.intro, 0, 1)
        gridbox.addWidget(self.username_label, 1, 0)
        gridbox.addWidget(self.username_field, 1, 1)
        gridbox.addWidget(self.username_error, 1, 2)
        gridbox.addWidget(self.password_label, 2, 0)
        gridbox.addWidget(self.password_field, 2, 1)
        gridbox.addWidget(self.password_error, 2, 2)
        gridbox.addWidget(self.login_button, 3, 1)
        gridbox.addWidget(self.login_error, 4, 1)

        gridbox.setColumnStretch(2, 1)
        gridbox.setRowStretch(0, 2)
        gridbox.setRowStretch(4, 2)

        self.topLeftGroupBox.setLayout(gridbox)

    def createNewUserGroupBox(self):
        self.topLeftGroupBoxBtt = QGroupBox(self.tr("Nouvel utilisateur"))

        self.setWindowTitle(u"Création d'un nouvel utilisateur")

        self.username_field = LineEdit()
        self.password_field = LineEdit()
        self.password_field.setEchoMode(LineEdit.Password)
        # self.password_field.setEchoMode(LineEdit.PasswordEchoOnEdit)
        self.password_field_v = LineEdit()
        self.password_field_v.setEchoMode(LineEdit.Password)
        self.password_field_v.textChanged.connect(self.check_password)
        # self.phone_field = IntLineEdit()
        self.pixmap = QPixmap("")
        self.image = QLabel(self)
        self.image.setPixmap(self.pixmap)

        self.liste_group = [u"user", u"admin"]
        #Combobox widget
        self.box_group = QComboBox()
        for index in self.liste_group:
            self.box_group.addItem(u'%(group)s' % {'group': index})

        butt = Button_save(u"Enregistrer")
        butt.clicked.connect(self.add_user)
        cancel_but = Button(u"Annuler")
        cancel_but.clicked.connect(self.cancel)

        editbox = QGridLayout()
        editbox.addWidget(QLabel(u"Non d'utilisateur"), 0, 0)
        editbox.addWidget(self.username_field, 0, 1)
        editbox.addWidget(QLabel(u"Mot de passe"), 1, 0)
        editbox.addWidget(self.password_field, 1, 1)
        editbox.addWidget(QLabel(u"Verification du Mot de passe"), 2, 0)
        editbox.addWidget(self.password_field_v, 2, 1)
        editbox.addWidget(self.image, 2, 2)
        # editbox.addWidget(QLabel(u"Numero de Téléphone"), 4, 0)
        # editbox.addWidget(self.phone_field, 4, 1)
        editbox.addWidget(QLabel(u"Groupe"), 5, 0)
        editbox.addWidget(self.box_group, 5, 1)
        editbox.addWidget(butt, 6, 1)
        editbox.addWidget(cancel_but, 6, 0)

        self.topLeftGroupBoxBtt.setLayout(editbox)

    def cancel(self):
        self.close()

    def goto_home(self):
        from ui.home import HomeViewWidget
        self.change_context(HomeViewWidget)

    def goto_new_user(self):
        from Common.ui.new_user import NewUserViewWidget
        self.open_dialog(NewUserViewWidget, modal=True, go_home=True)

    def ckecklogin(self):
        """ """
        # username = unicode(self.username_field.text()).strip()
        username = unicode(self.liste_username[self.box_username.currentIndex()])
        password = unicode(self.password_field.text()).strip()
        password = Owner().crypt_password(password)
        # check completeness
        try:
            owner = Owner.get(Owner.islog==True)
            owner.islog = False
            owner.save()
        except:
            pass
        if not self.is_complete():
            return

        self.pixmap = QPixmap(u"{}warning.png".format(Config.img_cmedia))
        try:
            owner = Owner.select().where(Owner.username==username,
                                         Owner.password==password).get()
            owner.islog = True
        except:
            raise
            self.username_error.setToolTip("Identifiant ou mot de passe incorrect")
            self.username_error.setPixmap(self.pixmap)
            return False

        try:
            owner.save()
        except NameError as e:
            raise_error(u"Erreur", "%s" % e)
            return False
        except:
            raise_error(u"Erreur", "Veuillez relancer l'application")
            return False

        # Le droit de reset des mots de passes
        # Une page special
        # self.goto_home()

        self.accept()

    def is_complete(self):
        """ form has been completly filled or not. Sets error messages """

        complete = True

        # reset login error
        self.login_error.clear()
        # password is required
        if not self.password_field.text():
            self.password_error.setText(u"Le mot de passe est requis.")
            complete = False
        else:
            self.password_error.clear()
        return complete

    def check_password(self):

        self.flog = False

        if (unicode(self.password_field.text()) == unicode(self.password_field_v.text())):
            self.pixmap = QPixmap(u"{}accept.png".format(Config.img_cmedia))
            self.image.setToolTip("Mot de passe correct")
            self.flog = True
        else:
            self.pixmap = QPixmap(u"{}decline.png".format(Config.img_cmedia))
            self.image.setToolTip("Mot de passe sont incorrect")
        self.image.setPixmap(self.pixmap)

    def add_user(self):
        """ add User """
        username = unicode(self.username_field.text()).strip()
        password = unicode(self.password_field.text()).strip()
        password = Owner().crypt_password(password)
        # phone = unicode(self.phone_field.text())
        group = self.liste_group[self.box_group.currentIndex()]
        if (username != "" and password != ""):
            if self.flog:
                ow = Owner()
                ow.username = username
                ow.password = password
                # ow.phone = phone
                ow.group = group
                ow.islog=True
                try:
                    ow.save()
                    self.accept()
                    self.close()
                    # raise_success(u"Confirmation", u"L'utilisateurs %s "
                    #               u"a été enregistré" % ow.username)
                except IntegrityError:
                    raise
                    raise_error(u"Erreur", u"L'utilisateurs %s "
                                u"existe déjà dans la base de donnée" % ow.username)

        else:
            raise_error(u"Erreur", u"Tout les champs sont obligatoire")

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
            # file_lience = open("licence.txt", "r")

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


def john_doe():
    try:
        ow = Owner.get(Owner.username=="anomime")
    except:
        ow = Owner(username="anomime", password="anomime",
                   group="admin", last_login=0)
    ow.islog = True
    ow.save()
    return ow
