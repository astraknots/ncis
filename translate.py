#!/usr/bin/python

import astrology_signs
import astrology_planets as planets
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def translate_chart_to_degrees_for_planets(chart):
    ''' Translate the chart to planets at degrees around 360'''
    chart_planet_degrees = {}

    for planet in planets.THE_PLANETS:
        chart_sign = chart[planet.name][0]
        chart_deg = chart[planet.name][1]
        chart_planet_degrees[planet.name] = chart_deg + astrology_signs.get_sign_by_name(chart_sign).degree_base

    logging.info("chart planet degrees:")
    logging.info(chart_planet_degrees)
    return chart_planet_degrees


def translate_chart_to_signs(chart):
    '''Translate the chart to signs at degrees around 360'''

    logging.debug("Chart to translate into signs:")
    logging.debug(chart)
    logging.debug("ASC:")
    logging.debug(chart['ASC'])

    #Mark the first row of the chart with the sign and degree of the ASC
    first_house_sign = astrology_signs.get_sign_by_name(chart['ASC'][0])
    logging.debug("first_house_sign")
    logging.debug(first_house_sign)

    asc_deg_start = chart['ASC'][1]
    logging.debug("asc_deg_start")
    logging.debug(asc_deg_start)

    # Get the list of signs starting with the first house sign
    ordered_signs = astrology_signs.get_ordered_signs(first_house_sign.index)

    return calculate_chart_signs_by_degrees(first_house_sign, asc_deg_start, ordered_signs)


def calculate_chart_signs_by_degrees(first_house_sign, asc_deg_start, ordered_signs):
    chart_signs_by_degrees = {}

    # Save the start degree to loop to later
    deg_start = asc_deg_start
    logging.debug("asc_deg_start:" + str(asc_deg_start))

    # Start at the ASC Degree with the 1st house sign, and loop over each sign adding 30 degrees to the chart_signs_by_degrees dict
    logging.debug("Start with asc sign and repeat for " + str(30 - asc_deg_start))
    d = 1
    for sign in ordered_signs:
        for ds in range(deg_start, 30):
            chart_signs_by_degrees[d] = sign
            d += 1
        deg_start = 0

    # Then loop over the rest of the degrees from ASC sign for the 12th house
    for ds in range(0, asc_deg_start):
        chart_signs_by_degrees[d] = first_house_sign
        d += 1

    logging.info("chart signs by row:")
    logging.info(chart_signs_by_degrees)
    return chart_signs_by_degrees
