#!usr/bin/env python
# -*- coding: utf-8 -*-
#maintainer: Fad

import hashlib
from sqlite3 import IntegrityError

from PyQt4.QtGui import (QComboBox, QLabel, QVBoxLayout,
                         QGridLayout, QPixmap, QDialog)

from configuration import Config

from model import Owner
from common import (F_Widget, IntLineEdit, Button_save, LineEdit, Button)
from util import raise_success, raise_error
from login import LoginWidget


class NewUserViewWidget(QDialog, F_Widget):
    def __init__(self, go_home, parent=0, *args, **kwargs):
        QDialog.__init__(self, parent, *args, **kwargs)

        self.setWindowTitle(u"Nouvel utilisateur")
        self.parent = parent
        self.go_home = go_home
        self.parentWidget().setWindowTitle(Config.NAME_ORGA + u"    ADMINISTRATION")

        self.username = LineEdit()
        self.password = LineEdit()
        self.password.setEchoMode(LineEdit.PasswordEchoOnEdit)
        self.password_v = LineEdit()
        self.password_v.setEchoMode(LineEdit.PasswordEchoOnEdit)
        self.password_v.textChanged.connect(self.check_password)
        self.phone = IntLineEdit()
        self.pixmap = QPixmap("")
        self.image = QLabel(self)
        self.image.setPixmap(self.pixmap)

        self.liste_group = [u"user", u"admin"]
        #Combobox widget
        self.box_group = QComboBox()
        for index in self.liste_group:
            self.box_group.addItem(u'%(group)s' % {'group': index})

        butt = Button_save(u"Enregistrer")
        butt.clicked.connect(self.add_operation)
        cancel_but = Button(u"Annuler")
        cancel_but.clicked.connect(self.cancel)

        editbox = QGridLayout()
        editbox.addWidget(QLabel(u"Non d'utilisateur"), 0, 0)
        editbox.addWidget(self.username, 0, 1)
        editbox.addWidget(QLabel(u"Mot de passe"), 1, 0)
        editbox.addWidget(self.password, 1, 1)
        editbox.addWidget(QLabel(u"Verification du Mot de passe"), 2, 0)
        editbox.addWidget(self.password_v, 2, 1)
        editbox.addWidget(self.image, 2, 2)
        editbox.addWidget(QLabel(u"Numero de Téléphone"), 4, 0)
        editbox.addWidget(self.phone, 4, 1)
        editbox.addWidget(QLabel(u"Groupe"), 5, 0)
        editbox.addWidget(self.box_group, 5, 1)
        editbox.addWidget(butt, 6, 1)
        editbox.addWidget(cancel_but, 6, 0)

        formbox = QVBoxLayout()
        formbox.addLayout(editbox)
        vbox = QVBoxLayout()
        vbox.addLayout(formbox)
        self.setLayout(vbox)

    def cancel(self):
        self.close()

    def check_password(self):

        self.flog = False

        if (unicode(self.password.text()) == unicode(self.password_v.text())):
            self.pixmap = QPixmap(u"{img_media}{img}".format(img_media=Config.img_media,
                                                      img="accept.png"))
            self.image.setToolTip("Mot de passe correct")
            self.flog = True
        else:
            self.pixmap = QPixmap(u"{img_media}{img}".format(img_media=Config.img_media,
                                                      img="decline.png"))
            self.image.setToolTip("Mot de passe sont incorrect")
        self.image.setPixmap(self.pixmap)

    def add_operation(self):
        ''' add operation '''
        username = unicode(self.username.text())
        password = unicode(self.password.text())
        phone = unicode(self.phone.text())
        group = self.liste_group[self.box_group.currentIndex()]

        if (username != "" and password != "" and phone != ""):
            if self.flog:
                ow = Owner()
                ow.username = username
                ow.password = hashlib.sha224(password).hexdigest()
                ow.phone = phone
                ow.group = group
                try:
                    ow.save()
                    if self.go_home:
                        self.goto_home()
                        self.parent.logout()
                    # else:
                    #     self.parent.table_owner.refresh_()
                    self.close()
                    raise_success(u"Confirmation", u"L'utilisateurs %s "
                                  u"a été enregistré" % ow.username)
                except IntegrityError:
                    raise_error(u"Erreur", u"L'utilisateurs %s "
                                u"existe déjà dans la base de donnée" % ow.username)
        else:
            raise_error(u"Erreur", u"Tout les champs sont obligatoire")

    def goto_home(self):
        self.change_main_context(LoginWidget)
