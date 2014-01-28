#!/usr/bin/env python
# -*- coding: utf8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu
# Maintainer: Fad

import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath('__file__')))


class CConstants(object):
    """ """
    # PERIODS
    W = "week"
    M = "month"

    # type_period = W
    # des_image_prod = os.path.join(ROOT_DIR, "cmedia/img_prod")
    img_cmedia = os.path.join(ROOT_DIR, "Cmedia/images/")

    # ------------------------- Autor --------------------------#
    AUTOR = u"Fadiga Ibrahima"
    EMAIL_AUT = u"ibfadiga@gmail.com"
    TEL_AUT = u"(223)76 43 38 90 ou (223)63 34 14 24"
    ADRESS_AUT = u"Boulkassoumbougou Bamako"
    ORG_AUT = u"Copyright © 2012 xxxx"
    # ------------------------- Application --------------------------#
    inco_exit = ""
    inco_dashboard = ""

    APP_NAME = u"Projet en dev"
    APP_DATE = u"02/2013"

    license = {'e8:11:32:6c:30:28': 'Fad ubuntu 13.10',
               '30:85:a9:17:b1:00': 'ASUS Bureau',
               'E8-11-32-6C-30-28': 'Fad Wind',
               '08:00:27:38:F8:23': 'Fad Wind Virtual'}

    APP_LOGO = "{}logo.png".format(img_cmedia)
    APP_LOGO_ICO = "{}logo.ico".format(img_cmedia)
