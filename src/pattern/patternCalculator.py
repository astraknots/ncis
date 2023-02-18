import logging

from src.chart.chart_objects.ChartPlanet import ChartPlanet
from src.pattern.pattern_objects import StitchAction
from src.pattern.pattern_objects.Garment import Garment
from src.pattern.pattern_objects.StitchDeterminer import StitchDeterminer
from src.pattern.pattern_objects.enums import GarmentType


def get_garment_type_from_name(garment_name):
    try:
        garment_type = GarmentType.get_garment_type_by_name(garment_name)
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


def calc_scored_planet_aspect_dict(garment, astra_calc_chart):
    '''Put planets (and aspect start-end ranges) into a dict for the garment organized by garment degree incs
    Store in garment.planet_aspect_scored_dict
    format: {garment_degree: [{Planet: [Aspect, Aspect]...}, ... ]...}
    '''
    deg_inc = garment.garment_type.value
    for planet in astra_calc_chart.chart_sign_degrees_by_planet:
        p_sign_deg = astra_calc_chart.chart_sign_degrees_by_planet[planet]
        p_deg = p_sign_deg[1]
        if planet in astra_calc_chart.chart_aspects_by_planet:
            p_chart_aspect = astra_calc_chart.chart_aspects_by_planet[planet]

            logging.info(str(planet) + " " + str(p_deg.degree_360) + " " + str(p_chart_aspect))

            for g_deg in garment.planet_aspect_scored_dict:
                if g_deg <= p_deg.degree_360 < g_deg+deg_inc:
                    chart_planet = ChartPlanet(planet, p_sign_deg, astra_calc_chart.chart_dignities_by_planet[planet])
                    chart_planet_aspect_dict = {chart_planet: p_chart_aspect}
                    garment.planet_aspect_scored_dict[g_deg].append(chart_planet_aspect_dict)


def calc_pattern_from_scores(garment, astra_calc_chart):
    #garment_dict = garment.garment_dict
    #print("__________-")
    for patt_deg in garment.planet_aspect_scored_dict:
        if len(garment.planet_aspect_scored_dict[patt_deg]) > 0: # It's a list of what is at this place in the pattern

            if len(garment.planet_aspect_scored_dict[patt_deg]) > 0:
                #print("...", garment.planet_aspect_scored_dict[patt_deg])
                planet_aspect_info_dict = garment.planet_aspect_scored_dict[patt_deg][0]

                for p_info in planet_aspect_info_dict:
                    aspect_list = planet_aspect_info_dict[p_info]
                    #print("....", p_info, " contains:")
                    for an_aspect in aspect_list:

                        # Only determine pattern info for the planets involved in this garment
                        aspected_planets = an_aspect.planets_in_aspect
                        if GarmentType.is_chart_planet_for_garment_type(garment.garment_type, aspected_planets[0]) and \
                            GarmentType.is_chart_planet_for_garment_type(garment.garment_type, aspected_planets[1]):
                            #print("Provide pattern info for:", an_aspect)
                            sd = StitchDeterminer(an_aspect)
                            garment.garment_dict[patt_deg].append(sd)
            #suggest_shape()
            #get_base_x()
            #get_width_x()


def make_up_pattern():
    '''GIven some params, choose a stitch pattern'''
    for a_st in StitchAction.StitchActions:
        print(a_st)


def calc_pattern(astra_calc_chart, garment_name):
    # Create the ordered dict by garment inc degrees
    # this contains a dict of the chart's degrees by deg increments for garment
    garment_type = get_garment_type_from_name(garment_name)
    garment = Garment(garment_type)

    #First put all the planet data into a dict
    calc_scored_planet_aspect_dict(garment, astra_calc_chart) #this modifies the garment object to store the results

    # Then start building patterns based on that data
    calc_pattern_from_scores(garment, astra_calc_chart)
    print(garment)

    # TODO: make_up_pattern()

    return garment
