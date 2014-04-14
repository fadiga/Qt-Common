#!/usr/bin/env python
# encoding=utf-8
# Autor: Fadiga

from models import Owner, Settings, SettingsAdmin, Version

PASS = "36cb1f4ebf4298c14c96ab541a454870fa53455d5431d1afe1d0af87" #'fad 86'
PASS1 = "4b91d93da8bc69d1360c449c79edf8dc9b24b385807c8d887d389471" #'ano 86'

LICENSE = '3483f0d7f57528841134b5802d64794234a2e85f'
LICENSE = 'trial pour le demo'

def init_fuxture():

    Owner(username="root", password=PASS, group="superuser", isvisible=False, login_count=0).save()
    Owner(username="anomime", password=PASS1, group="admin", isvisible=False, login_count=0).save()
    SettingsAdmin(license=LICENSE, tolerance=30, user="Demo").save()
    Settings(slug=Settings.DEFAULT, login=True, name_orga="demo s.a.r.l",
           phone=76433890, bp="demo", email_org="demo@demo.ml",
           adress_org="").save()
    Version(number=1).save()