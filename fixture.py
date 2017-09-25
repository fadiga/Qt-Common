#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Autor: Fadiga

from __future__ import (
    unicode_literals, absolute_import, division, print_function)


from Common.models import SettingsAdmin, Organization, License, Version


class AdminFixture(object):

    LIST_CREAT = [
        SettingsAdmin(user="Demo"),
        Version(number=1),
        Organization(slug=Organization.DEFAULT, adress_org="",
                     name_orga="demo s.a.r.l", bp="demo", login=True,
                     email_org="demo@demo.ml", phone=00000000,)]

    def create_all_or_pass(self):

        print(u"---- Init fixture -----")

        for f in self.LIST_CREAT:
            try:
                f.save()
            except Exception as e:
                print(e)
