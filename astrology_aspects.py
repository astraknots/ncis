#!/usr/bin/python

import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

class Aspect:
    """Astrological aspects and their index, orb, degree, value"""

    BIG_THREE_ORB = 9

    def __init__(self, name, index, orb, degree, value):
      self.name = name
      self.index = index
      self.orb = orb
      self.degree = degree
      self.value = value

    def __repr__(self):
        return "<Aspect name:%s index:%s orb:%s degree:%s value:%s>" \
               % (self.name, self.index, self.orb, self.degree, self.value)

    def __str__(self):
        return "Aspect name:%s index:%s orb:%s degree:%s value:%s" \
               % (self.name, self.index, self.orb, self.degree, self.value)


def get_aspect_by_name(name):
    for anasp in THE_ASPECTS:
        #logging.debug(asign)
        #logging.debug(name)
        if anasp.name == name:
            logging.debug("Matched " + name + " to aspect:")
            logging.debug(anasp)
            return anasp


def get_aspect_orb(aspect, planet):
    """Get the orb for the given aspect, or big three orb or aspect orb whichever is greater"""
    return max(Aspect.BIG_THREE_ORB, aspect.orb) if planet.is_big_three else aspect.orb


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


conj = Aspect('CONJ', 0, 10, 0, 0)
semisextile = Aspect('SEMISEXTILE', 1, 0, 30, 30)
sextile = Aspect('SEXTILE', 2, 6, 60, 60)
square = Aspect('SQUARE', 3, 8, 90, -90)
trine = Aspect('TRINE', 4, 8, 120, 120)
quincunx = Aspect('QUINCUNX', 5, 0, 150, -150)
opposition = Aspect('OPPOSITION', 6, 10, 180, -180)


THE_ASPECTS = (conj, semisextile, sextile, square, trine, quincunx, opposition)