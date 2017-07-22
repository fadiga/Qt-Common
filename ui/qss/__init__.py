#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: Fad
# ###############################
# #                             #
# #  Coded By: Ibrihima Fadiga  #
# #  Original: 10/12/15         #
# #  File: style CSS PyQt       #
# ###############################

from __future__ import (
    unicode_literals, absolute_import, division, print_function)

import platform
import os

from Common.models import SettingsAdmin
ROOT_DIR = os.path.dirname(os.path.realpath(__file__))


def load_stylesheet(file_qss):
    """
    """
    from PyQt4.QtCore import QFile, QTextStream
    f = QFile("{}.css".format(os.path.join(ROOT_DIR, file_qss)))
    if not f.exists():
        print("Unable to load stylesheet, file not found in "
              "resources")
        return ""
    else:
        f.open(QFile.ReadOnly | QFile.Text)
        ts = QTextStream(f)
        stylesheet = ts.readAll()
        if platform.system().lower() == 'darwin':  # see issue #12 on github
            mac_fix = '''
            QDockWidget::title
            {
                background-color: #353434;
                text-align: center;
                height: 12px;
            }
            '''
            stylesheet += mac_fix
        return stylesheet


dict_style = {1: ["Theme systeme", ""],
              2: ["Dark", load_stylesheet("dark")],
              3: ["DSView", load_stylesheet("DSView")],
              4: ["Tangerine", load_stylesheet("tangerine")],
              5: ["Coffee", load_stylesheet("coffee")],
              6: ["F", load_stylesheet("fad")],
              7: ["Fat", load_stylesheet("fat")],
              }

appStyle = dict_style.get(SettingsAdmin.get(id=1).style_number)[1]
