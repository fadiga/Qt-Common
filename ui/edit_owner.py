#!/usr/bin/env python
# encoding=utf-8
# maintainer: Fad
from __future__ import (unicode_literals, absolute_import, division, print_function)

from PyQt4.QtCore import Qt
from PyQt4.QtGui import (QVBoxLayout, QLabel, QCheckBox, QGridLayout,
                         QDialog, QComboBox, QPixmap)

from model import Owner

from common.cstatic import CConstants
from common.ui.util import raise_success, raise_error
from common.ui.common import (F_Widget, Button_save, Button, IntLineEdit,
                              F_PageTitle, LineEdit)


class EditOwnerViewWidget(QDialog, F_Widget):
    def __init__(self, owner, parent, *args, **kwargs):
        QDialog.__init__(self, parent, *args, **kwargs)

        self.owner = owner
        self.parent = parent
        vbox = QVBoxLayout()
        vbox.addWidget(F_PageTitle(u"Utilisateur: %s " % self.owner.username))

        self.checked = QCheckBox("Active")
        if self.owner.isactive:
            self.checked.setCheckState(Qt.Checked)
        # self.setCellWidget(nb_rows, 2, checked)
        self.checked.setToolTip(u"Cocher si vous voulez que l'utilisateur %s"
                                u"continue à utiliser le systeme" %
                                self.owner.username)
        self.password = LineEdit(self.owner.password)
        self.password.setEchoMode(LineEdit.PasswordEchoOnEdit)
        self.password_v = LineEdit(self.owner.password)
        self.password_v.setEchoMode(LineEdit.PasswordEchoOnEdit)
        self.password_v.textChanged.connect(self.check_password)
        self.phone = IntLineEdit(self.owner.phone)
        self.pixmap = QPixmap("")
        self.image = QLabel(self)
        self.image.setPixmap(self.pixmap)

        self.liste_group = [u"user", u"admin"]
        #Combobox widget
        self.box_group = QComboBox()
        for index in self.liste_group:
            self.box_group.addItem(u'%(group)s' % {'group': index})
        if self.owner.group == "admin":
            self.box_group.setCurrentIndex(1)

        formbox = QVBoxLayout()
        editbox = QGridLayout()

        editbox.addWidget(QLabel(u"Status"), 0, 0)
        editbox.addWidget(self.checked, 1, 0)
        editbox.addWidget(QLabel(u"password"), 0, 1)
        editbox.addWidget(self.password, 1, 1)
        editbox.addWidget(QLabel(u"password"), 0, 2)
        editbox.addWidget(self.password_v, 1, 2)
        editbox.addWidget(self.image, 1, 3)
        editbox.addWidget(QLabel(u"Tel:"), 0, 4)
        editbox.addWidget(self.phone, 1, 4)
        editbox.addWidget(QLabel(u"Group:"), 0, 5)
        editbox.addWidget(self.box_group, 1, 5)

        butt = Button_save(u"Enregistrer")
        butt.clicked.connect(self.save_edit)
        cancel_but = Button(u"Annuler")
        cancel_but.clicked.connect(self.cancel)
        editbox.addWidget(butt, 3, 0)
        editbox.addWidget(cancel_but, 3, 1)

        formbox.addLayout(editbox)
        vbox.addLayout(formbox)
        self.setLayout(vbox)

    def check_password(self):

        self.flog = False

        if (unicode(self.password.text()) == unicode(self.password_v.text())
                                                     and self.password != ""):
            self.pixmap =  QPixmap(u"{}accept.png".format(CConstants.img_cmedia))
            self.image.setToolTip("Mot de passe correct")
            self.flog = True
        else:
            self.pixmap =  QPixmap(u"{}decline.png".format(CConstants.img_cmedia))
            self.image.setToolTip("Mot de passe sont incorrect")
        self.image.setPixmap(self.pixmap)

    def cancel(self):
        self.close()

    def save_edit(self):
        ''' add operation '''
        password = unicode(self.password.text())
        phone = unicode(self.phone.text())
        group = self.liste_group[self.box_group.currentIndex()]
        self.check_password()
        if self.flog:
            status = False
            ow = Owner.get(id=self.owner.id)
            pass_isdiff = unicode(self.password.text()) != ow.password
            if self.checked.checkState() == Qt.Checked:
                status = True
            ow.password = Owner().crypt_password(password) if pass_isdiff else ow.password
            ow.phone = phone
            ow.group = group
            ow.isactive = status
            ow.save()
            self.cancel()
            raise_success(u"Confirmation", u"Le Compte %s "
                          u"a été mise à jour" % ow.username)
            from ui.admin import AdminViewWidget
            self.change_main_context(AdminViewWidget)
        else:
            raise_error(u"Error", u"Mot de passe pas correct")
