#!/usr/bin/env python
# -*- coding: utf8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu
# maintainer: Fad
from __future__ import (unicode_literals, absolute_import, division, print_function)

from PyQt4.QtGui import (QHBoxLayout, QGridLayout, QGroupBox, QIcon, QPixmap,
                         QPushButton)

from Common.ui.common import (F_Widget, F_PageTitle, FormLabel, PyTextViewer,
                              EnterTabbedLineEdit, ErrorLabel, Button_menu,
                              Button_rond, LineEdit)
from Common.ui.util import raise_error
from model import Owner
from configuration import Config
from ui.home import HomeViewWidget


class LoginWidget(F_Widget):

    title = u"Identification"

    def __init__(self, parent=0, *args, **kwargs):

        super(LoginWidget, self).__init__(parent=parent, *args, **kwargs)
        self.parent = parent

        self.parentWidget().setWindowTitle(Config.NAME_ORGA + u"    LOGIN")

        self.intro = FormLabel(u"<h3>Vous devez vous identifier pour pouvoir<h3>"
                                  u"<i>utiliser {}.</i>".format(Config.NAME_ORGA))
        self.title = F_PageTitle(u"<ul><h2>{app_org}</h2> \
                                 <b><li>{app_name}</li> </b>\
                                 <ul><li>{org}</li><li><b>Version:\
                                 </b> {version}</li></ul>\
                                 </ul>".format(email=Config.EMAIL_AUT,
                                               app_org=Config.NAME_ORGA,
                                               org=Config.ORG_AUT,
                                               version=Config.APP_VERSION,
                                               app_name=Config.APP_NAME))
        self.title.setStyleSheet(u"background: url({}) \
                                 no-repeat scroll 20px 50px #CCCCCC;\
                                 border-radius: 14px 14px 4px 4px;font: \
                                 13pt 'URW Bookman L';".format(Config.APP_LOGO))

        vbox = QHBoxLayout()
        vbox.addWidget(self.title)

        if len(Owner.all()) < 2:
            self.createNewUserGroupBox()
            vbox.addWidget(self.topLeftGroupBoxBtt)
            self.setLayout(vbox)
        else:
            self.createLoginUserGroupBox()
            vbox.addWidget(self.topLeftGroupBox)
            # set focus to username field
            self.setFocusProxy(self.username_field)
            self.setLayout(vbox)

    def createLoginUserGroupBox(self):
        self.topLeftGroupBox = QGroupBox(self.tr("Identification"))

        # username field
        self.username_field = EnterTabbedLineEdit()
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
        self.topLeftGroupBoxBtt = QGroupBox(self.tr("Nouveau utilisateur"))

        butt = Button_menu(u"Créer un nouvel utilisateur")
        butt.setIcon(QIcon.fromTheme('save', QIcon(u"{}useradd.png".format(Config.img_cmedia))))
        butt.clicked.connect(self.goto_new_user)

        gridbox = QGridLayout()
        gridbox.addWidget(butt, 0, 1, 1, 1)
        gridbox.addWidget(butt, 1, 2, 1, 1)

        self.topLeftGroupBoxBtt.setLayout(gridbox)

    def goto_home(self):
        self.change_main_context(HomeViewWidget)

    def goto_new_user(self):
        from Common.ui.new_user import NewUserViewWidget
        self.parent.open_dialog(NewUserViewWidget, modal=True, go_home=True)

    def ckecklogin(self):
        """ """
        username = unicode(self.username_field.text()).strip()
        password = unicode(self.password_field.text()).strip()
        password = Owner().crypt_password(password)
        # check completeness
        try:
            # owners = Owner.get(islog=True)
            owner = Owner.get(Owner.islog == True)
            owner.islog = False
            owner.save()
        except:
            pass
        if not self.is_complete():
            return

        self.pixmap = QPixmap(u"{}warning.png".format(Config.img_cmedia))
        try:
            owner = Owner.get(username=username, password=password)
            owner.islog = True
        except:
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
        self.goto_home()

    def is_complete(self):
        """ form has been completly filled or not. Sets error messages """

        complete = True

        # reset login error
        self.login_error.clear()

        # username is required
        if not self.username_field.text():
            self.username_error.setText(u"L'identifiant est requis.")
            complete = False
        else:
            self.username_error.clear()

        # password is required
        if not self.password_field.text():
            self.password_error.setText(u"Le mot de passe est requis.")
            complete = False
        else:
            self.password_error.clear()
        return complete

