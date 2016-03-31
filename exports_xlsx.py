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

style_org = {'align': 'center', 'valign': 'vcenter', 'font_size': 26,
             'border': 1,  'font_color': 'blue', 'bold': True}

style_title = {"border": 1, }
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
            'date': object date
            'format_money': [col,]

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
    format_money = dict_data.get("format_money")
    # print(data)

    dict_alph = {
        1: "A",
        2: "C",
        3: "D",
        4: "E",
        5: "F",
        6: "G",
        7: "H",
        8: "I",
    }

    if date_ == "None":
        date_ = date.today()

    workbook = xlsxwriter.Workbook(
        file_name, {'default_date_format': 'dd/mm/yy'})
    worksheet = workbook.add_worksheet(sheet_name)
    worksheet.fit_num_pages = 1

    format1 = workbook.add_format(
        {'num_format': '{}'.format(Config.NUMBER_FORMAT)})
    style_def = workbook.add_format({})
    rowx = 1
    end_colx = len(headers) - 1
    if Config.ORG_LOGO:
        worksheet.insert_image('A1:B2', os.path.join(
            Config.img_media, Config.ORG_LOGO), {'x_offset': 1.5, 'y_offset': 0.5})
        rowx += 6
    else:
        worksheet.merge_range('A{}:E{}'.format(
            rowx, rowx), Config.NAME_ORGA, workbook.add_format(style_org))
        rowx += 1
        worksheet.merge_range('A{}:E{}'.format(
            rowx, rowx), "Adresse : {}".format(Config.ADRESS_ORGA), style_def)
        rowx += 1
        worksheet.merge_range('A{}:B{}'.format(
            rowx, rowx), "BP : {}".format(Config.BP), style_def)
        worksheet.merge_range('{}{}:{}{}'.format(dict_alph.get(end_colx - 1), rowx, dict_alph.get(
            end_colx), rowx), "E-mail : {}".format(Config.EMAIL_ORGA), style_def)
        rowx += 1
        worksheet.merge_range('A{}:{}{}'.format(
            rowx, dict_alph.get(end_colx - 1), rowx), "Tel : {}".format(Config.TEL_ORGA), style_def)
        rowx += 2
    for col in widths:
        w = (120 / len(headers))
        worksheet.set_column(col, col, w)
    columns = [({'header': item}) for item in headers]
    end_row_table = len(data) + rowx + 3
    if format_money:
        for col_str in format_money:
            worksheet.set_column(col_str, 18, format1)
    rowx += 1
    worksheet.merge_range(
        "D{}:{}{}".format(rowx, dict_alph.get(end_colx), rowx), date_, workbook.add_format({'align': 'right'}))
    rowx += 2
    worksheet.add_table(
        'A{}:{}{}'.format(rowx, dict_alph.get(end_colx), end_row_table),
        {'autofilter': 0, 'data': data, 'columns': columns})
    rowx = end_row_table
    # rowx += 1
    if extend_rows:
        # worksheet.write(rowx, extend_rows[0][0] - 1, "Totals",
        #                 workbook.add_format(style_label))
        for elt in extend_rows:
            col, val = elt
            worksheet.write(rowx, col, val, style_def)
        rowx += 1
    if footers:
        rowx += 2
        for s_col, e_col, val in footers:
            worksheet.merge_range('{}{}:{}{}'.format(s_col, rowx, e_col, rowx),
                                  val, workbook.add_format(style_label))
        rowx += 1
    if others:
        for pos, pos2, val in others:
            worksheet.merge_range(
                '{}:{}'.format(pos, pos2), val, workbook.add_format(style_label))
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
