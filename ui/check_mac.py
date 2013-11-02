#!/usr/bin/python
# -*- coding: utf-8 -*-
# maintainer: Fadiga

import re
import subprocess

from configuration import Config


def get_mac():

    try:
        # windows
        ipconfig = subprocess.Popen(['ipconfig', '/all'], stdout=subprocess.PIPE)
        result = ipconfig.stdout.read()
        adresse_mac = re.search('([0-9A-F]{2}-?){6}', result).group()
        return adresse_mac
    except OSError:
        # Linux
        import os
        ifconfig = os.popen('ifconfig').readlines()

        for ligne in ifconfig:
            if 'hwaddr' in ligne.lower():
                adresse_mac = ligne.split('HWaddr')[1].strip()
        return adresse_mac
    except:
        return None


def is_valide_mac():
    """ check de license """
    return Config.license.has_key(get_mac())
