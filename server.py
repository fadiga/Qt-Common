#!/usr/bin/env python

import json
import requests
import platform
import os

from Common.models import License, Organization

from PyQt4.QtCore import QThread, SIGNAL, QObject

from Common.ui.util import internet_on, date_to_ts, to_timestamp
from configuration import Config

base_url = Config.BASE_URL


# class TaskThreadServerM(QThread):

#     def __init__(self, parent):
#         QThread.__init__(self, parent)
#         self.parent = parent

#     def run(self):
#         self.parent.submit()
#         self.emit(SIGNAL("download_finish"))


class Network(QObject):

    def __init__(self):
        QObject.__init__(self)

        if not Config.SERV:
            print("Not Serveur ")
            return

        # self.check = TaskThreadServerM(self)
        # QObject.connect(self.check, SIGNAL("download_"), self.download_)
        # self.check.start()

    def submit(self, url, data):
        print("submit")
        if internet_on(Config.BASE_URL):
            client = requests.session()
            response = client.get(url, data=json.dumps(data))
            print("response: ", response)
            try:
                return json.loads(response.content.decode('UTF-8'))
            except ValueError:
                return False
        else:
            print("Pas de Connexion")

    def update_version_checher(self):
        url_ = base_url + "client/desktop_client"
        data = {
            "app_info": {
                "name": Config.APP_NAME,
                "version": Config.APP_VERSION
            }
        }
        lcse_dic = []
        if Config.LSE:
            for lcse in License.select():
                acttn_date = date_to_ts(lcse.activation_date)
                lcse_dic.append({
                    # "owner": lcse.owner,
                    "code": lcse.code,
                    "isactivated": lcse.isactivated,
                    "activation_date": acttn_date,
                    "can_expired": lcse.can_expired,
                    "expiration_date": date_to_ts(
                        lcse.expiration_date) if lcse.can_expired else acttn_date,
                })
            data.update({"licenses": lcse_dic})

        return self.submit(url_, data)
