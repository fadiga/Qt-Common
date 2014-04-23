#!/usr/bin/env python
# -*- coding: utf8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu
# maintainer: Fad
from __future__ import (unicode_literals, absolute_import, division, print_function)

import re
import subprocess
import hashlib


from datetime import datetime
from Common import peewee
from Common.check_mac import get_mac

DB_FILE = "database.db"
# dbh = peewee.SqliteDatabase(DB_FILE, threadlocals=True)
dbh = peewee.SqliteDatabase(DB_FILE)
dbh.connect()


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
    phone = peewee.CharField(max_length=30, null=True, verbose_name=("Telephone"))
    username = peewee.CharField(max_length=30, unique=True, verbose_name=("Nom d'utilisateur"))
    password = peewee.CharField(max_length=150)
    isactive = peewee.BooleanField(default=True)
    isvisible = peewee.BooleanField(default=True)
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
            stt=SettingsAdmin().select().get()
            stt.tolerance -= 1
            stt.save()
        super(Owner, self).save()


class Settings(BaseModel):
    """docstring for Settings"""
    PREV = 0
    CURRENT = 1
    DEFAULT = 2
    LCONFIG = ((PREV, u"Precedent"),
              (DEFAULT, u"Par defaut"),
              (CURRENT, u"Actuel"),)

    slug = peewee.CharField(choices=LCONFIG, default=DEFAULT)
    login = peewee.BooleanField(default=True)
    name_orga = peewee.CharField('')
    phone = peewee.IntegerField('')
    bp = peewee.CharField('')
    email_org = peewee.CharField('')
    adress_org = peewee.TextField('')

    def __str__(self):
        return self.full_mane()

    def change_prev(self):
        self.slug = PREV
        self.save()

    def full_mane(self):
        return u"{}/{}/{}".format(self.name_orga, self.phone, self.email_org)


class SettingsAdmin(BaseModel):
    """docstring for SettingsAdmin"""
    user = peewee.CharField()
    date = peewee.DateTimeField(default=datetime.now())
    license = peewee.CharField()
    tolerance = peewee.IntegerField(default=0)

    def __str__(self):
        return u"{}/{}".format(self.license, self.user)

    @property
    def clean_mac(self):
        return get_mac().replace(":", "").replace("-","")

    def is_valide_mac(self, license):
        """ check de license """
        return license == hashlib.sha1(self.clean_mac).hexdigest()

    def can_use(self):

        if not self.is_valide_mac(self.license):
            if self.tolerance > 0:
                return True
            else:
                return False
        else:
            return True


class Version(BaseModel):
    date = peewee.DateTimeField(default=datetime.now(), verbose_name="Date de Version")
    number = peewee.IntegerField(default=1 , verbose_name="Numéro de Version")

    def __str__(self):
        return "{}/{}".format(self.number, self.date)

    def display_name(self):
        return "V-{}".format(self.number)


    def update_v(self):
        self.number += 1
        self.date = datetime.now()
        self.save()
