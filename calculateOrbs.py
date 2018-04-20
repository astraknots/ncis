#!/usr/bin/python

import aspects
import constants
import astrology_planets as planets
import astrology_aspects as asp
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def calc_orbs_of_influence(chart_degrees, sign_degree_dict):
    ''' Calculate Orbs of Influence'''
    orbs_by_planet = calc_orbs_by_planet(chart_degrees)

    degree_dict = {}
    # Degrees = {0 : [Aspect], 1 : [Aspect, Aspect] .... }
    for d in range(1, 361):
        logging.debug("sign_degree_dict[d], d:" + str(d))
        logging.debug(sign_degree_dict[d])
        degree_dict[d] = aspects.get_aspects_for_degree(orbs_by_planet, d, sign_degree_dict[d])

    logging.debug("degree_dict:")
    logging.debug(degree_dict)
    return degree_dict


def calc_orbs_by_planet(chart_degrees):
    """"Calculate orbs of influence by planet over the chart degrees"""
    orbs_by_planet = {}
    # {Planet = {Aspect : [Deg,Deg], Aspect : [Deg, Deg]}}

    for planet in planets.THE_PLANETS:
        deg = chart_degrees[planet.name]
        for aspect in asp.THE_ASPECTS:
            asp_orb = asp.get_aspect_orb(aspect, planet)
            asp_deg = aspect.degree
            range0 = deg + asp_deg - asp_orb
            range1 = deg + asp_deg + asp_orb
            if planet.name in orbs_by_planet:
                planet_dict = orbs_by_planet[planet.name]
            else:
                planet_dict = {}
            planet_dict[aspect.name] = [asp.adjust_degree_for_360(range0), asp.adjust_degree_for_360(range1)]
            orbs_by_planet[planet.name] = planet_dict

    logging.debug("orb degree dict by planet:")
    logging.debug(orbs_by_planet)

    return orbs_by_planet


