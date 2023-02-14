#!/usr/bin/python

import constants
from src.xlsx_spreadsheet.XslxChart import XlsxChart


class AstraXslxChart(XlsxChart):
    def __init__(self, filename):
        self.filename = filename
        self.garment = None

    def set_garment(self, garment):
        self.garment = garment

    def degree_inc(self):
        return constants.GARMENT_ST_TO_DEGREES[self.garment]

    def get_cell_color_format(self, color_name):
        cell_format = self.workbook.add_format()
        cell_format.set_pattern(1)
        cell_format.set_bg_color(color_name)
        return cell_format

