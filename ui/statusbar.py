#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: fadiga

from PyQt4.QtGui import QStatusBar, QProgressBar

from configuration import Config
from Common.ui.common import Button
from server import check_update, download_setup_file

from models import Owner


class GStatusBar(QStatusBar):

    def __init__(self, parent):

        QStatusBar.__init__(self, parent)

        self.setWindowOpacity(1.78)
        self.startTimer(4000)

        self.b = Button("")
        self.progressBar = QProgressBar()

        self.b.clicked.connect(self.update_setup)
        self.cpt = 0

    def update_setup(self):
        self.addWidget(self.progressBar)

        # self.progressBar.setGeometry(30, 40, 200, 25)
        self.progressBar.setValue(2)
        dl = download_setup_file(self.setup_file_url)
        if dl:
            import sys
            sys.exit()
        else:
            self.b.setText("« La mise à jour a échoué ».")
        self.progressBar.close()
        print("Updating ...")

    def timerEvent(self, event):
        self.cpt += 1
        data = check_update()
        # print(data)
        if not data:
            return
        is_last = data.get("is_last")
        self.setup_file_url = data.get("setup_file_url")
        # print(type(is_last))
        if not is_last:
            self.b.setText(data.get("message"))
            self.addWidget(self.b)
        else:
            user = Owner.get(islog=True)
            if self.cpt == 1:
                self.showMessage(
                    """Bienvenue! dans {} un outil rapide et facile à utiliser qui
                    vous permet de faire le suivi de stock""".format(
                        Config.APP_NAME))
            if self.cpt == 2:
                self.showMessage(
                    "User : {} est connecté avec accès {}.".format(
                        user.username, user.group))
            if self.cpt == 3:
                self.showMessage(
                    "{} est un produit de FadCorp ".format(Config.APP_NAME))
