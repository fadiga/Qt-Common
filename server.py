#!/usr/bin/env python

import json
import requests


from PyQt4.QtCore import QObject

from Common.ui.util import internet_on, datetime_to_str, get_serv_url, make_lcse
from configuration import Config
from info_hot import getSystemInfo
from Common.models import License, Organization, Settings, Owner, Version


class Network(QObject):
    def __init__(self):
        QObject.__init__(self)

        if not Config.SERV:
            print("Not Serveur ")
            return
        # print("Connexion serveur ...")

    def submit(self, url, data):
        # print("submit", data, " url ", url)
        if internet_on(Config.BASE_URL):
            client = requests.session()
            response = client.get(get_serv_url(url), data=json.dumps(data))
            try:
                # print("response : ", json.loads(response.content.decode('UTF-8')))
                return json.loads(response.content.decode('UTF-8'))
            except Exception as e:
                print("Error : ", e)
                return False
            except Exception as e:
                print(e)
        else:
            pass

    def update_version_checher(self):

        # print("update_version_checher")
        data = {
            "app_info": {"name": Config.APP_NAME, "version": Config.APP_VERSION},
            "getSystemInfo": json.loads(getSystemInfo()),
        }

        lcse_dic = []
        if Config.LSE:
            for lcse in License.select():
                acttn_date = datetime_to_str(lcse.activation_date)
                lcse_dic.append(
                    {
                        # "owner": lcse.owner,
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

    def check_licence(self):
        pass

    def get_licence(self):
        # print("update_license_checher")
        data = {"app_info": {"name": Config.APP_NAME, "version": Config.APP_VERSION}}
        lcse_dic = []
        for lcse in License.select():
            acttn_date = datetime_to_str(lcse.activation_date)
            lcse_dic.append(
                {
                    # "owner": lcse.owner,
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
        return self.submit("license", data)

    def get_or_inscript_app(self):
        orga = Organization.get(id=1)
        sttg = Settings.get(id=1)
        data = {
            "app_info": {"name": Config.APP_NAME, "version": Config.APP_VERSION},
            "getSystemInfo": json.loads(getSystemInfo()),
            "organization": {'slug': orga.slug, 'data': orga.data()},
            # "settings": sttg.data(),# "owner": [i.data() for i in Owner.all()],
            "licenses": [i.data() for i in License.all()],
        }
        # print(data)
        rep = self.submit("inscription_client", data)
        # print(rep)
        if rep.get('is_create'):
            orga.slug = rep.get('org_slug')
            orga.save()
        return rep
