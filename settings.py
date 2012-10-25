# -*- encoding: utf-8 -*-
import os

rel = lambda *x: os.path.abspath(os.path.join(os.path.dirname(__file__), *x))
# Final image resolution in dpi
RESOLUTION = 300
# Inch to cm conversion constant
INCH = 2.54
# Size of the QR code image in centimeters
SIDE = 7
# Number of QR-codes per-page
PER_PAGE = 6
# LOGO = rel("logos/Bee_Orange.png")

VERSIONS = [
    {'LOGO': rel("logos/my1.png"),
     'QR_HEAD_TEXT': u'Aktionscode',
     'FIRST_COLOR': "#008483",
     'SECOND_COLOR': "#f18d05",
     'HEADER': u"STORYTAIL GMBH - FALKENRIED-PIAZZA - HOHELUFTCHAUSSEE 18"
                " - 20253 HAMBURG",
     'HEADER_COLOR': "#000000"},
    {'LOGO': rel("logos/my1.png"),
     'QR_HEAD_TEXT': u'Einlösecode',
     'FIRST_COLOR': "#616161",
     'SECOND_COLOR': "#e54028",
     'HEADER': u"STORYTAIL GMBH - FALKENRIED-PIAZZA - HOHELUFTCHAUSSEE 18"
                " - 20253 HAMBURG",
     'HEADER_COLOR': "#000000"}
]

HEADER_FONT = rel("fonts/folder_rg.ttf")
TEXT_FONT = rel("fonts/folder_rg.ttf")
OUTPUT_DIR = "codes"

DEFAULT_URL = 'http://mediasapiens.co'
QR_FONT_SIZE = 14
