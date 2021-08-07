#!/usr/bin/env python
# -*- coding: utf8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu
# maintainer: Fad
from __future__ import unicode_literals, absolute_import, division, print_function

from PyQt4.QtCore import Qt, SIGNAL
from PyQt4.QtGui import (
    QVBoxLayout,
    QHBoxLayout,
    QFont,
    QGridLayout,
    QSplitter,
    QCheckBox,
    QMessageBox,
    QTextEdit,
    QFormLayout,
    QListWidgetItem,
    QIcon,
    QPixmap,
    QListWidget,
    QComboBox,
    QDoubleSpinBox,
)

from Common.ui.user_add_or_edit import NewOrEditUserViewWidget
from Common.ui.common import (
    FWidget,
    FLabel,
    Button,
    LineEdit,
    ButtonSave,
    FormLabel,
    IntLineEdit,
)

from configuration import Config
from Common.models import Owner, Organization, Settings
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

        self.parentWidget().setWindowTitle(Config.APP_NAME + u"    ADMINISTRATION")

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

        table_settings = QVBoxLayout()
        self.table_settings = SettingsTableWidget(parent=self)
        table_settings.addLayout(editbox)
        table_settings.addWidget(self.table_settings)

        self.history_table = TrashTableWidget(parent=self)
        history_table.addLayout(gridbox)
        history_table.addWidget(self.history_table)

        table_login = QVBoxLayout()
        self.table_login = LoginManageWidget(parent=self)
        table_login.addLayout(gridbox)
        table_login.addWidget(self.table_login)

        tab_widget = tabbox(
            (table_settings, _(u"Paramètre")),
            (table_config, _(u"Gestion de l'organisation")),
            (history_table, _(u"Historique")),
            (table_login, _(u"Gestion d'utilisateurs")),
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
            self,
            'Suppression definitive',
            self.tr("Voulez vous vraiment le supprimer?"),
            QMessageBox.Yes,
            QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            for doc in self.history_table.getSelectTableItems():
                doc.remove_doc()
                self.history_table.refresh_()


class TrashTableWidget(FTableWidget):
    def __init__(self, parent, *args, **kwargs):

        FTableWidget.__init__(self, parent=parent, *args, **kwargs)

        self.parent = parent

        self.hheaders = [
            _(u"Selection"),
            _(u"Date"),
            _(u"categorie"),
            _(u"Description"),
        ]
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
            self.connect(editor, SIGNAL('stateChanged(int)'), self.parent.enablebtt)
            return editor
        return super(TrashTableWidget, self)._item_for_data(row, column, data, context)

    def click_item(self, row, column, *args):
        pass


class OrganizationTableWidget(FWidget):
    def __init__(self, parent, *args, **kwargs):
        super(FWidget, self).__init__(parent=parent, *args, **kwargs)

        self.organization = Organization().get(id=1)
        # print(self.organization)
        self.parent = parent
        vbox = QVBoxLayout()
        # vbox.addWidget(FPageTitle(u"Utilisateur: %s " %
        # self.organisation.name_orga))

        # self.liste_devise = Organization.DEVISE
        # Combobox widget

        # self.checked = QCheckBox("Active")
        # if self.organization.is_login:
        #     self.checked.setCheckState(Qt.Checked)
        # self.checked.setToolTip(
        #     u"""Cocher si vous voulez pour deactive
        #                         le login continue à utiliser le systeme"""
        # )

        self.bn_upload = Button(u"logo de l'organisation")
        self.bn_upload.setIcon(
            QIcon.fromTheme('', QIcon(u"{}db.png".format(Config.img_cmedia)))
        )
        self.bn_upload.clicked.connect(self.upload_logo)

        self.logo_orga = LineEdit(self.organization.logo_orga)
        self.name_orga = LineEdit(self.organization.name_orga)
        self.phone = IntLineEdit(str(self.organization.phone))
        self.phone.setMaximumWidth(250)
        self.bp = LineEdit(self.organization.bp)
        self.bp.setMaximumWidth(250)
        self.adress_org = QTextEdit(self.organization.adress_org)
        self.email_org = LineEdit(self.organization.email_org)
        self.email_org.setMaximumWidth(250)

        formbox = QFormLayout()
        formbox.addRow(self.bn_upload, self.logo_orga)
        formbox.addRow(FormLabel(u"Nom de l'organisation:"), self.name_orga)
        formbox.addRow(FormLabel(u"Tel:"), self.phone)
        formbox.addRow(FormLabel(u"B.P:"), self.bp)
        formbox.addRow(FormLabel(u"E-mail:"), self.email_org)
        formbox.addRow(FormLabel(u"Adresse complete:"), self.adress_org)

        butt = ButtonSave(u"Enregistrer")
        butt.clicked.connect(self.save_edit)
        formbox.addRow("", butt)

        vbox.addLayout(formbox)
        self.setLayout(vbox)

    def upload_logo(self):
        from Common.exports import upload_file

        upload_file(folder='C://', dst_folder=Config.ARMOIRE)
        self.accept()

    def save_edit(self):
        '''add operation'''
        name_orga = unicode(self.name_orga.text())
        if check_is_empty(self.name_orga):
            return

        if check_is_empty(self.phone):
            return

        orga = Organization().get(id=1)
        orga.name_orga = name_orga
        orga.phone = unicode(self.phone.text())
        orga.email_org = unicode(self.email_org.text())
        orga.bp = unicode(self.bp.text())
        orga.adress_org = unicode(self.adress_org.toPlainText())
        orga.save()
        self.parent.parent.Notify(
            u"Le Compte %s a été mise à jour" % orga.name_orga, "success"
        )


class LoginManageWidget(FWidget):
    def __init__(self, parent, *args, **kwargs):
        super(FWidget, self).__init__(parent=parent, *args, **kwargs)
        self.parentWidget().setWindowTitle("Utilisateur")
        self.parent = parent

        self.table_owner = OwnerTableWidget(parent=self)
        self.table_owner.setFixedWidth(300)
        self.table_info = InfoTableWidget(parent=self)
        self.operation = OperationWidget(parent=self)
        self.operation.setFixedHeight(100)

        splitterH = QSplitter(Qt.Horizontal)
        splitterH.addWidget(self.table_owner)

        splitterV = QSplitter(Qt.Vertical)
        splitterV.addWidget(self.operation)
        splitterV.addWidget(self.table_info)
        splitterH.addWidget(splitterV)
        vbox = QHBoxLayout(self)
        vbox.addWidget(splitterH)
        self.setLayout(vbox)


class OperationWidget(FWidget):

    """docstring for OperationWidget"""

    def __init__(self, parent, *args, **kwargs):
        super(FWidget, self).__init__(parent=parent, *args, **kwargs)

        vbox = QVBoxLayout(self)
        gridbox = QGridLayout()
        self.parent = parent

        self.add_ow_but = Button(_(u"+ Utilisateur"))
        self.add_ow_but.setMaximumWidth(250)
        # self.add_ow_but.setMaximumHeight(90)
        self.add_ow_but.setIcon(
            QIcon.fromTheme('', QIcon(u"{}user_add.png".format(Config.img_cmedia)))
        )
        self.add_ow_but.clicked.connect(self.add_owner)
        vbox.addWidget(self.add_ow_but)
        self.setLayout(vbox)

    def add_owner(self):
        self.parent.parent.open_dialog(
            NewOrEditUserViewWidget, modal=True, pp=self.parent.table_owner
        )


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
        """Rafraichir la liste des groupes"""
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
        icon.addPixmap(
            QPixmap(u"{}{}.png".format(Config.img_cmedia, logo)),
            QIcon.Normal,
            QIcon.Off,
        )
        self.setIcon(icon)
        self.init_text()

    def init_text(self):
        try:
            self.setText(self.owner.username)
        except AttributeError:
            font = QFont()
            font.setBold(True)
            self.setFont(font)
            self.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter | Qt.AlignCenter)
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
        self.edit_ow_but = Button(u"Mettre à jour")
        self.edit_ow_but.setIcon(
            QIcon.fromTheme(
                'document-new', QIcon(u"{}edit_user.png".format(Config.img_cmedia))
            )
        )
        self.edit_ow_but.setEnabled(False)
        self.edit_ow_but.setMaximumHeight(90)
        self.edit_ow_but.clicked.connect(self.edit_owner)

        self.formbox = QGridLayout()
        self.formbox.addWidget(self.edit_ow_but, 0, 0)
        self.formbox.addWidget(self.details, 1, 0)
        # self.formbox.ColumnStretch(4, 2)
        # self.formbox.RowStretch(6, 2)
        vbox = QVBoxLayout()
        vbox.addLayout(self.formbox)
        self.setLayout(vbox)

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
            """.format(
                group=self.owner.group,
                login_count=self.owner.login_count,
                last_login=self.owner.last_login.strftime(u"%c"),
                phone=self.owner.phone,
                isactive=self.owner.isactive,
                username=self.owner.username,
            )
        )

    def edit_owner(self):
        self.parent.parent.open_dialog(
            NewOrEditUserViewWidget,
            owner=self.owner,
            modal=True,
            pp=self.parent.table_info,
        )


class SettingsTableWidget(FWidget):
    def __init__(self, parent, *args, **kwargs):
        super(FWidget, self).__init__(parent=parent, *args, **kwargs)

        self.settings = Settings().get(id=1)
        self.parent = parent
        vbox = QVBoxLayout()
        # self.slug_field =
        self.url_field = LineEdit(self.settings.url)
        self.list_theme = Settings.THEME
        # Combobox widget
        self.box_theme = QComboBox()
        for index, value in enumerate(self.list_theme):
            self.box_theme.addItem("{}".format(self.list_theme[value]), value)
            if self.settings.theme == value:
                self.box_theme.setCurrentIndex(index)

        self.box_vilgule = QDoubleSpinBox()

        self.box_vilgule.setMaximum(4)
        self.after_cam = self.box_vilgule.setValue(float(self.settings.after_cam))

        self.liste_devise = Settings.DEVISE
        # Combobox widget
        self.box_devise = QComboBox()
        for index, value in enumerate(self.liste_devise):
            self.box_devise.addItem("{}".format(self.liste_devise[value]), value)
            if self.settings.devise == value:
                self.box_devise.setCurrentIndex(index)

        self.liste_position = Settings.POSITION
        # Combobox widget
        self.box_position = QComboBox()
        for index, value in enumerate(self.liste_position):
            self.box_position.addItem("{}".format(self.liste_position[value]), value)
            if self.settings.toolbar_position == value:
                self.box_position.setCurrentIndex(index)

        self.checked = QCheckBox("Active")
        if self.settings.is_login:
            self.checked.setCheckState(Qt.Checked)
        self.checked.setToolTip(
            u"""Cocher si vous voulez pour deactive
                                le login continue à utiliser le systeme"""
        )
        self.toolbar_checked = QCheckBox("Active")
        print("toolbar ", self.settings.toolbar)
        if self.settings.toolbar:
            self.toolbar_checked.setCheckState(Qt.Checked)
        self.toolbar_checked.setToolTip(
            u"""Cocher si vous voulez pour deactive
                                le menu toolbar"""
        )

        formbox = QFormLayout()
        formbox.addRow(FormLabel(u"URL :*"), self.url_field)
        formbox.addRow(FormLabel(u"Theme :"), self.box_theme)
        formbox.addRow(FormLabel(u"Identification"), self.checked)
        formbox.addRow(FormLabel(u"Menu vertical"), self.toolbar_checked)
        formbox.addRow(
            FormLabel(u"Nombre de chiffre après la vilgule :"), self.box_vilgule
        )
        formbox.addRow(FormLabel(u"Devise :"), self.box_devise)
        formbox.addRow(FormLabel(u"Position du menu :"), self.box_position)

        butt = ButtonSave(u"Enregistrer")
        butt.clicked.connect(self.save_edit)
        formbox.addRow("", butt)

        vbox.addLayout(formbox)
        self.setLayout(vbox)

    def save_edit(self):
        '''add operation'''
        if check_is_empty(self.url_field):
            return

        self.settings.url = str(self.url_field.text())
        self.settings.is_login = (
            True if self.checked.checkState() == Qt.Checked else False
        )
        self.settings.toolbar = (
            True if self.toolbar_checked.checkState() == Qt.Checked else False
        )
        print("self.settings.toolbar", self.settings.toolbar)
        self.settings.after_cam = int(self.box_vilgule.value())
        self.settings.theme = self.box_theme.itemData(self.box_theme.currentIndex())
        self.settings.devise = self.box_devise.itemData(self.box_devise.currentIndex())
        self.settings.toolbar_position = self.box_position.itemData(
            self.box_position.currentIndex()
        )
        self.settings.save()

        self.parent.parent.Notify(u"Paramètre mise à jour avec success", "success")
