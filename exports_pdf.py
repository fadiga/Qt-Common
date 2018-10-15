#!usr/bin/env python
# -*- coding= UTF-8 -*-
# maintainer: Fadiga

from __future__ import (
    unicode_literals, absolute_import, division, print_function)


from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
# from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Spacer, Paragraph
from reportlab.platypus.tables import Table, TableStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
# from Common.cel import cel
# from num2words import num2words
from Common.ui.util import get_temp_filename, openFile
from reportlab.lib.styles import ParagraphStyle

# setup the empty canvas
# from io import FileIO as file
# from Common.pyPdf import PdfFileWriter, PdfFileReader
# from PyPDF2 import PdfFileWriter, PdfFileReader
# from datetime import datetime


def export_dynamic_data(dict_data):
    date = dict_data.get("date")
    data = dict_data.get("data")
    headers = dict_data.get("headers")
    file_name = "{}.pdf".format(dict_data.get("file_name"))
    title = str(dict_data.get("title"))

    el = []
    # htable = headers
    hdata = [(title, "", "", ""), (date, "", "", "")]
    htable = Table(hdata)
    htable.hAlign = "LEFT"

    ldata = []
    ldata.append(headers)
    # style_ = ParagraphStyle(
    #     name='Normal',
    # )

    for r in data:
        ldata.append(r)

    btable = Table(ldata)
    # btable = Table(ldata, colWidths=[(inch) for i in range(1, len(ldata) + 1)])
    # btable = Table(ldata)
    btable.hAlign = "LEFT"
    btable.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor("#C0C0C0")),
        ('GRID', (0, 1), (-1, -1), 0.01 * inch, (0, 0, 0,)),
        ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold')]))
    el.append(htable)
    el.append(btable)

    doc = SimpleDocTemplate(file_name, pagesize=A4)
    doc.build(el)
    openFile(file_name)


# def export_dynamic_data1(dict_data):
#     '''
#         - Export params
#         dict = {
#             'file_name': "prod.pdf",
#             'data' : [1, 3, ...],
#             'headers': ["ff", "kkk", "ooo"],
#             'sheet': "Les produits",
#             'extend_rows': [(row1, col1, val), (row2, col2, val), ]
#             'widths': [col, ..]
#             'date': object date
#             'format_money': ['D:D',]

#         }
#         - Principe
#         write((nbre ligne - 1), nbre colonne, "contenu", style(optionnel).
#         merge_range((nbre ligne - 1), (nbre ligne - 1) + nbre de ligne à merger, (nbre de colonne - 1), (nbre de colonne - 1) + nbre
#         de colonne à merger, u"contenu", style(optionnel)).
#     '''

#     file_name = str(dict_data.get("file_name"))
#     headers = dict_data.get("headers")
#     sheet_name = str(dict_data.get("sheet"))
#     title = str(dict_data.get("title"))
#     data = dict_data.get("data")
#     widths = dict_data.get("widths")
#     date_ = str(dict_data.get("date"))
#     extend_rows = dict_data.get("extend_rows")
#     others = dict_data.get("others")
#     footers = dict_data.get("footers")
#     exclude_row = dict_data.get("exclude_row")
#     format_money = dict_data.get("format_money")
#     # print(data)
#     if date_ == "None":
#         date_ = datetime.now()

#     """
#         cette views est cree pour la generation du PDF
#     """

#     # filename = get_temp_filename('pdf')
#     # print(filename)
#     # on recupere les items de la facture

#     # Static source pdf to be overlayed
#     PDFSOURCE = 'fact_source.pdf'
#     TMP_FILE = 'tmp.pdf'
#     DATE_FORMAT = u"%d/%m/%Y"

#     DEFAULT_FONT_SIZE = 11
#     FONT = 'Courier-Bold'
#     # A simple function to return a leading 0 on any single digit int.

#     def double_zero(value):
#         try:
#             return '%02d' % value
#         except TypeError:
#             return value

#     # PDF en entrée
#     # input1 = PdfFileReader(file(PDFSOURCE, "rb"))

#     # PDF en sortie
#     output = PdfFileWriter()
#     # Récupération du nombre de pages
#     n_pages = output.getNumPages()
#     # Pour chaque page
#     for i in range(n_pages):
#         page = output.getPage(i)

#         p = canvas.Canvas(TMP_FILE, pagesize=A4)
#         # p.setFont(FONT, DEFAULT_FONT_SIZE)

#         y = 610
#         x = 40
#         for drow in data:
#             p.drawString(x + 75, y, str(drow[0]))
#             p.drawString(x + 340, y, str(drow[1]).rjust(10, ' '))
#             p.drawString(x + 430, y, str(drow[2]).rjust(10, ' '))
#             y -= 20
#         p.drawString(130, 683, str())
#         p.save()
#         # p.drawString(98, 667, (report.client))

#         # p.drawString(460, 683, str(report.date.strftime(DATE_FORMAT)))

#         watermark = PdfFileReader(file(TMP_FILE, "rb"))
#         # Création page_initiale+watermark
#         # page.mergePage(watermark.getPage(0))
#         # Création de la nouvelle page
#         output.addPage(page)
#     # Nouveau pdf
#     file_dest = file_name
#     outputStream = file(file_dest, u"wb")
#     output.write(outputStream)
#     outputStream.close()
#     openFile(file_name)
