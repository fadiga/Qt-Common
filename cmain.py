#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu
# maintainer: Fadiga

from __future__ import (
    unicode_literals, absolute_import, division, print_function)

from PyQt4.QtGui import QDialog

import locale
import gettext
import gettext_windows

from Common.cstatic import CConstants
from Common.models import Owner

from Common.ui.util import is_valide_mac
from Common.ui.login import LoginWidget
from Common.ui.import_db import ImportBDWidget
from Common.ui.license_view import LicenseViewWidget
from Common.ui.user_add_or_edit import NewOrEditUserViewWidget
# from Common.ui.organization_add_or_edit import NewOrEditOrganizationViewWidget


def cmain():

    gettext_windows.setup_env()
    locale.setlocale(locale.LC_ALL, '')
    gettext.install('main.py', localedir='locale')

    if CConstants.DEBUG:
        print("Debug is True")
        return True

    if Owner().select().where(Owner.isactive == True).count() == 0:
        if not ImportBDWidget().exec_() == QDialog.Accepted:
            return

    if Owner().select().where(Owner.isactive == True).count() == 0:
        if not NewOrEditUserViewWidget().exec_() == QDialog.Accepted:
            return

    # if Organization().select().count() == 0:
    #     if not NewOrEditOrganizationViewWidget().exec_() == QDialog.Accepted:
    #         return

    if CConstants.LSE:
        if not is_valide_mac() == CConstants.OK:
            if not LicenseViewWidget(parent=None).exec_() == QDialog.Accepted:
                return
    if LoginWidget().exec_() == QDialog.Accepted:
        return True
    return False
