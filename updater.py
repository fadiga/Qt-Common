#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: fadiga

from PyQt4.QtCore import QThread, SIGNAL, QObject, Qt
import json
# import os
import requests
from threading import Event
from configuration import Config
from Common.models import License
from Common.ui.util import internet_on


class UpdaterInit(QObject):

    def __init__(self):
        QObject.__init__(self)
        self.base_url = Config.BASE_URL
        if not Config.SERV:
            return
        # self.status_bar = QStatusBar()
        print("TTTTTTTTTTT")
        self.stopFlag = Event()
        self.check = TaskThreadServer(self)
        self.connect(self.check, SIGNAL('UpdaterInit'), self.update_data,
                     Qt.QueuedConnection)
        self.check.start()

    def update_data(self):
        print("update_data")
        if not internet_on(self.base_url):
            # print("Pas de d'internet !")
            return

        if Office().select().count() == 0:
            return
        lse = License().select().where(License.id == 1).get()
        if not lse.isactivated:
            print("is not activated")
            return

        office = Office().select().where(Office.id == 1).get()
        if not office.is_syncro:
            resp = self.sender("add-office", office.data())
            if resp.get("save"):
                office.updated()

        for model in [CooperativeCompanie, CooperativeMember, CheckList, Demande, Immatriculation]:
            for m in model.all():
                if not m.is_syncro:
                    print("sending :", model)
                    resp = self.sender("update-data", m.data())
                    # print("resp : ", resp)
                    if resp.get("save"):
                        m.updated()

        # self.emit(SIGNAL("UpdaterInit"))

    def sender(self, url, data):
        client = requests.session()
        url_ = self.base_url + "/scoop/" + url
        response = client.get(url_, data=json.dumps(data))
        try:
            return json.loads(response.content.decode('UTF-8'))
        except ValueError as e:
            return {"save": False, "msg_error": e}
        except Exception as e:
            print(e)


class TaskThreadServer(QThread):

    def __init__(self, parent):
        QThread.__init__(self, parent)
        self.parent = parent
        self.stopped = parent.stopFlag

    def run(self):
        while not self.stopped.wait(20):
            print("RUN {}".format(self.stopped))
            self.parent.update_data()
