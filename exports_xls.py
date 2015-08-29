#!usr/bin/env python
# -*- coding= UTF-8 -*-
# maintainer: Fadiga

from __future__ import (
    unicode_literals, absolute_import, division, print_function)

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
title_font = _font.format(height="250", color="blue", bold="on")
value_font = _font.format(height="250", color="black", bold="off")
label_font = _font.format(height="300", color="black", bold="on")

# styles
style_org = xlwt.easyxf(dft_pattern + label_font + int_align + _borders)
style_title = xlwt.easyxf(dft_pattern + center_align + title_font)
style_value = xlwt.easyxf(dft_pattern + value_font)
style_label = xlwt.easyxf(dft_pattern + label_font + int_align)
style_headers = xlwt.easyxf(
    _pattern.format(color="22") + label_font + _borders, center_align)


def align_style(val):
    try:
        int(val)
        return int_align
    except ValueError:
        return str_align
    else:
        return 0


def export_dynamic_data(dict_data):
    '''
        - Export params
        dict = {
            'file_name': "prod.xls",
            'data' : [1, 3, ...],
            'headers': ["ff", "kkk", "ooo"],
            'sheet': "Les produits",
            'extend_rows': [(row1, col1, val), (row2, col2, val), ]
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
    title = str(dict_data.get("title"))
    data = dict_data.get("data")
    widths = dict_data.get("widths")
    date_ = str(dict_data.get("date"))
    extend_rows = dict_data.get("extend_rows")
    others = dict_data.get("others")
    footers = dict_data.get("footers")
    print(dict_data)

    if date_ == "None":
        date_ = date.today().strftime("%A le %d/%m/%Y")

    book = xlwt.Workbook(encoding='ascii')
    sheet = book.add_sheet(sheet_name)
    sheet.fit_num_pages = 1
    for col in widths:
        w = len(headers) / len(widths)
        sheet.col(col).width = 0x0d00 * int(w)

    rowx = 0
    end_colx = len(headers) - 1
    sheet.write_merge(
        rowx, rowx + 1, 0, end_colx, Config.NAME_ORGA, style_org)
    rowx += 3
    sheet.write_merge(rowx, rowx, 0, end_colx, title, style_title)
    rowx += 2
    # sheet.write(rowx, 0, u"Date : ", style_label)
    print(rowx)
    sheet.write_merge(
        rowx, rowx, 0, end_colx, date_, style_label)
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
    if extend_rows:
        # sheet.write(rowx, extend_rows[0][0] - 1, "Totals",
        # xlwt.easyxf(pattern + value_font + align_style(val) + _borders))
        for elt in extend_rows:
            col, val = elt
            sheet.write(rowx, col, val,
                        xlwt.easyxf(pattern + value_font + align_style(val) + _borders))
        rowx += 1
    if footers:
        rowx += 2
        for elt in footers:
            mrow, col, colx, val = elt
            sheet.write_merge(rowx, rowx, col, colx, val,
                              xlwt.easyxf(pattern + value_font + align_style(val)))
        rowx += 1

    if others:
        for rowx, row, colx, col, val in others:
            nb_ch = 60
            if len(val) > nb_ch:
                sheet.write_merge(rowx, row, colx, col, val[:nb_ch],
                                  xlwt.easyxf(pattern + value_font + align_style(val)))

                sheet.write_merge(rowx + 1, row + 1, colx, col, val[nb_ch:],
                                  xlwt.easyxf(pattern + value_font + align_style(val)))
            else:
                sheet.write_merge(rowx, row, colx, col, val,
                                  xlwt.easyxf(pattern + value_font + align_style(val)))

    try:
        book.save(file_name)
        openFile(file_name)
    except Exception as e:
        print(e)


# def long_cel(val):
#     list_char = []
#     while len(val) > 20:
#         c = True
#         print(len(val))
#         list_char.append(val[:20])
#         val = val[20:]
#     list_char.append(val)
#     print(list_char, "val")
#     return list_char
