#!/usr/bin/env python


import json
import requests
import platform

from Common.models import License, Organization

from PyQt4.QtCore import QObject

from Common.ui.util import internet_on, date_to_ts, to_timestamp
from configuration import Config

base_url = Config.BASE_URL


class Network(QObject):

    def __init__(self, parent):

        QObject.__init__(self, parent)

        if not Config.SERV:
            print("Not Serveur ")
            return

    #     self.t = TaskThreadServer(self)
    #     # QObject.connect(self.t, SIGNAL("rsp_server()"), self.rsp_server)
    #     self.t.start()

    # def start(self):
    #     return self.rsp


def desktop_client():

    if not internet_on(Config.BASE_URL):
        print("pas de connexion")
        return False
    else:
        print("Connexion OK")

        data = {
            "app_info": {
                "name": Config.APP_NAME,
                "version": Config.APP_VERSION
            }
        }
        lcse_dic = []
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

        host_info = {
            "platform": platform.platform(),
            "system": platform.system(),
            "version": platform.version(),
            "node": platform.node(),
            "processor": platform.processor()
        }
        data.update({"host_info": host_info})
        organ = Organization().get(id=1)
        info_organization = {
            'name_orga': organ.name_orga,
            'phone': organ.phone,
            'bp': organ.bp,
            'email_org': organ.email_org,
            'adress_org': organ.adress_org,
            'devise': organ.devise,
        }
        data.update({"organization": info_organization})
        # license
        url_ = base_url + "desktop_client"
        client = requests.session()
        response = client.get(url_, data=json.dumps(data))
        print(response)
        try:
            return json.loads(response.content.decode('UTF-8'))
        except ValueError:
            return False
