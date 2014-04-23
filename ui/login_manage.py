#!/usr/bin/env python
# -*- coding: utf8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu
# maintainer: Fad
from __future__ import (unicode_literals, absolute_import, division, print_function)

from PyQt4.QtGui import (QVBoxLayout, QFont, QGridLayout, QSplitter, QFrame,
                         QListWidgetItem, QIcon, QPixmap, QLabel, QListWidget)
from PyQt4.QtCore import Qt

from Common.ui.edit_owner import EditOwnerViewWidget
from Common.ui.common import (F_Widget, F_Label, F_BoxTitle, Button)

from configuration import Config
from Common.models import Owner


class LoginManageWidget(F_Widget):

    def __init__(self, owner="", parent=0, *args, **kwargs):
        super(LoginManageWidget, self).__init__(parent=parent,
                                                           *args, **kwargs)
        self.parentWidget().setWindowTitle(Config.NAME_ORGA + u"  Gestion ")
        self.parent = parent

        self.table_owner = OwnerTableWidget(parent=self)
        self.table_info = InfoTableWidget(parent=self)
        self.operation = OperationWidget(parent=self)

        splitter = QSplitter(Qt.Horizontal)
        splitter.setFrameShape(QFrame.StyledPanel)

        splitter_down = QSplitter(Qt.Vertical)
        splitter_down.addWidget(self.operation)

        splitter_left = QSplitter(Qt.Vertical)
        splitter_left.addWidget(F_BoxTitle(u""))
        splitter_left.addWidget(self.table_owner)
        splitter_left.addWidget(splitter_down)

        splitter_rigth = QSplitter(Qt.Vertical)
        splitter_rigth.addWidget(F_BoxTitle(u""))
        splitter_rigth.addWidget(self.table_info)
        splitter_rigth.resize(900, 1000)

        splitter.addWidget(splitter_left)
        splitter.addWidget(splitter_rigth)

        gridbox = QGridLayout()
        gridbox.addWidget(splitter, 2, 0, 5, 4)

        vbox = QVBoxLayout(self)
        vbox.addLayout(gridbox)
        self.setLayout(vbox)


class OperationWidget(F_Widget):
    """docstring for OperationWidget"""

    def __init__(self, parent, *args, **kwargs):
        super(F_Widget, self).__init__(parent=parent, *args, **kwargs)

        vbox = QVBoxLayout(self)
        editbox = QGridLayout()
        self.parent = parent

        self.empty = F_Label(u"")
        editbox.addWidget(self.empty, 1, 0)

        self.add_ow_but = Button(_(u"Nouvel utilisateur"))
        self.add_ow_but.setIcon(QIcon.fromTheme('',
                                     QIcon(u"{}user_add.png".format(Config.img_cmedia))))
        self.add_ow_but.clicked.connect(self.add_owner)

        # self.edit_ow_but = Button(u"Mettre à jour")
        # self.edit_ow_but.setIcon(QIcon.fromTheme('document-new',
        #                              QIcon(u"{}edit_user.png".format(Config.img_cmedia))))
        # self.edit_ow_but.setEnabled(False)
        # self.edit_ow_but.clicked.connect(self.edit_owner)
        editbox.addWidget(self.add_ow_but, 2, 0)
        # editbox.addWidget(self.edit_ow_but, 3, 0)

        vbox.addLayout(editbox)
        self.setLayout(vbox)

    def add_owner(self):
        from Common.ui.new_user import NewUserViewWidget
        self.parent.open_dialog(NewUserViewWidget, modal=True, pp=self.parent.table_owner)


    # def edit_owner(self):
    #     self.parent.open_dialog(EditOwnerViewWidget,
    #                             modal=True, pp=self.parent.table_info)

