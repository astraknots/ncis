#!/usr/bin/python

import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class Planet:
    """Astrological planets and their index, aspect, element, mode, degree_base and score"""

    def __init__(self, name, index, is_big_three):
      self.name = name
      self.index = index
      self.is_big_three = is_big_three

    def __repr__(self):
        return "<Planet name:%s index:%s is_big_three:%s>" \
               % (self.name, self.index, self.is_big_three)

    def __str__(self):
        return "Planet name:%s index:%s is_big_three:%s" \
               % (self.name, self.index, self.is_big_three)


sun = Planet('SUN', 0, True)
moon = Planet('MOON', 1, True)
asc = Planet('ASC', 2, True)
mercury = Planet('MERCURY', 3, False)
venus = Planet('VENUS', 4, False)
mars = Planet('MARS', 5, False)
jupiter = Planet('JUPITER', 6, False)
saturn = Planet('SATURN', 7, False)
uranus = Planet('URANUS', 8, False)
neptune = Planet('NEPTUNE', 9, False)
pluto = Planet('PLUTO', 10, False)

THE_PLANETS = (sun, moon, asc, mercury, venus, mars, jupiter, saturn, uranus, neptune, pluto)
