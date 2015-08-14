#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Autor: Fadiga

from __future__ import (
    unicode_literals, absolute_import, division, print_function)

from Common.models import Owner, Organization, SettingsAdmin, Version


class AdminFixture(object):

    LICENSE = '3483f0d7f57528841134b5802d64794234a2e85f'
    LICENSE = 'trial pour le demo'

    LIST_CREAT = [SettingsAdmin(license=LICENSE, tolerance=130, user="Demo"),
                  Version(number=1),
                  Organization(slug=Organization.DEFAULT, adress_org="",
                               name_orga="demo s.a.r.l", bp="demo", login=True,
                               email_org="demo@demo.ml", phone=76433890,)]

    def creat_all_or_pass(self):

        print(u"---- Init fixture -----")
        for f in self.LIST_CREAT:
            try:
                f.save()
            except Exception as e:
                print(e)
