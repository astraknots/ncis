#!/usr/bin/python

import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

class Sign:
    """Astrological signs and their index, aspect, element, mode, degree_base and score"""

    def __init__(self, name, index, aspect, element, mode, degree_base, score):
      self.name = name
      self.index = index
      self.aspect = aspect
      self.element = element
      self.mode = mode
      self.degree_base = degree_base
      self.score = score

    def __repr__(self):
        return "<Sign name:%s index:%s aspect:%s element:%s mode:%s degree_base:%s score:%s>" \
               % (self.name, self.index, self.aspect, self.element, self.mode, self.degree_base, self.score)

    def __str__(self):
        return "Sign name:%s index:%s aspect:%s element:%s mode:%s degree_base:%s score:%s" \
               % (self.name, self.index, self.aspect, self.element, self.mode, self.degree_base, self.score)


def get_sign_by_name(name):
    for asign in THE_SIGNS:
        #logging.debug(asign)
        #logging.debug(name)
        if asign.name == name:
            logging.debug("Matched " + name + " to sign:")
            logging.debug(asign)
            return asign


def get_ordered_signs(sign_start_idx):
    '''Returns the ordered list of 12 signs, starting with the sign at sign_start_idx'''
    if sign_start_idx == 0:
        ordered_signs = THE_SIGNS
    elif sign_start_idx == 1:
        ordered_signs = list(THE_SIGNS)[1:] + [THE_SIGNS[0]]
    else:
        ordered_signs = list(THE_SIGNS[sign_start_idx:]) + list(THE_SIGNS[0:sign_start_idx])

    logging.debug(ordered_signs)
    return ordered_signs


def get_modes_for_signs(sign1, sign2):
    modes = [sign1.mode]
    if sign2.mode not in modes:
        modes.append(sign2.mode)
        ##print("modes ", modes)
        # for mode in modes:
        # print("mode score:", constants.MODE_SCORES[mode])

    return modes


def get_elements_for_signs(sign1, sign2):
    elements = [sign1.element]
    if sign2.element not in elements:
        elements.append(sign2.element)
    ##print("elements ", elements)
    #for element in elements:
       # print("element score:", constants.ELEMENT_SCORES[element])

    return elements


aries = Sign('ARIES', 0, 'TRINE', 'FIRE', 'CARDINAL', 0, 1)
taurus = Sign('TAURUS', 1, 'SQUARE', 'EARTH', 'FIXED', 30, 2)
gemini = Sign('GEMINI', 2, 'SEXTILE', 'AIR', 'MUTABLE', 60, 3)
cancer = Sign('CANCER', 3, 'SEMISEXTILE', 'WATER', 'CARDINAL', 90, 4)
leo = Sign('LEO', 4, 'CONJ', 'FIRE', 'FIXED', 120, 5)
virgo = Sign('VIRGO', 5, 'SEMISEXTILE', 'EARTH', 'MUTABLE', 150, 6)
libra = Sign('LIBRA', 6, 'SEXTILE', 'AIR', 'CARDINAL', 180, 7)
scorpio = Sign('SCORPIO', 7, 'SQUARE', 'WATER', 'FIXED', 210, 8)
sagittarius = Sign('SAGITTARIUS', 8, 'TRINE', 'FIRE', 'MUTABLE', 240, 9)
capricorn = Sign('CAPRICORN', 9, 'QUINCUNX', 'EARTH', 'CARDINAL', 270, 10)
aquarius = Sign('AQUARIUS', 10, 'OPPOSITION', 'AIR', 'FIXED', 300, 11)
pisces = Sign('PISCES', 11, 'QUINCUNX', 'WATER', 'MUTABLE', 330, 12)

THE_SIGNS = (aries, taurus, gemini, cancer, leo, virgo, libra, scorpio, sagittarius, capricorn, aquarius, pisces)
