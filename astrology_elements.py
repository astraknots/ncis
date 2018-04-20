#!/usr/bin/python

import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class Element:
    """Astrological elements and their index, scores"""

    def __init__(self, name, index, scores):
        self.name = name
        self.index = index
        self.scores = scores

    def __repr__(self):
        return "<Element name:%s index:%s scores:%s>" \
               % (self.name, self.index, self.scores)

    def __str__(self):
        return "Element name:%s index:%s scores:%s" \
               % (self.name, self.index, self.scores)


def get_element_by_name(name):
    for _element in THE_ELEMENTS:
        #logging.debug(asign)
        #logging.debug(name)
        if _element.name == name:
            logging.debug("Matched " + name + " to element:")
            logging.debug(_element)
            return _element

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


earth = Element('EARTH', 0, (2,6,10))
air = Element('AIR', 1, (3,7,11))
fire = Element('FIRE', 2, (1,5,9))
water = Element('WATER', 2, (4,8,12))


THE_ELEMENTS = (earth, air, fire, water)