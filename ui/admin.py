#!/usr/bin/env python
# -*- coding: utf8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu
# maintainer: Fad
from __future__ import (
    unicode_literals, absolute_import, division, print_function)

from PyQt4.QtCore import Qt, SIGNAL
from PyQt4.QtGui import (QVBoxLayout, QFont, QGridLayout, QSplitter,
                         QFrame, QCheckBox, QMessageBox, QTextEdit,
                         QListWidgetItem, QIcon, QPixmap, QLabel, QListWidget)

from Common.ui.user_add_or_edit import NewOrEditUserViewWidget
from Common.ui.common import (FWidget, FLabel, FBoxTitle, Button,
                              LineEdit, Button_save, FormLabel, IntLineEdit)

from configuration import Config
from Common.models import Owner

from Common.models import Organization, SettingsAdmin
from Common.tabpane import tabbox
from Common.ui.util import (formatted_number, raise_error)
from Common.ui.table import FTableWidget

from static import Constants

try:
    unicode
except NameError:
    unicode = str


class AdminViewWidget(FWidget):

    def __init__(self, parent=0, *args, **kwargs):
        super(AdminViewWidget, self).__init__(parent=parent, *args, **kwargs)

        self.parent = parent

        self.parentWidget().setWindowTitle(
            Constants.APP_NAME + u"    ADMINISTRATION")

        editbox = QGridLayout()
        table_config = QVBoxLayout()
        self.table_config = OrganizationTableWidget(parent=self)
        table_config.addLayout(editbox)
        table_config.addWidget(self.table_config)

        self.bttrestor = Button(_(u"Restaurer"))
        self.bttrestor.clicked.connect(self.restorseleted)
        self.bttrestor.setEnabled(False)
        self.bttempty = Button(_(u"Vide"))
        self.bttempty.clicked.connect(self.deletedseleted)
        self.bttempty.setEnabled(False)
        # Grid
        gridbox = QGridLayout()
        # gridbox.addWidget(self.bttrestor, 0 , 1)
        # gridbox.addWidget(self.bttempty, 0 , 2)
        history_table = QVBoxLayout()

        self.history_table = TrashTableWidget(parent=self)
        history_table.addLayout(gridbox)
        history_table.addWidget(self.history_table)

        table_login = QVBoxLayout()
        self.table_login = LoginManageWidget(parent=self)
        table_login.addLayout(gridbox)
        table_login.addWidget(self.table_login)

        tab_widget = tabbox((table_config, _(u"Gestion de l'organisation")),
                            (history_table, _(u"Historique")),
                            (table_login, _(u"Gestion d'Utilisateurs")),
                            )

        vbox = QVBoxLayout()
        vbox.addWidget(tab_widget)
        self.setLayout(vbox)

    def enablebtt(self):
        self.bttrestor.setEnabled(True)
        self.bttempty.setEnabled(True)

    def restorseleted(self):
        for doc in self.history_table.getSelectTableItems():
            doc.isnottrash()
            self.history_table.refresh_()

    def deletedseleted(self):
        reply = QMessageBox.question(self, 'Suppression definitive',
                                     self.tr(
                                         "Voulez vous vraiment le supprimer? "),
                                     QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            for doc in self.history_table.getSelectTableItems():
                doc.remove_doc()
                self.history_table.refresh_()


class TrashTableWidget(FTableWidget):

    def __init__(self, parent, *args, **kwargs):

        FTableWidget.__init__(self, parent=parent, *args, **kwargs)

        self.parent = parent

        self.hheaders = [
            _(u"Selection"), _(u"Date"), _(u"categorie"), _(u"Description")]
        self.stretch_columns = [0]
        self.align_map = {0: 'l'}
        self.ecart = -5
        self.display_vheaders = False
        self.display_fixed = True

        self.refresh_()

    def refresh_(self):
        self._reset()
        self.set_data_for()
        self.refresh()

    def set_data_for(self):
        self.data = []
        # self.data = [("", record.date, record.category, record.description)
        # for record in Records.select().where(Records.trash ==
        # True).order_by(Records.category.asc())]

    def getSelectTableItems(self):
        n = self.rowCount()
        ldata = []
        for i in range(n):
            item = self.cellWidget(i, 0)
            if not item:
                pass
            elif item.checkState() == Qt.Checked:
                ldata.append("ee")
                # ldata.append(Records.filter(description=str(self.item(i, 3).text())).get())
        return ldata

    def _item_for_data(self, row, column, data, context=None):
        if column == 0:
            # create check box as our editor.
            editor = QCheckBox()
            if data == 2:
                editor.setCheckState(2)
            self.connect(
                editor, SIGNAL('stateChanged(int)'), self.parent.enablebtt)
            return editor
        return super(TrashTableWidget, self)._item_for_data(row, column,
                                                            data, context)

    def click_item(self, row, column, *args):
        pass


class OrganizationTableWidget(FWidget):

    def __init__(self, parent, *args, **kwargs):
        super(FWidget, self).__init__(parent=parent, *args, **kwargs)

        self.organisation = Organization.get(id=1)
        self.parent = parent
        vbox = QVBoxLayout()
        # vbox.addWidget(FPageTitle(u"Utilisateur: %s " % self.organisation.name_orga))

        self.checked = QCheckBox("Active")
        if SettingsAdmin.select().where(SettingsAdmin.login == True).count() != 0:
            self.checked.setCheckState(Qt.Checked)
        # self.setCellWidget(nb_rows, 2, checked)
        self.checked.setToolTip(u"""Cocher si vous voulez pour deactive
                                le login continue à utiliser le systeme""")
        self.name_orga = LineEdit(self.organisation.name_orga)
        self.phone = IntLineEdit(str(self.organisation.phone))
        self.bp = LineEdit(self.organisation.bp)
        self.adress_org = QTextEdit(self.organisation.adress_org)
        self.email_org = LineEdit(self.organisation.email_org)

        formbox = QVBoxLayout()
        editbox = QGridLayout()

        editbox.addWidget(FormLabel(u"Non de l'organisation: "), 0, 0)
        editbox.addWidget(self.name_orga, 0, 1)
        editbox.addWidget(FormLabel(u"Activer le login"), 1, 0)
        editbox.addWidget(self.checked, 1, 1)
        editbox.addWidget(FormLabel(u"B.P:"), 2, 0)
        editbox.addWidget(self.bp, 2, 1)
        editbox.addWidget(FormLabel(u"Tel:"), 3, 0)
        editbox.addWidget(self.phone, 3, 1)
        editbox.addWidget(FormLabel(u"E-mail:"), 4, 0)
        editbox.addWidget(self.email_org, 4, 1)
        editbox.addWidget(FormLabel(u"Adresse complete:"), 5, 0)
        editbox.addWidget(self.adress_org, 5, 1)

        butt = Button_save(u"Enregistrer")
        butt.clicked.connect(self.save_edit)
        editbox.addWidget(butt, 8, 1)

        formbox.addLayout(editbox)
        vbox.addLayout(formbox)
        self.setLayout(vbox)

    def save_edit(self):
        ''' add operation '''
        name_orga = unicode(self.name_orga.text())
        bp = unicode(self.bp.text())
        email_org = unicode(self.email_org.text())
        phone = unicode(self.phone.text())
        adress_org = unicode(self.adress_org.toPlainText())

        if self.check_impty:
            login = False
            org = Organization.get(id=self.organisation.id)
            if self.checked.checkState() == Qt.Checked:
                login = True
            org.phone = phone
            org.name_orga = name_orga
            org.email_org = email_org
            org.bp = bp
            org.adress_org = adress_org
            org.save()
            sttg = SettingsAdmin.get(id=1)
            sttg.login = login
            sttg.save()
            self.parent.parent.Notify(u"Le Compte %s a été mise à jour" %
                                      org.name_orga, "success")
        else:
            raise_error(u"Error", u"Mot de passe pas correct")

    def check_impty(self):
        flag = False
        for field in [self.name_orga, self.phone, self.bp, self.email_org]:
            if field.text() == "":
                flag = True
        return flag


class LoginManageWidget(FWidget):

    def __init__(self, parent, *args, **kwargs):
        super(FWidget, self).__init__(parent=parent, *args, **kwargs)
        self.parentWidget().setWindowTitle(Config.NAME_ORGA + u"  Gestion ")
        self.parent = parent

        self.table_owner = OwnerTableWidget(parent=self)
        self.table_info = InfoTableWidget(parent=self)
        self.operation = OperationWidget(parent=self)

        splitter = QSplitter(Qt.Horizontal)
        # splitter.setFrameShape(QFrame.StyledPanel)

        splitter_down = QSplitter(Qt.Vertical)
        splitter_down.addWidget(self.operation)

        splitter_left = QSplitter(Qt.Vertical)
        splitter_left.addWidget(FBoxTitle(u""))
        splitter_left.addWidget(self.table_owner)
        splitter_left.addWidget(splitter_down)

        splitter_rigth = QSplitter(Qt.Vertical)
        splitter_rigth.addWidget(FBoxTitle(u""))
        splitter_rigth.addWidget(self.table_info)
        splitter_rigth.resize(900, 1000)

        splitter.addWidget(splitter_left)
        splitter.addWidget(splitter_rigth)

        gridbox = QGridLayout()
        gridbox.addWidget(splitter, 2, 0, 5, 4)

        vbox = QVBoxLayout(self)
        vbox.addLayout(gridbox)
        self.setLayout(vbox)


class OperationWidget(FWidget):

    """docstring for OperationWidget"""

    def __init__(self, parent, *args, **kwargs):
        super(FWidget, self).__init__(parent=parent, *args, **kwargs)

        vbox = QVBoxLayout(self)
        editbox = QGridLayout()
        self.parent = parent

        self.empty = FLabel(u"")
        editbox.addWidget(self.empty, 1, 0)

        self.add_ow_but = Button(_(u"Nouvel utilisateur"))
        self.add_ow_but.setIcon(QIcon.fromTheme('',
                                                QIcon(u"{}user_add.png".format(Config.img_cmedia))))
        self.add_ow_but.clicked.connect(self.add_owner)

        editbox.addWidget(self.add_ow_but, 2, 0)

        vbox.addLayout(editbox)
        self.setLayout(vbox)

    def add_owner(self):
        self.parent.parent.open_dialog(
            NewOrEditUserViewWidget, modal=True, pp=self.parent.table_owner)


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
        for owner in Owner.select():
            self.addItem(OwnerQListWidgetItem(owner))

    def handleClicked(self):
        owner_item = self.currentItem()
        if isinstance(owner_item, int):
            return
        self.parent.table_info.edit_ow_but.setEnabled(True)
        self.parent.table_info.refresh_(owner_item.owner)


class OwnerQListWidgetItem(QListWidgetItem):

    def __init__(self, owner):
        super(OwnerQListWidgetItem, self).__init__()

        self.owner = owner

        if isinstance(owner, int):
            logo = ""
        else:
            logo = "user_active" if self.owner.isactive else "user_deactive"
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
            self.setTextAlignment(
                Qt.AlignHCenter | Qt.AlignVCenter | Qt.AlignCenter)
            self.setText(u"Utilisateurs")

    @property
    def owner_id(self):
        try:
            return self.owner_id
        except AttributeError:
            return self.owner


class InfoTableWidget(FWidget):

    def __init__(self, parent, *args, **kwargs):
        super(FWidget, self).__init__(parent=parent, *args, **kwargs)

        self.parent = parent

        self.refresh()

        self.username_field = FLabel()
        self.password_field = FLabel()
        self.phone_field = FLabel()
        self.group_field = FLabel()
        self.isactive_field = FLabel()
        self.last_login_field = FLabel()
        self.login_count_field = FLabel()
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
        self.owner = owner

        if isinstance(self.owner, int):
            return

        for i in [self.isactive_field, self.phone_field, self.last_login_field,
                  self.login_count_field]:
            i.setText("")

        self.username_field.setText(
            "<h2>Nom:  {}</h2>".format(self.owner.username))
        self.isactive_field.setText(
            "<b>Active:</b> {}".format(self.owner.isactive))
        self.phone_field.setText(
            u"<b>Numéro tel:</b> {}".format(self.owner.phone))
        self.last_login_field.setText(u"<b>Dernière login:</b> {}".format(
                                      self.owner.last_login.strftime(u"%c")))
        self.login_count_field.setText("<b>Numbre de connexion:</b> {}"
                                       .format(self.owner.login_count))
        self.group_field.setText("<b>Groupe:</b> {}".format(self.owner.group))

    def edit_owner(self):
        self.parent.parent.open_dialog(NewOrEditUserViewWidget, owner=self.owner,
                                       modal=True, pp=self.parent.table_info)
