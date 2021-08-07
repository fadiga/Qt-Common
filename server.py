#!/usr/bin/env python

import json
import requests


from PyQt4.QtCore import QObject

from Common.ui.util import internet_on, date_to_ts, get_serv_url
from configuration import Config
from info_hot import getSystemInfo
from Common.models import License


class Network(QObject):
    def __init__(self):
        QObject.__init__(self)

        if not Config.SERV:
            print("Not Serveur ")
            return
        print("Connexion serveur ...")

    def submit(self, url, data):
        # print("submit", data)
        if internet_on(Config.BASE_URL):
            client = requests.session()
            response = client.get(url, data=json.dumps(data))
            try:
                print("response : ", json.loads(response.content.decode('UTF-8')))
                return json.loads(response.content.decode('UTF-8'))
            except ValueError:
                return False
            except Exception as e:
                print(e)
        else:
            pass

    def update_version_checher(self):
        url_ = get_serv_url("desktop_client")
        print("update_version_checher", url_)
        data = {
            "app_info": {"name": Config.APP_NAME, "version": Config.APP_VERSION},
            "getSystemInfo": json.loads(getSystemInfo()),
        }

        lcse_dic = []
        if Config.LSE:
            for lcse in License.select():
                acttn_date = date_to_ts(lcse.activation_date)
                lcse_dic.append(
                    {
                        # "owner": lcse.owner,
                        "code": lcse.code,
                        "isactivated": lcse.isactivated,
                        "activation_date": acttn_date,
                        "can_expired": lcse.can_expired,
                        "expiration_date": date_to_ts(lcse.expiration_date)
                        if lcse.can_expired
                        else acttn_date,
                    }
                )
            data.update({"licenses": lcse_dic})
        return self.submit(url_, data)

    def check_licence(self):
        pass

    def get_licence(self):
        url_ = get_serv_url("license")
        print("update_license_checher", url_)
        data = {"app_info": {"name": Config.APP_NAME, "version": Config.APP_VERSION}}
        lcse_dic = []
        for lcse in License.select():
            acttn_date = date_to_ts(lcse.activation_date)
            lcse_dic.append(
                {
                    # "owner": lcse.owner,
                    "code": lcse.code,
                    "isactivated": lcse.isactivated,
                    "activation_date": acttn_date,
                    "can_expired": lcse.can_expired,
                    "expiration_date": date_to_ts(lcse.expiration_date)
                    if lcse.can_expired
                    else acttn_date,
                }
            )
        data.update({"licenses": lcse_dic})
        return self.submit(url_, data)
