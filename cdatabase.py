#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Autor: Fadiga


from __future__ import (
    unicode_literals, absolute_import, division, print_function)

from Common.models import (
    Owner, Organization, License, Version, FileJoin, History, Settings)

from playhouse.migrate import migrate, CharField, BooleanField


class AdminDatabase(object):

    LIST_CREAT = [History, Owner, Organization,
                  Settings, License, Version, FileJoin]
    CREATE_DB = True
    LIST_MIGRATE = []

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

    def make_migrate(self, db_v=7):
        print("--check migrate--")
        from Common.models import migrator
        version = Version.get(Version.id == 1)
        print("version ", version.id)
        if db_v != version.number:
            print("Make migrate", self.LIST_MIGRATE)
            for x, y, z in self.LIST_MIGRATE:
                try:
                    migrate(migrator.add_column(x, y, z))
                    print(x, " : ", y)
                except Exception as e:
                    print(e)
                    pass
            version.number = db_v
            version.save()
            print("After save")
