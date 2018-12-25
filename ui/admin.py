#!/usr/bin/env python
# -*- coding: utf8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu
# maintainer: Fad
from __future__ import (
    unicode_literals, absolute_import, division, print_function)

from PyQt4.QtCore import Qt, SIGNAL
from PyQt4.QtGui import (
    QVBoxLayout, QHBoxLayout, QFont, QGridLayout, QSplitter, QCheckBox,
    QMessageBox, QTextEdit, QFormLayout, QListWidgetItem, QIcon, QPixmap,
    QListWidget, QComboBox)

from Common.ui.user_add_or_edit import NewOrEditUserViewWidget
from Common.ui.common import (FWidget, FLabel, Button,
                              LineEdit, Button_save, FormLabel, IntLineEdit)

from configuration import Config
from Common.models import Owner

from Common.models import Organization
from Common.tabpane import tabbox
from Common.ui.util import check_is_empty
from Common.ui.table import FTableWidget


try:
    unicode
except NameError:
    unicode = str


class AdminViewWidget(FWidget):

    def __init__(self, parent=0, *args, **kwargs):
        super(AdminViewWidget, self).__init__(parent=parent, *args, **kwargs)

        self.parent = parent

        self.parentWidget().setWindowTitle(
            Config.APP_NAME + u"    ADMINISTRATION")

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
        reply = QMessageBox.question(
            self, 'Suppression definitive',
            self.tr("Voulez vous vraiment le supprimer ?"),
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
                # ldata.append(Records.filter(description=str(self.item(i,
                # 3).text())).get())
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

        self.organization = Organization().get(id=1)
        self.parent = parent
        vbox = QVBoxLayout()
        # vbox.addWidget(FPageTitle(u"Utilisateur: %s " %
        # self.organisation.name_orga))

        self.liste_devise = Organization.DEVISE
        # Combobox widget
        self.box_devise = QComboBox()
        for index, value in enumerate(self.liste_devise):
            self.box_devise.addItem(
                "{} {}".format(self.liste_devise[value], value))
            if self.organization.devise == value:
                self.box_devise.setCurrentIndex(index)

        self.checked = QCheckBox("Active")
        if self.organization.is_login:
            self.checked.setCheckState(Qt.Checked)
        self.checked.setToolTip(u"""Cocher si vous voulez pour deactive
                                le login continue à utiliser le systeme""")
        self.name_orga = LineEdit(self.organization.name_orga)
        self.phone = IntLineEdit(str(self.organization.phone))
        self.bp = LineEdit(self.organization.bp)
        self.adress_org = QTextEdit(self.organization.adress_org)
        self.email_org = LineEdit(self.organization.email_org)

        formbox = QFormLayout()
        formbox.addRow(FormLabel(u"Nom de l'organisation:"), self.name_orga)
        formbox.addRow(FormLabel(u"Tel:"), self.phone)
        formbox.addRow(FormLabel(u"Activer le login"), self.checked)
        formbox.addRow(FormLabel(u"Devise :"), self.box_devise)
        formbox.addRow(FormLabel(u"B.P:"), self.bp)
        formbox.addRow(FormLabel(u"E-mail:"), self.email_org)
        formbox.addRow(FormLabel(u"Adresse complete:"), self.adress_org)

        butt = Button_save(u"Enregistrer")
        butt.clicked.connect(self.save_edit)
        formbox.addRow("", butt)

        vbox.addLayout(formbox)
        self.setLayout(vbox)

    def save_edit(self):
        ''' add operation '''
        name_orga = unicode(self.name_orga.text())
        if check_is_empty(self.name_orga):
            return

        if check_is_empty(self.phone):
            return

        orga = Organization().get(id=1)
        orga.name_orga = name_orga
        orga.phone = unicode(self.phone.text())
        orga.is_login = True if self.checked.checkState() == Qt.Checked else False
        orga.devise = str(self.box_devise.currentText().split()[1])
        orga.email_org = unicode(self.email_org.text())
        orga.bp = unicode(self.bp.text())
        orga.adress_org = unicode(self.adress_org.toPlainText())
        orga.save()

        self.parent.parent.Notify(u"Le Compte %s a été mise à jour" %
                                  orga.name_orga, "success")


class LoginManageWidget(FWidget):

    def __init__(self, parent, *args, **kwargs):
        super(FWidget, self).__init__(parent=parent, *args, **kwargs)
        self.parentWidget().setWindowTitle("Utilisateur")
        self.parent = parent

        self.table_owner = OwnerTableWidget(parent=self)
        self.table_info = InfoTableWidget(parent=self)
        # self.operation.

        splitter = QSplitter(Qt.Vertical)
        _splitter = QSplitter(Qt.Horizontal)
        _splitter.addWidget(self.table_owner)
        _splitter.addWidget(self.table_info)
        splitter.addWidget(_splitter)
        vbox = QHBoxLayout(self)
        vbox.addWidget(splitter)
        self.setLayout(vbox)


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

        self.details = FLabel()

        self.add_ow_but = Button(_(u"Nouvel utilisateur"))
        self.add_ow_but.setMaximumWidth(300)
        self.add_ow_but.setMaximumHeight(50)
        self.add_ow_but.setIcon(
            QIcon.fromTheme('', QIcon(u"{}user_add.png".format(Config.img_cmedia))))
        self.add_ow_but.clicked.connect(self.add_owner)
        self.edit_ow_but = Button(u"Mettre à jour")
        self.edit_ow_but.setIcon(QIcon.fromTheme(
            'document-new', QIcon(u"{}edit_user.png".format(Config.img_cmedia))))
        self.edit_ow_but.setEnabled(False)
        self.edit_ow_but.setMaximumWidth(200)
        self.edit_ow_but.setMaximumHeight(50)
        self.edit_ow_but.clicked.connect(self.edit_owner)

        self.formbox = QGridLayout()
        self.formbox.addWidget(self.add_ow_but, 0, 0)
        self.formbox.addWidget(self.details, 1, 0)
        self.formbox.addWidget(self.edit_ow_but, 2, 0)
        # self.formbox.ColumnStretch(4, 2)
        # self.formbox.RowStretch(6, 2)
        vbox = QVBoxLayout()
        vbox.addLayout(self.formbox)
        self.setLayout(vbox)

    def add_owner(self):
        self.parent.parent.open_dialog(
            NewOrEditUserViewWidget, modal=True, pp=self.parent.table_owner)

    def refresh_(self, owner):
        self.refresh()
        self.owner = owner

        if isinstance(self.owner, int):
            return
        self.details.setText(
            """<h2>Nom:  {username}</h2>
                <h4><b>Active:</b> {isactive}</h4>
                <h4><b>Numéro tel:</b> {phone}</h4>
                <h4><b>Dernière login:</b> {last_login}</h4>
                <h4><b>Nombre de connexion:</b> {login_count}</h4>
                <h4><b>Groupe:</b> {group}</h4>
            """.format(group=self.owner.group,
                       login_count=self.owner.login_count,
                       last_login=self.owner.last_login.strftime(u"%c"),
                       phone=self.owner.phone,
                       isactive=self.owner.isactive,
                       username=self.owner.username))

    def edit_owner(self):
        self.parent.parent.open_dialog(
            NewOrEditUserViewWidget, owner=self.owner, modal=True, pp=self.parent.table_info)
