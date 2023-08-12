#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Autor: Fadiga


from __future__ import absolute_import, division, print_function, unicode_literals

from models import FileJoin, History, License, Organization, Owner, Settings, Version
from playhouse.migrate import BooleanField, CharField, migrate


class AdminDatabase(object):
    LIST_CREAT = [History, Owner, Organization, Settings, License, Version, FileJoin]
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
            print("---- database -----")
            from fixture import FixtInit

            FixtInit().create_all_or_pass()

    def make_migrate(self, db_v=1):
        # print(db_v)
        version = Version.get(Version.id == 1)
        print("number ", version.number, "  db_v : ", db_v)
        if db_v > version.number:
            print("--check migrate--")
            from models import migrator

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
