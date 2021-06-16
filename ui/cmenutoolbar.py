# !/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: fad

from __future__ import unicode_literals, absolute_import, division, print_function

from PyQt4.QtGui import QIcon, QToolBar, QCursor
from PyQt4.QtCore import Qt, QSize

from Common.ui.common import FMainWindow

from configuration import Config


class FMenuToolBar(QToolBar, FMainWindow):
    def __init__(self, parent=None, *args, **kwargs):
        QToolBar.__init__(self, parent, *args, **kwargs)

        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        # self.setToolButtonStyle(Qt.ToolButtonFollowStyle)
        self.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        # self.setToolButtonStyle(Qt.ToolButtonIconOnly)
        # self.setToolButtonStyle(Qt.ToolButtonTextOnly)
        self.setOrientation(Qt.Vertical)

        # self.setIconSize(QSize(135, 35))
        # font = QFont()
        # font.setPointSize(10)
        # font.setBold(True)
        # font.setWeight(35)
        # self.setFont(font)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        # self.setFocusPolicy(Qt.TabFocus)
        # self.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.setAcceptDrops(True)
        # self.setAutoFillBackground(True)
        # self.addSeparator()
        self.addAction(
            QIcon(u"{}exit.png".format(Config.img_cmedia)), u"Quiter", self.goto_exit
        )

        menu = []

    def goto(self, goto):
        self.change_main_context(goto)

    def goto_exit(self):
        self.parent().exit()
