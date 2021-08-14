#!/usr/bin/env python

import json
import requests


from PyQt4.QtCore import QObject

from Common.ui.util import internet_on, datetime_to_str, get_serv_url, is_valide_mac

from info_hot import getSystemInfo
from Common.models import License, Organization, Settings, Owner, Version


class Network(QObject):
    def __init__(self):
        QObject.__init__(self)

        print("Connexion serveur ...")

    def submit(self, url, data):
        print("submit", 'data', " url ", url)
        if internet_on():
            client = requests.session()
            response = client.get(get_serv_url(url), data=json.dumps(data))
            if response.status_code == 200:
                # print(response.status_code)
                try:
                    return json.loads(response.content.decode('UTF-8'))
                except Exception as e:
                    return {"response": e}
        else:
            return {"response": "Pas d'internet"}

    def update_version_checher(self):

        # print("update_version_checher")

        from configuration import Config

        orga = Organization.get(id=1)
        data = {
            "org_slug": orga.slug,
            "app_info": {"name": Config.APP_NAME, "version": Config.APP_VERSION},
            "getSystemInfo": json.loads(getSystemInfo()),
            "current_lcse": is_valide_mac()[0].code,
        }

        lcse_dic = []
        # if Config.LSE:
        for lcse in License.select():
            acttn_date = datetime_to_str(lcse.activation_date)
            lcse_dic.append(
                {
                    "code": lcse.code,
                    "isactivated": lcse.isactivated,
                    "activation_date": acttn_date,
                    "can_expired": lcse.can_expired,
                    "expiration_date": datetime_to_str(lcse.expiration_date)
                    if lcse.can_expired
                    else acttn_date,
                }
            )
        data.update({"licenses": lcse_dic})

        return self.submit("desktop_client", data)

    def get_or_inscript_app(self):

        from configuration import Config

        orga = Organization.get(id=1)
        sttg = Settings.get(id=1)
        data = {
            "app_info": {"name": Config.APP_NAME, "version": Config.APP_VERSION},
            "getSystemInfo": json.loads(getSystemInfo()),
            "organization": {'slug': orga.slug, 'data': orga.data()},
            "licenses": [i.data() for i in License.all()],
        }

        rep = self.submit("inscription_client", data)

        if rep.get('is_create'):
            orga.slug = rep.get('org_slug')
            orga.save()
        return rep
