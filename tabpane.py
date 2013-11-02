#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: Fad

from PyQt4.QtGui import QTabWidget
from common.ui.common import TabPane


def tabbox(*args):
    """ adds a box with tab
    params:  (widget, title) title is the string """
    tab_widget = QTabWidget()
    tab_widget.setMovable(True)
    tab_widget.setAutoFillBackground(True)
    # tab_widget.setTabShape(QTabWidget.Triangular)
    # tab_widget.setTabPosition(QTabWidget.West)

    for box, btitle in args:
        pane = TabPane()
        pane.addBox(box)
        tab_widget.addTab(pane, btitle)
    return tab_widget
