#!usr/bin/env python
# -*- coding= UTF-8 -*-
#maintainer: Fadiga

from __future__ import (unicode_literals, absolute_import, division, print_function)

import xlwt

from datetime import date

from Common.ui.util import openFile
from configuration import Config


_pattern = "pattern: pattern solid, fore_color {color}"
_borders = "; borders: right 1, left 1, top 1, bottom 1"
_align = "; align: horiz {horiz}, vert {vert}"
_font = "; font: name Times New Roman, height {height}, bold {bold}, color {color}"

dft_pattern = _pattern.format(color="white")
str_align = _align.format(horiz="left", vert="center")
int_align = _align.format(horiz="right", vert="center")
center_align = _align.format(horiz="center", vert="center")
dft_font = _font.format(height="250", color="black", bold="off")
title_font = _font.format(height="250", color="black", bold="off")
value_font = _font.format(height="250", color="black", bold="off")
label_font = _font.format(height="300", color="black", bold="on")

#styles
style_title = xlwt.easyxf(dft_pattern + center_align + title_font + _borders)
style_value = xlwt.easyxf(dft_pattern + value_font)
style_label = xlwt.easyxf(dft_pattern + label_font + int_align)
style_headers = xlwt.easyxf(_pattern.format(color="22") + label_font + _borders, center_align)


def align_style(val):
    try:
        int(val)
        return int_align
    except ValueError:
        return str_align


def export_dynamic_data(dict_data):
    '''
        - Export params
        dict = {
            'file_name': "prod.xls",
            'data' : [1, 3, ...],
            'headers': ["ff", "kkk", "ooo"],
            'sheet': "Les produits",
            'widths': [col, ..]
            'date': le 20 juin 2015
        }
        - Principe
        write((nbre ligne - 1), nbre colonne, "contenu", style(optionnel).
        write_merge((nbre ligne - 1), (nbre ligne - 1) + nbre de ligne à merger, (nbre de colonne - 1), (nbre de colonne - 1) + nbre
        de colonne à merger, u"contenu", style(optionnel)).
    '''

    file_name = str(dict_data.get("file_name"))
    headers = dict_data.get("headers")
    sheet_name = str(dict_data.get("sheet"))
    data = dict_data.get("data")
    widths = dict_data.get("widths")
    date_ = str(dict_data.get("date"))

    if date_ == "None":
        date_ = date.today().strftime("%A le %d/%m/%Y")

    book = xlwt.Workbook(encoding='ascii')
    sheet = book.add_sheet(sheet_name)

    for col in widths:
        w = 8 / len(widths)
        sheet.col(col).width = 0x0d00 * int(w)

    rowx = 0
    sheet.write_merge(rowx, rowx + 1, 0, 3, Config.NAME_ORGA, style_title)
    rowx += 3
    sheet.write(rowx, 0, u"Date : ", style_label)
    sheet.write_merge(rowx, rowx, 1, 3, date_, style_value)
    rowx += 2
    for colx, val_center in enumerate(headers):
        sheet.write(rowx, colx, val_center, style_headers)
    rowx += 1
    for elt in data:
        if int(rowx) % 2 == 0:
            pattern = dft_pattern
        else:
            pattern = _pattern.format(color="0x01F")
        for colx, val in enumerate(elt):
            sheet.write(rowx, colx, val,
                xlwt.easyxf(pattern + value_font + align_style(val) + _borders))
        rowx += 1

    book.save(file_name)
    openFile(file_name)
