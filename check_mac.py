#!/usr/bin/env python
# -*- coding: utf8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu
# maintainer: Fad
from __future__ import (
    unicode_literals, absolute_import, division, print_function)
from uuid import getnode


def get_mac():
    # The return value is the mac address as 48 bit integer.
    return getnode()
