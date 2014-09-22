#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Autor: Fadiga

from __future__ import (unicode_literals, absolute_import, division, print_function)

from Common.models import Owner, Organization, SettingsAdmin, Version


class AdminFixture(object):

    PASS = "36cb1f4ebf4298c14c96ab541a454870fa53455d5431d1afe1d0af87" #'fad 86'
    PASS1 = "4b91d93da8bc69d1360c449c79edf8dc9b24b385807c8d887d389471" #'ano 86'

    LICENSE = '3483f0d7f57528841134b5802d64794234a2e85f'
    LICENSE = 'trial pour le demo'

    LIST_CREAT = [Owner(username="root", password=PASS,  login_count=0,
                        group="superuser", isvisible=False),
                  Owner(username="anomime", password=PASS1, group="admin",
                        isvisible=False, login_count=0),
                  SettingsAdmin(license=LICENSE, tolerance=130, user="Demo"),
                  Version(number=1),
                  Organization(slug=Organization.DEFAULT, adress_org="",
                               name_orga="demo s.a.r.l", bp="demo", login=True,
                               email_org="demo@demo.ml", phone=76433890,)]

    def creat_all_or_pass(self):

        print(u"---- Init fixture -----")
        for f in self.LIST_CREAT:
            try:
                f.save()
                # print(u"{} est Creé".format(f.display_name()).encode('utf-8'))
            except Exception, e:
                print(e)
