#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu
# maintainer: Fadiga

from __future__ import (
    unicode_literals, absolute_import, division, print_function)

from PyQt4.QtGui import QDialog
from Common.cstatic import CConstants
from Common.models import SettingsAdmin, Owner

from Common.ui.login import LoginWidget
from Common.ui.license_view import LicenseViewWidget
from Common.ui.user_add_or_edit import NewOrEditUserViewWidget


def cmain():
    settg = SettingsAdmin().get(id=1)
    if CConstants.DEBUG:
        print("Debug is True")
        return True
    elif not settg.can_use:
        if LicenseViewWidget(parent=None).exec_() == QDialog.Accepted:
            return True
    elif Owner().select().where(Owner.isactive == True).count() == 0:
        if NewOrEditUserViewWidget().exec_() == QDialog.Accepted:
            return True
    elif not settg.login:
        return True
    elif LoginWidget().exec_() == QDialog.Accepted:
        return True
    return False
