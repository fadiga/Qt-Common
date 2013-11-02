#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: Fadiga

import hashlib

from PyQt4.QtGui import (QHBoxLayout, QGridLayout, QGroupBox, QIcon,
                         QLineEdit, QPixmap, QPushButton)

from common import (F_Widget, F_PageTitle, FormLabel, PyTextViewer,
                    EnterTabbedLineEdit, ErrorLabel, Button_menu, Button_rond)
from util import raise_error
from model import Owner
from configuration import Config
# from check_mac import get_mac, is_valide_mac
from ui.home import HomeViewWidget
from ui.dashboard import DashbordViewWidget


class LoginWidget(F_Widget):

    title = u"Identification"

    def __init__(self, parent=0, *args, **kwargs):

        super(LoginWidget, self).__init__(parent=parent, *args, **kwargs)

        self.parent = parent
        self.parentWidget().setWindowTitle(Config.NAME_ORGA + u"    LOGIN")

        self.intro = PyTextViewer(u"<h3>Vous devez vous identifier pour pouvoir<h3>"
                                  u"<i>utiliser %s.</i>" % Config.NAME_ORGA)
        self.title = F_PageTitle(u"<ul><h2>{app_name}</h2> \
                                 <b><li>Logiciel de suivi de stock</li> </b>\
                                 <ul><li>{org}</li><li><b>Version:\
                                 </b> {version}</li></ul>\
                                 </ul>".format(email=Config.EMAIL_AUT,
                                                 app_name=Config.NAME_ORGA,
                                                 org=Config.ORG_AUT,
                                                 version=Config.APP_VERSION))

        self.title.setStyleSheet(u"background: url(%s)"
                                 u" no-repeat scroll 20px 50px #CCCCCC;"
                                 u"border-radius: 14px 14px 4px 4px;font:"
                                 u" 13pt 'URW Bookman L';" % Config.APP_LOGO)

        vbox = QHBoxLayout()
        vbox.addWidget(self.title)
        if Config.debug:
            self.createDebugBtt()
            vbox.addWidget(self.DebugBtt)
        # elif len(Orders.all()) > Config.tolerance:
        #     if not is_valide_mac():
        #         self.create_chow_ms_err()
        #         vbox.addWidget(self.chow_ms_err)

        elif len(Owner.all()) < 2:
            self.createTopRightGroupBoxBtt()
            vbox.addWidget(self.topLeftGroupBoxBtt)
        else:
            self.createTopRightGroupBox()
            vbox.addWidget(self.topLeftGroupBox)
            # set focus to username field
            self.setFocusProxy(self.username_field)
        self.setLayout(vbox)

    def create_chow_ms_err(self):
        self.chow_ms_err = QGroupBox()

        ms_err = PyTextViewer(u"<h3>Vous n'avez pas le droit d'utiliser ce \
                              logiciel sur cette machine, veuillez me contacté \
                              </h3> <ul><li><b>Tel:</b> {phone}</li>\
                              <li><b>{adress}</b></li><li><b>E-mail:</b> \
                              {email}</li></ul>".format(email=Config.EMAIL_AUT,
                                                        adress=Config.ADRESS_AUT,
                                                        phone=Config.TEL_AUT})

        gridbox = QGridLayout()
        gridbox.addWidget(F_PageTitle("Erreur de permission"), 0, 1)
        gridbox.addWidget(ms_err, 0, 0)
        gridbox.addWidget(F_PageTitle("Erreur de permission"), 1, 0)
        gridbox.addWidget(PyTextViewer(get_mac().replace(":", "-")), 1, 1)

        self.chow_ms_err.setLayout(gridbox)

    def createDebugBtt(self):
        self.DebugBtt = QGroupBox(self.tr("Mode debug"))
        butt = Button_rond(u"Home")
        butt.setIcon(QIcon.fromTheme('save', QIcon(u"{img_media}{img}".format(img_media=Config.img_media,
                                                      img='dashboard.png'))))
        butt.clicked.connect(self.goto_home)

        gridbox = QGridLayout()
        gridbox.addWidget(butt, 0, 1, 1, 1)
        gridbox.addWidget(butt, 1, 2, 1, 1)

        self.DebugBtt.setLayout(gridbox)

    def createTopRightGroupBox(self):
        self.topLeftGroupBox = QGroupBox(self.tr("Identification"))

        # username field
        self.username_field = EnterTabbedLineEdit()
        self.username_label = FormLabel(u"&Identifiant")
        self.username_label.setBuddy(self.username_field)
        self.username_error = ErrorLabel(u"")

        # password field
        self.password_field = EnterTabbedLineEdit()
        self.password_field.setEchoMode(QLineEdit.Password)
        # self.password_field.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        self.password_label = FormLabel(u"&Mot de &passe")
        self.password_label.setBuddy(self.password_field)
        self.password_error = ErrorLabel(u"")

        # login button
        self.login_button = QPushButton(u"&S'identifier")
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

    def createTopRightGroupBoxBtt(self):
        self.topLeftGroupBoxBtt = QGroupBox(self.tr("Nouveau utilisateur"))

        butt = Button_menu(u"Créer un nouvel utilisateur")
        butt.setIcon(QIcon.fromTheme('save', QIcon(u"{img_media}{img}".format(img_media=Config.img_media,
                                                      img='useradd.png'))))
        butt.clicked.connect(self.goto_new_user)

        gridbox = QGridLayout()
        gridbox.addWidget(butt, 0, 1, 1, 1)
        gridbox.addWidget(butt, 1, 2, 1, 1)

        self.topLeftGroupBoxBtt.setLayout(gridbox)

    def goto_home(self):
        self.change_main_context(HomeViewWidget)

    def goto_dasboard(self):
        self.change_main_context(DashbordViewWidget)

    def goto_xx(self):
        from ui.order import OrderViewWidget
        self.parent.change_context(OrderViewWidget)

    def goto_new_user(self):
        from new_user import NewUserViewWidget
        self.parent.open_dialog(NewUserViewWidget, modal=True, go_home=True)

    def ckecklogin(self):
        """ """
        username = unicode(self.username_field.text()).strip()
        password = unicode(self.password_field.text()).strip()
        password = hashlib.sha224(password).hexdigest()
        # check completeness
        try:
            # owners = Owner.filter(islog=True)
            owners = Owner.select().where(Owner.islog == True).get()
            for ur in owners:
                ur.islog = False
                ur.save()
        except:
            pass
        if not self.is_complete():
            return

        self.pixmap = QPixmap(u"{img_media}{img}".format(img_media=Config.img_media,
                                                      img="warning.png"))
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

        if owner.group in ["superuser", "admin"]:
            # Le droit de reset des mots de passes
            # Une page special
            self.goto_home()
        else:
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
