#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: fadiga

from PyQt4.QtCore import QThread, SIGNAL, QObject, Qt
import json

# import os
import requests
from threading import Event
from Common.models import Settings, Organization, License
from Common.ui.util import get_serv_url, internet_on

from server import Network


class UpdaterInit(QObject):
    def __init__(self):
        QObject.__init__(self)

        # self.status_bar = QStatusBar()
        self.stopFlag = Event()
        self.check = TaskThreadUpdater(self)
        self.connect(
            self.check, SIGNAL('update_data'), self.update_data, Qt.QueuedConnection
        )
        self.check.start()

    def update_data(self, orga_slug):
        # print("update_data")
        from configuration import Config
        from database import Setup

        self.base_url = Config.BASE_URL
        print("UpdaterInit start")

        self.emit(SIGNAL("contact_server"))
        for m in Setup.LIST_CREAT:
            for d in m.select().where(m.is_syncro == False):
                d = d.data()
                d.update({"slug": orga_slug})
                # print("sending :", d)
                resp = Network().submit("update-data", d)
                # print("resp : ", resp)
                if resp.get("save"):
                    d.updated()


class TaskThreadUpdater(QThread):
    def __init__(self, parent):
        QThread.__init__(self, parent)
        self.parent = parent
        self.stopped = parent.stopFlag

    def run(self):
        # from Common.ui.statusbar import GStatusBar

        w = 5
        while not self.stopped.wait(w):
            # GStatusBar().update_data()
            if not internet_on(get_serv_url('')):
                print("Pas de d'internet !")
                return
            # print("RUN {}".format(self.stopped))
            w = 20
            self.emit(SIGNAL("contact_server"))
            if Settings().select().count() == 0:
                return
            orga_slug = Organization.get(id=1).slug
            # print("orga_slug ", orga_slug)
            if not orga_slug:
                rep_serv = Network().get_or_inscript_app()

            resp = Network().submit(
                "check_org", {'orga_slug': orga_slug, "lcse": License.get(id=1).code}
            )
            print(resp)
            if resp.get('is_syncro'):
                self.parent.update_data(orga_slug)
