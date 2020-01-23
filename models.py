#!/usr/bin/env python
# -*- coding: utf8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu
# maintainer: Fad
from __future__ import (
    unicode_literals, absolute_import, division, print_function)

import os
import time
import hashlib
import peewee

# from peewee_migrate import Router
from datetime import timedelta, datetime
from playhouse.migrate import (
    SqliteMigrator, migrate, CharField, BooleanField, DateTimeField)

from Common.ui.util import copy_file

DB_FILE = "database.db"

print("Peewee version : " + peewee.__version__)


NOW = datetime.now()


dbh = peewee.SqliteDatabase(DB_FILE)
migrator = SqliteMigrator(dbh)

list_migrate = []

try:
    from migrations import make_migrate
    list_migrate += make_migrate()
except Exception as e:
    print(e)

for x, y, z in list_migrate:
    try:
        migrate(migrator.add_column(x, y, z))
        print(x, " : ", y)
    except Exception as e:
        print(e)
        # raise e


class BaseModel(peewee.Model):

    class Meta:
        database = dbh

    @classmethod
    def all(cls):
        return list(cls.select())

    def get_or_none(self, obj):
        try:
            return obj.get()
        except:
            return None


class FileJoin(BaseModel):

    DEST_FILES = "Files"

    class Meta:
        ordering = (('file_name', 'desc'))
        # db_table = 'file_join'

    file_name = peewee.CharField(max_length=200, null=True)
    file_slug = peewee.CharField(max_length=200, null=True, unique=True)
    on_created = peewee.DateTimeField(default=NOW)

    def __str__(self):
        return "{} {}".format(self.file_name, self.file_slug)

    def save(self):
        self.file_slug = copy_file(self.DEST_FILES, self.file_slug)
        super(FileJoin, self).save()

    def display_name(self):
        return u"{}".format(self.file_name)

    @property
    def get_file(self):
        return os.path.join(
            os.path.join(os.path.dirname(os.path.abspath('__file__')),
                         self.DEST_FILES), self.file_slug)

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


class Owner(BaseModel):

    """ The web user who is also owner of the Settings
    """

    class Meta:
        ordering = (('username', 'desc'))
        # db_table = 'owner'

    USER = u"Utilisateur"
    ADMIN = u"Administrateur"
    ROOT = u"superuser"

    username = peewee.CharField(
        max_length=30, unique=True, verbose_name=("Identifiant"))
    group = peewee.CharField(default=USER)
    islog = peewee.BooleanField(default=False)
    phone = peewee.CharField(
        max_length=30, null=True, verbose_name=("Telephone"))
    password = peewee.CharField(max_length=150)
    isactive = peewee.BooleanField(default=True)
    last_login = peewee.DateTimeField(default=NOW)
    login_count = peewee.IntegerField(default=0)

    def __str__(self):
        return u"{}".format(self.username)

    def display_name(self):
        return u"{name}/{group}/{login_count}".format(
            name=self.username, group=self.group, login_count=self.login_count)

    def crypt_password(self, password):
        return hashlib.sha224(str(password).encode("utf-8")).hexdigest()

    def save(self):
        if self.islog:
            self.login_count += 1
        super(Owner, self).save()

    def is_login(self):
        return Owner.select().get(islog=True)


class Settings(BaseModel):
    """docstring for Settings"""
    PREV = 0
    CURRENT = 1
    DEFAULT = 2
    LCONFIG = ((PREV, u"Precedent"),
               (DEFAULT, u"Par defaut"),
               (CURRENT, u"Actuel"),)

    USA = "dollar"
    XOF = "xof"
    EURO = "euro"
    DEVISE = {
        USA: "$",
        XOF: "F",
        EURO: "€"
    }
    DF = "systeme"
    BL = "blue"
    DK = "dark"
    THEME = {
        DF: "Par defaut",
        DK: "Dark",
        BL: "Blue",
    }
    slug = peewee.CharField(choices=LCONFIG, default=DEFAULT)
    is_login = peewee.BooleanField(default=True)
    theme = peewee.CharField(default=1)
    devise = peewee.CharField(choices=DEVISE, default=XOF)

    def __str__(self):
        return self.display_name()

    def display_name(self):
        return u"{}/{}/{}".format(self.slug, self.is_login, self.theme)

#     @classmethod
#     def get_or_create(cls, name_orga, typ):
#         try:
#             ctct = cls.get(name_orga=name_orga, type_=typ)
#         except cls.DoesNotExist:
#             ctct = cls.create(name_orga=name_orga, type_=typ)
#         return ctct


class License(BaseModel):

    code = peewee.CharField(unique=True)
    isactivated = peewee.BooleanField(default=False)
    activation_date = peewee.DateTimeField(default=NOW)
    can_expired = peewee.BooleanField(default=True)
    expiration_date = peewee.DateTimeField(null=True)
    owner = peewee.CharField(default="USER")
    update_date = peewee.DateTimeField(default=NOW)

    def __str__(self):
        return self.code

    def check_key(self):
        return

    @property
    def is_expired(self):
        return NOW > self.expiration_date if self.expiration_date else True

    def can_use(self):
        from cstatic import CConstants
        if not self.isactivated:
            if self.can_expired:
                return CConstants.OK if not self.is_expired else CConstants.IS_EXPIRED
            else:
                return CConstants.IS_NOT_ACTIVATED
        else:
            return CConstants.OK

    def activation(self):
        self.isactivated = True
        self.can_expired = False
        self.save()

    def deactivation(self):
        self.isactivated = False
        self.save()

    def get_evaluation(self):
        self.can_expired = True
        self.expiration_date = datetime.now() + timedelta(
            days=60, milliseconds=4)
        self.save()

    def remove_activation(self):
        self.can_expired = True
        self.expiration_date = datetime.now() - timedelta(days=1)
        self.save()


class Version(BaseModel):

    DL = 'dl'
    IN = "in"
    DO = "do"

    date = peewee.DateTimeField(
        default=NOW, verbose_name="Date de Version")
    number = peewee.IntegerField(default=1, verbose_name="Numéro de Version")
    name = peewee.CharField()
    stat = peewee.CharField(default=DL)

    def __str__(self):
        return u"{}/{}".format(self.number, self.date)

    def display_name(self):
        return u"db-v{}".format(self.number)

    def update_v(self):
        self.number += 1
        self.date = NOW
        # print(self.number)
        self.save()


class History(BaseModel):

    date = peewee.DateTimeField(default=NOW)
    data = peewee.CharField()
    action = peewee.CharField()

    def __str__(self, arg):
        return "{} à {} par {}".format(date=self.date, action=self.action)
