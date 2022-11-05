#!/usr/bin/python
import logging

import xlsxwriter

import constants

class XlsxChart:
    def __init__(self, filename):
        self.worksheet = None
        self.workbook = None
        self.filename = filename
        self.row_cnt = 0

    def create_chart_booksheet(self, sheet_name):
        ''' Create an new Excel file and add a worksheet.'''
        self.workbook = xlsxwriter.Workbook(self.filename + '.xlsx')

        # Add blank chart worksheet
        self.worksheet = self.workbook.add_worksheet(sheet_name)

    def set_col_width(self, col_start, col_end, col_width):
        self.worksheet.set_column(col_start, col_end, col_width)

    def write_to_sheet(self, row, col, args):
        self.worksheet.write(row, col, args)

    def write_to_sheet_format(self, row, col, args, wformat):
        self.worksheet.write(row, col, args, wformat)

    def set_row_cnt(self, row_cnt):
        self.row_cnt = row_cnt

    def get_bold_format(self):
        bold_format = self.workbook.add_format({'bold': True})
        return bold_format

    def close_book(self):
        self.workbook.close()
