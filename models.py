#!/usr/bin/env python
# -*- coding: utf8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu
# maintainer: Fad
from __future__ import (unicode_literals, absolute_import, division, print_function)

import hashlib


from datetime import datetime
from common import peewee
# import peewee

DB_FILE = "database.db"
dbh = peewee.SqliteDatabase(DB_FILE)


class BaseModel(peewee.Model):

    class Meta:
        database = dbh

    @classmethod
    def all(cls):
        return list(cls.select())


class Owner(BaseModel):
    """ The web user who is also owner of the Organization
    """

    USER = 0
    ADMIN = 1
    ROOT = 2
    GROUPS = ((USER, u"user"),
              (ADMIN, u"admin"),
              (ROOT, u"superuser"))

    group = peewee.CharField(choices=GROUPS, default=USER)
    islog = peewee.BooleanField(default=False)
    phone = peewee.CharField(max_length=30, blank=True, null=True, verbose_name=("Telephone"))
    username = peewee.CharField(max_length=30, unique=True, verbose_name=("Nom d'utilisateur"))
    password = peewee.CharField(max_length=150)
    isactive = peewee.BooleanField(default=True)
    last_login = peewee.DateTimeField(default=datetime.now())
    login_count = peewee.IntegerField(default=0)

    def __str__(self):
        return u"{}".format(self.username)

    def full_mane(self):
        return u"{name}/{group}/{login_count}".format(name=self.username,
                                                      group=self.group,
                                                      login_count=self.login_count)

    def crypt_password(self, password):
        return hashlib.sha224(password).hexdigest()

    def save(self):
        if self.islog:
            self.login_count += 1

        super(Owner, self).save()