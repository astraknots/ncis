#!/usr/bin/python

import sys, getopt
#import xlsxwriter
import constants, shapes
from itertools import groupby
from collections import Counter
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def getOrderedSigns(sign_start_idx):
    ordered_signs = []
    for x in range(sign_start_idx, sign_start_idx + 12):
        sign_idx = x if x <= 11 else x - 12
        ordered_signs.append(constants.SIGNS[sign_idx])

    logging.debug(ordered_signs)
    return ordered_signs


def getHouseSignIdx(house_sign):
    '''Get the index of the sign from the signs list which is zero indexed. Raise exception if sign not valid'''
    if house_sign not in constants.SIGNS:
        raise ValueError("Sign: " + house_sign + " not found in constants.SIGNS")

    return constants.SIGNS.index(house_sign)
    

def determineBestPatternsForSignMatch(possPatterns, rowNum, sign_degree_dict):
    bestPatterns = ''
    if sign_degree_dict[rowNum] in constants.SIGN_ASPECT:
        assignAspect = constants.SIGN_ASPECT[sign_degree_dict[rowNum]]

        aspectShapes = constants.PATTERN_ASPECT_SHAPES[assignAspect]
        logging.debug("assign aspect:" + assignAspect + " shapes:")
        logging.debug(aspectShapes)

        bestPatterns = shapes.determineBestPatternsForShapeMatch(possPatterns, [assignAspect])
        logging.debug("best patterns in sign match:")
        logging.debug(bestPatterns)
    return bestPatterns
