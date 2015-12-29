#!usr/bin/env python
# -*- coding= UTF-8 -*-
# maintainer: Fadiga

from __future__ import (
    unicode_literals, absolute_import, division, print_function)

import xlsxwriter
import os

from datetime import date

from Common.ui.util import openFile
from configuration import Config


# _pattern = "pattern: pattern solid, fore_color {color}"
# _borders = "; borders: right 1, left 1, top 1, bottom 1"
# _align = "; align: horiz {horiz}, vert {vert}"
# _font = "; font: name Times New Roman, height {height}, bold {bold},
# color {color}"

# dft_pattern = _pattern.format(color="white")
# str_align = _align.format(horiz="left", vert="center")
# int_align = _align.format(horiz="right", vert="center")
# center_align = _align.format(horiz="center", vert="center")
# dft_font = _font.format(height="250", color="black", bold="off")
# title_font = _font.format(height="250", color="blue", bold="on")
# value_font = _font.format(height="250", color="black", bold="off")
# label_font = _font.format(height="300", color="black", bold="on")

# styles
# style_org = xlsxwriter.easyxf(dft_pattern + label_font + int_align + _borders)
# style_title = xlsxwriter.easyxf(dft_pattern + center_align + title_font)
# style_value = xlsxwriter.easyxf(dft_pattern + value_font)
# style_label = xlsxwriter.easyxf(dft_pattern + label_font + int_align)
# style_headers = xlsxwriter.easyxf(
#     _pattern.format(color="22") + label_font + _borders, center_align)
style_org = {'align': 'center', 'valign': 'vcenter', 'border': 1}

style_title = {"border": 1}
style_value = {"border": 1}
style_label = {"border": 1}
style_headers = {"border": 1}


def align_style(val):
    try:
        int(val)
        return int_align
    except ValueError:
        return str_align
    except TypeError:
        return "ERROR"
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
        merge_range((nbre ligne - 1), (nbre ligne - 1) + nbre de ligne à merger, (nbre de colonne - 1), (nbre de colonne - 1) + nbre
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
    exclude_row = dict_data.get("exclude_row")

    dict_alph = {
        1: "A",
        2: "C",
        3: "D",
        4: "E",
        5: "F",
        6: "G",
        7: "H"
    }

    if date_ == "None":
        date_ = date.today().strftime("%A le %d/%m/%Y")

    workbook = xlsxwriter.Workbook(file_name)
    worksheet = workbook.add_worksheet(sheet_name)
    worksheet.fit_num_pages = 1

    worksheet.insert_image('A1:B2', os.path.join(
        Config.img_media, 'org_logo.png'), {'x_offset': 1.5, 'y_offset': 0.5})
    for col in widths:
        w = (120 / len(headers))
        worksheet.set_column(col, col, w)

    end_colx = len(headers) - 1
    rowx = 6
    worksheet.merge_range(
        "A{}:E{}".format(rowx, rowx), title, workbook.add_format({'align': 'center'}))
    rowx += 4
    columns = [({'header': item}) for item in headers]
    # data = [item[:-1] for item in data]
    # worksheet.merge_range(
    # rowx, rowx + 1, 0, end_colx, Config.NAME_ORGA,
    # workbook.add_format(style_org))
    rowx += 1
    worksheet.merge_range(
        "B{}:{}9".format(9, dict_alph.get(end_colx)), date_, workbook.add_format({'align': 'right'}))
    rowx += 1
    # worksheet.set_column('A:D', 10)
    worksheet.add_table(
        'A{}:{}10'.format(len(data) + rowx, dict_alph.get(end_colx)), {'data': data, 'columns': columns})
    # rowx += 2
    # for colx, val_center in enumerate(headers):
    #     worksheet.write(
    #         rowx, colx, val_center, workbook.add_format(style_headers))
    # rowx += 1

    # pattern = dft_pattern
    # for elt in data:
    #     if exclude_row:
    #         elt = elt[:-1]
    #     if int(rowx) % 2 != 0:
    #         pattern = _pattern.format(color="67")
    #     for colx, val in enumerate(elt):
    # if not isinstance(val, int) or not isinstance(val, str):
    # continue
    #         worksheet.write(rowx, colx, val, workbook.add_format(style_label))
    #     rowx += 1
    rowx += len(data)
    if extend_rows:
        worksheet.write(rowx, extend_rows[0][0] - 1, "Totals",
                        workbook.add_format(style_label))
        for elt in extend_rows:
            col, val = elt
            worksheet.write(rowx, col, val, workbook.add_format(style_label))
        rowx += 1
    # if footers:
    #     rowx += 2
    #     for elt in footers:
    #         mrow, col, colx, val = elt
    #         worksheet.merge_range('{}{}:{}{}'.format(dict_alph.get(
    #             rowx), rowx, dict_alph.get(col), colx), val, workbook.add_format(style_label))
    #     rowx += 1

    if others:
        for rowx, row, colx, col, val in others:
            nb_ch = 60
            print(rowx, row, colx, col)
            # if len(val) > nb_ch:
            #     worksheet.merge_range(
            #         'A{}:{}{}'.format(row, dict_alph.get(colx), col),
            #         val[:nb_ch], workbook.add_format(style_label))
            #     worksheet.merge_range(
            #     rowx + 1, row + 1, colx, col, val[nb_ch:],
            #     workbook.add_format(style_label))
            # else:
            #     worksheet.merge_range(
            # rowx, row, colx, col, val, workbook.add_format(style_label))

    try:
        workbook.close()
        # workbook.save(file_name)
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
