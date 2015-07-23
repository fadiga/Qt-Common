#!/usr/bin/env python
# -*- coding: utf8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu
# maintainer: Fad
# from __future__ import (unicode_literals, absolute_import, division, print_function)

import re
import subprocess
import os

try:
    unicode
except NameError:
    unicode = str

def get_mac():

    try:
        # Linux
        ifconfig = os.popen('ifconfig').readlines()
        for ligne in ifconfig:
            if 'hwaddr' in ligne.lower():
                adresse_mac = ligne.split('HWaddr')[1].strip()
        return adresse_mac

    except OSError:
        # windows
        ipconfig = subprocess.Popen(['ipconfig', '/all'], shell=True, stdout=subprocess.PIPE)
        result = ipconfig.stdout.read()
        adresse_mac = re.search('([0-9A-F]{2}-?){6}', unicode(result)).group()
        return adresse_mac
    except Exception as e:
        print(e)
        return ""
