#!/usr/bin/env python
# -*- coding: utf8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu
# maintainer: Fad
# from __future__ import (unicode_literals, absolute_import, division, print_function)

import re
import subprocess


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


# def is_valide_mac(license):
#     """ check de license """
#     return license.has_key(get_mac())
