import logging

from enums import Garment
from src.chart_objects.ChartPlanet import ChartPlanet
from src.pattern.enums.GarmentType import GarmentType


def get_garment_type_from_name(garment_name):
    try:
        garment_type = GarmentType[garment_name]
    except KeyError:
        #default to HAT
        garment_type = GarmentType.HAT
    return garment_type


def get_planet_sign_dignity_for_planet(astra_calc_chart, planet):
    p_dig_list = astra_calc_chart.chart_dignities_by_planet[planet]
    planet_sign_dignity = None
    if len(p_dig_list) > 0:
        planet_sign_dignity = p_dig_list[0]
    return planet_sign_dignity


def calc_garment_dict(garment, astra_calc_chart):
    '''Put planets (and aspect start-end ranges) into a dict for the garment organized by garment degree incs'''
    deg_inc = garment.garment_type.value
    for planet in astra_calc_chart.chart_sign_degrees_by_planet:
        p_sign_deg = astra_calc_chart.chart_sign_degrees_by_planet[planet]
        p_deg = p_sign_deg[1]
        p_aspect = astra_calc_chart.chart_aspects_by_planet[planet]
        logging.info(str(planet) + " " + str(p_deg.degree_360) + " " + str(p_aspect))
        for g_deg in garment.garment_dict:
            if g_deg <= p_deg.degree_360 < g_deg+deg_inc:
                chart_planet = ChartPlanet(planet, p_sign_deg, get_planet_sign_dignity_for_planet(astra_calc_chart, planet))
                planet_aspect_dict = {chart_planet: p_aspect}
                garment.garment_dict[g_deg].append(planet_aspect_dict)


def calc_pattern(astra_calc_chart, garment_type):
    # Create the ordered dict by garment inc degrees
    # this contains a dict of the chart's degrees by deg increments for garment
    garment = Garment(garment_type)
    calc_garment_dict(garment, astra_calc_chart)
    print(garment)
