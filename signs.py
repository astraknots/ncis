#!/usr/bin/python


import constants, shapes, astrology_signs
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

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
