#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: fadiga

from PyQt4.QtCore import QThread, SIGNAL, QObject, Qt
import json

# import os
import requests
from threading import Event
from Common.models import Settings
from Common.ui.util import internet_on

from server import Network


class UpdaterInit(QObject):
    def __init__(self):
        QObject.__init__(self)

        # self.status_bar = QStatusBar()
        self.stopFlag = Event()
        self.check = TaskThreadServer(self)
        self.connect(
            self.check, SIGNAL('update_data'), self.update_data, Qt.QueuedConnection
        )
        self.check.start()

    def update_data(self):
        print("update_data")
        from configuration import Config
        from database import Setup

        self.base_url = Config.BASE_URL
        print("UpdaterInit start")
        if not internet_on(self.base_url):
            print("Pas de d'internet !")
            return
        else:
            print("Is connected")

        if Settings().select().count() == 0:
            return

        for m in Setup.LIST_CREAT:
            # print(m)
            for d in m.select().where(m.is_syncro == False):
                print("sending :", d.data())
                resp = Network().submit("update-data", d.data())
                print("resp : ", resp)
                if resp.get("save"):
                    d.updated()

        self.emit(SIGNAL("update_data"))


class TaskThreadServer(QThread):
    def __init__(self, parent):
        QThread.__init__(self, parent)
        self.parent = parent
        self.stopped = parent.stopFlag

    def run(self):
        while not self.stopped.wait(5):
            # print("RUN {}".format(self.stopped))
            self.parent.update_data()
