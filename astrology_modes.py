#!/usr/bin/python

import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class Mode:
    """Astrological modes and their index, scores"""

    def __init__(self, name, index, scores):
        self.name = name
        self.index = index
        self.scores = scores

    def __repr__(self):
        return "<Mode name:%s index:%s scores:%s>" \
               % (self.name, self.index, self.scores)

    def __str__(self):
        return "Mode name:%s index:%s scores:%s" \
               % (self.name, self.index, self.scores)


def get_mode_by_name(name):
    for amode in THE_MODES:
        #logging.debug(asign)
        #logging.debug(name)
        if amode.name == name:
            logging.debug("Matched " + name + " to mode:")
            logging.debug(amode)
            return amode

#def get_aspect_orb(aspect, planet):
#    """Get the orb for the given aspect, or big three orb or aspect orb whichever is greater"""
#    return max(Aspect.BIG_THREE_ORB, aspect.orb) if planet.is_big_three else aspect.orb


def adjust_degree_for_360(degree):
    """Adjust the given degree to be within 360"""
    adj_degree = degree
    if degree > 360:
        adj_degree = degree - 360
    elif degree < 0:
        adj_degree = degree + 360
    return adj_degree


def is_degree_in_range(deg, rang):
    return rang[0] <= deg <= rang[1]


cardinal = Mode('CARDINAL', 0, (1,10,7,4))
fixed = Mode('FIXED', 1, (5,2,11,8))
mutable = Mode('MUTABLE', 2, (9,6,3,12))


THE_MODES = (cardinal, fixed, mutable)