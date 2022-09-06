#!/usr/bin/python
import logging

import xlsxwriter

import constants
from XslxChart import XlsxChart


class AstraXslxChart(XlsxChart):
    def __init__(self, filename):
        self.filename = filename
        self.garment = None

    def set_garment(self, garment):
        self.garment = garment

    def degree_inc(self):
        return constants.GARMENT_ST_TO_DEGREES[self.garment]
