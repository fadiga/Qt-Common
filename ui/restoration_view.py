#!usr/bin/env python
# -*- coding: utf8 -*-
# maintainer: Fad
from __future__ import unicode_literals, absolute_import, division, print_function

from PyQt4.QtCore import Qt
from PyQt4.QtGui import (
    QVBoxLayout,
    QGridLayout,
    QGroupBox,
    QDialog,
    QTextEdit,
    QFormLayout,
    QIcon,
)
from PyQt4.QtGui import QComboBox, QVBoxLayout, QCheckBox, QFormLayout, QDialog
from peewee import IntegrityError
from Common.ui.util import check_is_empty, field_error, is_valide_codition_field
from Common.models import Owner

from Common.exports import import_backup
from Common.ui.common import (
    FWidget,
    LineEdit,
    Button,
    FLabel,
    FormLabel,
    EnterTabbedLineEdit,
)

from configuration import Config

try:
    unicode
except:
    unicode = str


class RestorationViewWidget(QDialog, FWidget):
    def __init__(self, pp=None, owner=None, parent=None, *args, **kwargs):
        QDialog.__init__(self, parent, *args, **kwargs)

        self.setWindowTitle(u"Restoration de Données")
        vbox = QVBoxLayout()
        # self.online_resto_box()
        self.label = FLabel()
        self.label.setStyleSheet(
            "background: url('{}center.png') no-repeat scroll 0 0;"
            "height: 50px;width:50px; margin: 0; padding: 0;".format(Config.img_media)
        )

        # ==== Box of restor online ====
        self.onlineRestorBoxBtt = QGroupBox(self.tr("Restoration de données en line"))
        self.bn_resto_onligne = Button(u"Connexion")
        self.bn_resto_onligne.setIcon(
            QIcon.fromTheme('', QIcon(u"{}cloud.png".format(Config.img_cmedia)))
        )
        self.bn_resto_onligne.clicked.connect(self.resto_onligne)

        self.bn_resto_l = Button(u"Import de sauvegarde locale")
        self.bn_resto_l.setIcon(
            QIcon.fromTheme('', QIcon(u"{}db.png".format(Config.img_cmedia)))
        )
        self.bn_resto_l.clicked.connect(self.resto_local_db)

        self.bn_ignore = Button(u"Première installation")
        self.bn_ignore.setIcon(
            QIcon.fromTheme('', QIcon(u"{}go-next.png".format(Config.img_cmedia)))
        )
        self.bn_ignore.clicked.connect(self.ignore_resto)

        self.mail_field = LineEdit()
        self.password_field = EnterTabbedLineEdit()
        self.password_field.setEchoMode(LineEdit.Password)
        self.password_field.setFocus()

        formbox = QFormLayout()

        # formbox.addRow(FormLabel("<i>les données sauvegardé en ligne</i>"))
        formbox.addRow(FormLabel("E-mail"), self.mail_field)
        formbox.addRow(FormLabel("Mot de passe"), self.password_field)
        formbox.addRow(FormLabel(""), self.bn_resto_onligne)
        self.onlineRestorBoxBtt.setLayout(formbox)
        vbox.addWidget(self.onlineRestorBoxBtt)

        # ==== Box of restor online ====
        self.onLocaleRestorBoxBtt = QGroupBox(
            self.tr("Restoration de données en locale.")
        )

        l_formbox = QFormLayout()
        # l_formbox.addRow(FormLabel("<i>Une copie de la base de données exportée.</i>"))
        l_formbox.addRow(FormLabel(""), self.bn_resto_l)
        self.onLocaleRestorBoxBtt.setLayout(l_formbox)
        vbox.addWidget(self.onLocaleRestorBoxBtt)

        i_formbox = QFormLayout()
        i_formbox.addRow(FLabel("<h2></h2>"), self.bn_ignore)
        vbox.addLayout(i_formbox)
        self.setLayout(vbox)

    def resto_onligne(self):
        # self.open_dialog()
        self.vbox.removeWidget(self.topLeftGroupBoxBtt)
        # return

    def ignore_resto(self):
        print("ignore_resto")
        self.accept()

    def resto_local_db(self):
        import_backup(folder='C://', dst_folder=Config.ARMOIRE)
        self.accept()
