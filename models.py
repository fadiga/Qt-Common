#!/usr/bin/env python
# -*- coding: utf8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu
# maintainer: Fad
from __future__ import (unicode_literals, absolute_import, division, print_function)

import os
import time
import hashlib

from datetime import datetime

# from Common import peewee224 as peewee
from Common.check_mac import get_mac

DB_FILE = "database.db"

from Common import peewee
print("Peewee version : " + peewee.__version__)


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

    def display_name(self):
        return u"{name}/{group}/{login_count}".format(name=self.username,
                                                      group=self.group,
                                                      login_count=self.login_count)

    def crypt_password(self, password):
        return hashlib.sha224(str(password).encode("utf-8")).hexdigest()

    def save(self):
        if self.islog:
            self.login_count += 1
            stt = SettingsAdmin().select().get()
            stt.tolerance -= 1
            stt.save()
        super(Owner, self).save()


class Organization(BaseModel):
    """docstring for Organization"""
    PREV = 0
    CURRENT = 1
    DEFAULT = 2
    LCONFIG = ((PREV, u"Precedent"),
               (DEFAULT, u"Par defaut"),
               (CURRENT, u"Actuel"),)

    slug = peewee.CharField(choices=LCONFIG, default=DEFAULT)
    login = peewee.BooleanField(default=True)
    name_orga = peewee.CharField(verbose_name=(""))
    phone = peewee.IntegerField(null=True, verbose_name=(""))
    bp = peewee.CharField(null=True, verbose_name=(""))
    email_org = peewee.CharField(null=True, verbose_name=(""))
    adress_org = peewee.TextField(null=True, verbose_name=(""))

    def __str__(self):
        return self.display_name()

    def change_prev(self):
        self.slug = self.PREV
        self.save()

    def display_name(self):
        return u"{}/{}/{}".format(self.name_orga, self.phone, self.email_org)

    @classmethod
    def get_or_create(cls, name_orga, typ):
        try:
            ctct = cls.get(name_orga=name_orga, type_=typ)
            print(ctct)
        except cls.DoesNotExist:
            ctct = cls.create(name_orga=name_orga, type_=typ)
        return ctct


class SettingsAdmin(BaseModel):
    """docstring for SettingsAdmin"""
    user = peewee.CharField(default="User")
    date = peewee.DateTimeField(default=datetime.now())
    license = peewee.CharField(default=None, null=True)
    tolerance = peewee.IntegerField(default=230)

    def __str__(self):
        return self.display_name()

    def display_name(self):
        return u"{}/{}/{}".format(self.user, self.date, self.license)

    @property
    def clean_mac(self):
        return get_mac().replace(":", "").replace("-", "")

    def is_valide_mac(self, license):
        """ check de license """
        return license == hashlib.md5(str(self.clean_mac).encode('utf-8')).hexdigest()

    @property
    def can_use(self):
        if self.is_valide_mac(self.license) or self.tolerance >= 0:
            return True
        return False


class Version(BaseModel):
    date = peewee.DateTimeField(default=datetime.now(), verbose_name="Date de Version")
    number = peewee.IntegerField(default=1, verbose_name="Numéro de Version")

    def __str__(self):
        return u"{}/{}".format(self.number, self.date)

    def display_name(self):
        return u"V-{}".format(self.number)

    def update_v(self):
        self.number += 1
        self.date = datetime.now()
        self.save()


class FileJoin(BaseModel):

    class Meta:
        ordering = (('file_name', 'desc'))

    file_name = peewee.CharField(max_length=200, null=True)
    file_slug = peewee.CharField(max_length=200, null=True, unique=True)
    on_created = peewee.DateTimeField(default=datetime.now)

    def __str__(self):
        return "{}({})".format(self.file_name, self.file_slug)

    def display_name(self):
        return u"{}".format(self.file_name)

    @property
    def get_file(self):
        from static import Constants
        return os.path.join(Constants.des_image_record, self.file_slug)

    def show_file(self):
        from Common.ui.util import uopen_file
        uopen_file(self.get_file)

    def remove_file(self):
        """ Remove doc and file """
        self.delete_instance()
        try:
            os.remove(self.get_file)
        except TypeError:
            pass

    def isnottrash(self):
        self.trash = False
        self.save()

    @property
    def os_info(self):
        return os.stat(self.get_file)

    @property
    def created_date(self):
        return time.ctime(self.os_info.st_ctime)

    @property
    def modification_date(self):
        return time.ctime(self.os_info.st_mtime)

    @property
    def last_date_access(self):
        return time.ctime(self.os_info.st_atime)

    @property
    def get_taille(self):
        """ La taille du document"""
        octe = 1024
        q = octe
        kocte = octe * octe
        unit = "ko"

        taille_oct = float(self.os_info.st_size)
        if kocte < taille_oct:
            unit = "Mo"
            q = kocte

        taille = round(taille_oct / q, 2)
        return "{} {}".format(taille, unit)
