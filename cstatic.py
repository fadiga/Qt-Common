#!/usr/bin/env python
# -*- coding: utf8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu
# Maintainer: Fad

import os
# from Common.models import Organization, Version

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath('__file__')))


class CConstants(object):

    """ """
    # PERIODS
    W = "week"
    M = "month"
    OK = 'ok'
    IS_NOT_ACTIVATED = "is_not_activated"
    IS_EXPIRED = "is_expired"

    import logging

    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S')

    file_img = os.path.join(
        os.path.dirname(os.path.abspath('__file__')), 'cimages/')
    # deployment
    if os.path.exists(file_img):
        img_cmedia = file_img
    else:
        img_cmedia = os.path.join(ROOT_DIR, "Common", "cimages/")
    # ------------------------- Autor --------------------------#
    AUTOR = u"Fadiga Ibrahima"
    EMAIL_AUT = u"ibfadiga@gmail.com"
    TEL_AUT = u"(+223)76 43 38 90 \n (+223)63 34 14 24"
    ADRESS_AUT = u"Boulkassoumbougou Bamako"
    ORG_AUT = u"Copyright © 2012 xxxx"
    # ------------------------- Application --------------------------#
    inco_exit = ""
    inco_dashboard = ""
    EMAIL_ORGA = ""
    APP_NAME = u"Projet en dev"
    APP_DATE = u"02/2013"
    APP_VERSION = "1.7"
    DEBUG = False

    EXCLUDE_MENU_ADMIN = []
    LSE = False
    ORG = False
    SERV = None
    list_models = []
    APP_LOGO = os.path.join(img_cmedia, "logo.png")
    APP_LOGO_ICO = os.path.join(img_cmedia, "logo.ico")
    ExportFolders = []
    ExportFiles = []
    # BASE_URL = "http://192.168.1.31:9001/"
    # BASE_URL = "http://192.168.5.51:9001/"
    # BASE_URL = "http://172.20.10.3:9001/"
    BASE_URL = "http://fadcorp.ml/"