class OwnerTableWidget(QListWidget):
    """docstring for OwnerTableWidget"""
    def __init__(self, parent, *args, **kwargs):
        super(OwnerTableWidget, self).__init__(parent)
        self.parent = parent
        self.setAutoScroll(True)
        self.setAutoFillBackground(True)
        self.itemSelectionChanged.connect(self.handleClicked)
        self.refresh_()

    def refresh_(self):
        """ Rafraichir la liste des groupes"""
        self.clear()
        self.addItem(OwnerQListWidgetItem(-1))
        for owner in Owner.select().where((Owner.isvisible==True)):
            self.addItem(OwnerQListWidgetItem(owner))

    def handleClicked(self):
        owner = self.currentItem()
        if isinstance(owner, int):
            return
        self.parent.table_info.edit_ow_but.setEnabled(True)
        self.parent.table_info.refresh_(owner)


class OwnerQListWidgetItem(QListWidgetItem):

    def __init__(self, owner):
        super(OwnerQListWidgetItem, self).__init__()

        self.owner = owner

        if isinstance(owner, int):
            logo = ""
        else:
            logo = "user_active" if self.owner.isactive else "user-offline"
        icon = QIcon()
        icon.addPixmap(QPixmap(u"{}{}.png".format(Config.img_cmedia, logo)),
                       QIcon.Normal, QIcon.Off)
        self.setIcon(icon)
        self.init_text()

    def init_text(self):
        try:
            self.setText(self.owner.username)
        except AttributeError:
            font = QFont()
            font.setBold(True)
            self.setFont(font)
            self.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter|Qt.AlignCenter)
            self.setText(u"Utilisateurs")

    @property
    def owner_id(self):
        try:
            return self.owner_id
        except AttributeError:
            return self.owner


class InfoTableWidget(F_Widget):

    def __init__(self, parent, *args, **kwargs):
        super(F_Widget, self).__init__(parent=parent, *args, **kwargs)

        self.parent = parent

        self.refresh()

        self.username_field = F_Label()
        self.password_field = F_Label()
        self.phone_field = F_Label()
        self.group_field = F_Label()
        self.isactive_field = F_Label()
        self.last_login_field = F_Label()
        self.login_count_field = F_Label()
        self.pixmap = QPixmap("")
        self.image = QLabel(self)
        self.image.setPixmap(self.pixmap)
        self.edit_ow_but = Button(u"Mettre à jour")
        self.edit_ow_but.setIcon(QIcon.fromTheme('document-new',
                                     QIcon(u"{}edit_user.png".format(Config.img_cmedia))))
        self.edit_ow_but.setEnabled(False)
        self.edit_ow_but.clicked.connect(self.edit_owner)

        self.editbox = QGridLayout()
        self.editbox.addWidget(self.edit_ow_but, 0, 3)
        self.editbox.addWidget(self.username_field, 0, 0)
        self.editbox.addWidget(self.group_field, 1, 0)
        self.editbox.addWidget(self.login_count_field, 2, 0)
        self.editbox.addWidget(self.isactive_field, 3, 0)
        self.editbox.addWidget(self.last_login_field, 4, 0)
        self.editbox.addWidget(self.phone_field, 5, 0)
        self.editbox.setColumnStretch(4, 2)
        self.editbox.setRowStretch(6, 2)
        vbox = QVBoxLayout()
        vbox.addLayout(self.editbox)
        self.setLayout(vbox)

    def refresh_(self, owner):
        self.refresh()
        self.owner = owner.owner

        if isinstance(self.owner, int):
            return

        for i in [self.isactive_field, self.phone_field, self.last_login_field,
                  self.login_count_field]:
            i.setText("")

        self.username_field.setText("<h2>Nom:  {}</h2>".format(self.owner.username))
        self.isactive_field.setText("<b>Active:</b> {}".format(self.owner.isactive))
        self.phone_field.setText(u"<b>Numéro tel:</b> {}".format(self.owner.phone))
        self.last_login_field.setText(u"<b>Dernière login:</b> {}".format(
                                     self.owner.last_login
                                         .strftime(u"%A le %d %b %Y a %Hh:%Mmn")))
        self.login_count_field.setText("<b>Numbre de connexion:</b> {}"
                                      .format(self.owner.login_count))
        self.group_field.setText("<b>Groupe:</b> {}".format(self.owner.group))

    def edit_owner(self):
        self.parent.open_dialog(EditOwnerViewWidget,
                                modal=True, pp=self.parent.table_info)