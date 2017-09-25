#!/usr/bin/env python

import os
import json
import requests
import platform

# from Common.models import License
from Common.ui.util import internet_on, date_to_ts, to_timestamp
from configuration import Config

base_url = Config.BASE_URL

# check network connexion
# check if


def send_info_pc():

    if not internet_on(Config.BASE_URL):
        print("pas de connexion")
        return False
    else:
        print("Connexion OK")
        url_info = base_url + "info-pc"
        data = {
            "app_name": Config.APP_NAME,
            "syst_info": {
                "platform": platform.platform(),
                "system": platform.system(),
                "version": platform.version(),
                "node": platform.node(),
                "processor": platform.processor()
            }, "version": {
                "number": ""}
        }

        client = requests.session()
        requests.get(url_info)
        response = client.post(url_info, data=json.dumps(data))


def send_info(lcses):

    if not internet_on(Config.BASE_URL):
        print("pas de connexion")
        return False
    else:
        print("Connexion OK")
        data = {}
        lcse_dic = {}
        for lcse in lcses:
            acttn_date = date_to_ts(lcse.activation_date)
            print("Code license : ", lcse.code)
            print("Date to ts", date_to_ts(lcse.activation_date))
            print("Date to timestamp", to_timestamp(lcse.activation_date))
            lcse_dic.update({
                "owner": lcse.owner,
                "code": lcse.code,
                "isactivated": lcse.isactivated,
                "activation_date": acttn_date,
                "can_expired": lcse.can_expired,
                "expiration_date": date_to_ts(
                    lcse.expiration_date) if lcse.can_expired else acttn_date,
            })

        data.update({"licenses": lcse_dic})
        # license
        url_lcse = base_url + "license"
        client = requests.session()
        requests.get(url_lcse)
        response = client.post(url_lcse, data=json.dumps(data))

# get info
# update date update


def get_info():
    requests.get(base_url + 'info_pc/' + "")
    return ''


def download_setup_file(file_url):
    url = "{}{}".format(base_url, file_url)
    import shutil
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(os.path.basename(file_url), 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
        try:
            os.startfile(os.path.basename(file_url))
        except OSError:
            return False
        return True


def check_update():
    if not internet_on(Config.BASE_URL):
        print("pas de connexion")
        return False
    else:
        url_update = base_url + 'update'
        client = requests.session()
        requests.get(base_url)
        data = {
            "app_name": Config.APP_NAME, "version_number": Config.APP_VERSION}
        rsp = client.get(url_update, data=json.dumps(data))
        try:
            return json.loads(rsp.content.decode('UTF-8'))
        except ValueError:
            return False


# if not internet_on(Config.BASE_URL):
#     print("pas de connexion")
# else:
#     # get info.

#     # send_info_pc()
#     # get_info()
#     print("Connexion OK")

#     # lcses = License.select()
#     # print(lcses.count())
#     # if lcses.count() <= 0:
#     #     print("not lcse")
#     #     send_info(lcses)


# try:
#     if lcses.count() <= 0:
#         print("not lcse")
#         send_info(lcses)
# except:
#     pass
