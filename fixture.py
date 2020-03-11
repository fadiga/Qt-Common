#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Autor: Fadiga

from __future__ import (
    unicode_literals, absolute_import, division, print_function)


from Common.models import Version, Settings


class AdminFixture(object):

    LIST_CREAT = [Version(number=1), Settings()]

    def create_all_or_pass(self):

        print(u"---- Init fixture -----")

        for f in self.LIST_CREAT:
            try:
                f.save()
            except Exception as e:
                print(e)
