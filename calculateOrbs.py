#!/usr/bin/python

import sys, getopt
import aspects
#import xlsxwriter
import constants
from itertools import groupby
from collections import Counter


def calcOrbsOfInfluence(chart_degrees, sign_degree_dict):
    ''' Calculate Orbs of Influence'''
    orbs_by_planet = calcOrbsByPlanet(chart_degrees)

    degree_dict = {}
    # Degrees = {0 : [Aspect], 1 : [Aspect, Aspect] .... }
    for d in range(1, 361):
        degree_dict[d] = aspects.getAspectsForDegree(orbs_by_planet, d, sign_degree_dict[d])

    return degree_dict


def calcOrbsByPlanet(chart_degrees):
    orbs_by_planet = {}
    # {Planet = {Aspect : [Deg,Deg], Aspect : [Deg, Deg]}}

    for planet in constants.PLANETS:
        deg = chart_degrees[planet]
        for aspect in constants.ASPECTS:
            asp_orb = aspects.getAspectOrb(aspect, planet)
            asp_deg = constants.ASPECT_DEGREES[aspect]
            range0 = deg + asp_deg - asp_orb
            range1 = deg + asp_deg + asp_orb
            if planet in orbs_by_planet:
                planet_dict = orbs_by_planet[planet]
            else:
                planet_dict = {}
            planet_dict[aspect] = [aspects.adjustDegFor360(range0), aspects.adjustDegFor360(range1)]
            orbs_by_planet[planet] = planet_dict

    print("orb degree dict by planet:", orbs_by_planet)

    return orbs_by_planet


