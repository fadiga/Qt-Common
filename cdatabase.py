#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Autor: Fadiga


from __future__ import (
    unicode_literals, absolute_import, division, print_function)

from Common.models import (
    Owner, Organization, License, Version, FileJoin, History)


class AdminDatabase(object):

    LIST_CREAT = [History, Owner, Organization, License, Version, FileJoin]
    CREATE_DB = True

    def create_all_or_pass(self, drop_tables=False):
        did_create = False
        for model in self.LIST_CREAT:
            if drop_tables:
                model.drop_table()
            if not model.table_exists():
                model.create_table()
                did_create = True

        if did_create:
            print(u"---- database -----")
            from fixture import FixtInit
            FixtInit().create_all_or_pass()
