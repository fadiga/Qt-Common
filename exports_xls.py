#!usr/bin/env python
# -*- coding= UTF-8 -*-
#maintainer: Fadiga

from __future__ import (unicode_literals, absolute_import, division, print_function)

import xlwt

from datetime import date

from Common.ui.util import openFile
from configuration import Config

font_title = xlwt.Font()
font_title.name = 'Times New Roman'
font_title.bold = True
font_title.height = 19 * 0x14
font_title.underline = xlwt.Font.UNDERLINE_DOUBLE

borders = xlwt.Borders()
borders.left = 1
borders.right = 1
borders.top = 1
borders.bottom = 1

al_center = xlwt.Alignment()
al_center.horz = xlwt.Alignment.HORZ_CENTER
al_center.vert = xlwt.Alignment.VERT_CENTER

al_right = xlwt.Alignment()
al_right.horz = xlwt.Alignment.HORZ_RIGHT

color = xlwt.Pattern()
color.pattern = xlwt.Pattern.SOLID_PATTERN
color.pattern_fore_colour = 22

pat2 = xlwt.Pattern()
pat2.pattern = xlwt.Pattern.SOLID_PATTERN
pat2.pattern_fore_colour = 0x01F

#styles
style_title = xlwt.easyxf('font: name Cooper Black, height 250, bold on,'
                          'color blue')
style_title.alignment = al_center

style_ = xlwt.easyxf('font: name Centaur, height 250, bold on, color black')
style_.alignment = al_center

style_t_table = xlwt.easyxf('font: name Times New Roman, height 250, bold on')
style_t_table.pattern = color
style_t_table.alignment = al_center
style_t_table.borders = borders

style2 = xlwt.easyxf('font: name Times New Roman, height 250, bold on')
style2.borders = borders

style1 = xlwt.easyxf('font: name Times New Roman, height 250, bold on')
style1.pattern = pat2
style1.borders = borders

style = xlwt.easyxf('font: name Times New Roman, height 250, bold off')
style.borders = borders

style_mag = xlwt.easyxf('font: name Times New Roman, height 250, bold on')
style_mag.alignment = al_center
style_mag.borders = borders
style_mag.pattern = color

int_style = xlwt.easyxf('font: name Times New Roman, height 250, bold off')
int_style.borders = borders
int_style.alignment = al_right

style_code = xlwt.easyxf('font: name Times New Roman, height 250, bold off, color blue')
style_code.borders = borders


def export_dynamic_data(file_name, dict_data):

    ''' Export params
    dict = {
        'file_name': "prod.xls",
        'data' : [1, 3, ...],
        'headers': ["ff", "kkk", "ooo"],
        'sheet': "Les produits",
        'widths': [col, ..]
    } '''

    # file_name = str(dict_data.get("file_name"))
    file_name = file_name
    # type(file_name)
    # print(file_name)
    headers = dict_data.get("headers")
    sheet_name = dict_data.get("sheet")
    data = dict_data.get("data")
    widths = dict_data.get("widths")

    # Principe
    # write((nbre ligne - 1), nbre colonne, "contenu", style(optionnel).
    # write_merge((nbre ligne - 1), (nbre ligne - 1) + nbre de ligne
    # à merger, (nbre de colonne - 1), (nbre de colonne - 1) + nbre
    # de colonne à merger, u"contenu", style(optionnel)).
    book = xlwt.Workbook(encoding='ascii')
    sheet = book.add_sheet(sheet_name)

    for col in widths:
        w = 8/len(widths)
        sheet.col(col).width = 0x0d00 * int(w)

    rowx = 0
    sheet.write_merge(rowx, rowx + 1, 0, 3,
                      u"Rapports de gestion de stock %s" % Config.NAME_ORGA, style_title)
    rowx += 3
    sheet.write_merge(rowx, rowx, 1, 2, u"Date du rapport: ", style)

    rowx += 1
    for colx, val_center in enumerate(headers):
        sheet.write(rowx, colx, val_center, style_t_table)
    rowx += 1
    for elt in data:
        if int(rowx) % 2 == 0:
            style_row_table = style1
        else:
            style_row_table = style2
        for colx, val in enumerate(elt):
            sheet.write(rowx, colx, val, style_row_table)
        rowx += 1

    book.save(file_name)
    openFile(file_name)
