#!/usr/bin/python

import sys, getopt
#import xlsxwriter
import constants, signs
from itertools import groupby
from collections import Counter
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def translateChartToDegreesForPlanets(chart):
    ''' Translate the chart to planets at degrees around 360'''
    chart_degrees = {}

    for planet in constants.PLANETS:
        chart_sign = chart[planet][0]
        chart_deg = chart[planet][1]
        chart_degrees[planet] = chart_deg + constants.SIGNS_DEGREE_BASE[chart_sign]

    logging.info("chart degrees:")
    logging.info(chart_degrees)
    return chart_degrees

def translateChartToSigns(chart):
    '''Translate the chart to signs at degrees around 360'''
    chart_signs = {}

    logging.debug("Chart to translate into signs:")
    logging.debug(chart)
    logging.debug("ASC:")
    logging.debug(chart['ASC'])
    #Mark the first row of the chart with the sign of the ASC
    first_house_sign = chart['ASC'][0]
    deg_start = chart['ASC'][1]

    sign_start_idx = signs.getHouseSignIdx(first_house_sign)

    ordered_signs = signs.getOrderedSigns(sign_start_idx)

    logging.debug("sign_start_idx" + str(sign_start_idx) + constants.SIGNS[sign_start_idx])

    logging.debug("first_house_sign" + first_house_sign)
    chart_signs[1] = first_house_sign

    logging.debug("deg start" + str(deg_start) + "repeat for " + str(30 - deg_start))
    #print(constants.SIGNS[first_house_sign])

    d = 1
    for sign in ordered_signs:
        for ds in range(deg_start, 30):
            chart_signs[d] = sign
            d = d+1
        deg_start = 0

    for ds in range(0, chart['ASC'][1]):
        chart_signs[d] = first_house_sign
        d = d+1

    logging.info("chart signs by row:")
    logging.info(chart_signs)
    return chart_signs

