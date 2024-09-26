#!/usr/bin/env python
# -*- coding: utf8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu
# Maintainer: Fad

import logging
import os
from pathlib import Path

# ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", datefmt="%m/%d/%Y %I:%M:%S"
)

logger.setLevel(logging.DEBUG)


class CConstants(object):

    """ """

    # PERIODS
    W = "week"
    M = "month"
    OK = "ok"
    IS_NOT_ACTIVATED = "is_not_activated"
    IS_EXPIRED = "is_expired"
    img_media = "static/images/"
    NAME_MAIN = "main.py"
    # img_media = os.path.join(ROOT_DIR, "static", "images/")
    img_cmedia = str(Path(__file__).parent.joinpath("cimages").resolve()) + "/"

    IBS_LOGO = os.path.join(img_cmedia, "ibs.jpg")
    # ------------------------- Autor --------------------------#
    AUTOR = "Fadiga Ibrahima"
    EMAIL_AUT = "ibfadiga@gmail.com"
    TEL_AUT = "(+223)76 43 38 90"
    ADRESS_AUT = "Boulkassoumbougou Bamako"
    ORG_AUT = "Copyright © 2012 xxxx"
    # ------------------------- Application --------------------------#
    inco_exit = ""
    inco_dashboard = ""
    EMAIL_ORGA = ""
    APP_NAME = "Projet en dev"
    APP_DATE = "02/2013"
    APP_VERSION = "1.7"
    DEBUG = False

    des_image_record = Path(__file__)
    EXCLUDE_MENU_ADMIN = []
    LSE = True
    ORG = False
    SERV = False
    list_models = []
    APP_LOGO = os.path.join(img_media, "logo.png")
    APP_LOGO_ICO = os.path.join(img_media, "logo.ico")
    ExportFolders = []
    ExportFiles = []
    BASE_URL = "https://file-repo.ml"
