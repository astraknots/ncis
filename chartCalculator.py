import getopt
import logging
import sys

import Planet
import Sign
import chartData
import AspectType
from ChartAspect import ChartAspect
from AstraChart import AstraChart
from AstraChartCalc import AstraChartCalc
from ChartDegree import ChartDegree
from Garment import Garment, GarmentType
from AspectType import AspectDirection, AspectName


def create_chart_dict(raw_chart_data):
    '''Take in the raw chart data in strings, translate to our objects, return a dict'''
    chart_dict = {}
    for entry in raw_chart_data:
        logging.debug(str(entry) + " " + str(raw_chart_data[entry]))

        planet = Planet.get_planet_by_name(entry)
        sign_degree_raw = raw_chart_data[entry]
        sign = Sign.get_sign_by_name(sign_degree_raw[0])

        logging.debug(str(sign))

        chart_degree = ChartDegree(sign, sign_degree_raw[1])
        ChartDegree.calculate_and_set_360_degree_from_sign_degree(chart_degree, sign.name)

        logging.debug(str(chart_degree))

        chart_dict[planet] = [sign, chart_degree]
    return chart_dict


def calc_aspect_orbs(chart_dict):
    orbs_by_planet = {}
    # {Planet = {Aspect : [Deg,Deg], Aspect : [Deg, Deg]}}

    print("chart_dict:", chart_dict)
    for planet in chart_dict:
        sign_degree_data = chart_dict[planet]
        chart_degree = sign_degree_data[1]
        for aspect in AspectType.AspectTypes:
            asp_orb = aspect.orb
            asp_deg = aspect.degree
            deg = chart_degree.degree_360
            range0 = deg + asp_deg - asp_orb
            range1 = deg + asp_deg + asp_orb
            if planet in orbs_by_planet:
                planet_dict = orbs_by_planet[planet]
            else:
                planet_dict = {}
            planet_dict[aspect] = [AspectType.adjust_deg_for_360(range0), AspectType.adjust_deg_for_360(range1)]
            orbs_by_planet[planet] = planet_dict

    logging.info("orb degree dict by planet (aspect_orbs):")
    logging.info(orbs_by_planet)

    return orbs_by_planet


def get_faster_planet_difference(planet1, planet2, planet1_deg, planet2_deg):
    # TODO: Assert that the speeds are never the same, because they should be different
    if planet1.speed > planet2.speed: # planet1 is faster
        return planet1_deg - planet2_deg
    else:
        return planet2_deg - planet1_deg


def determine_aspect_direction(deg_diff, calc_chart_diff):
    #TODO: decide if this should determine an exact aspect or throw a message
    if (deg_diff < 0 < calc_chart_diff) or (deg_diff > 0 > calc_chart_diff):
        return AspectDirection.APPLYING
    elif (deg_diff > 0 and calc_chart_diff > 0) or (deg_diff < 0 and calc_chart_diff < 0):
        return AspectDirection.SEPARATING


def calc_planet_aspects(chart_dict, aspect_orbs):
    aspects_by_planet = {}

    #Loop over the planets in the chart, then loop over every other planet and capture aspects and details

    for planet in chart_dict:
        planet_name = planet.name
        planet_speed = planet.speed
        chart_sign_deg = chart_dict[planet] # The planet's sign & degree in a list

        planet_chart_deg = chart_sign_deg[1].degree_360 # The planet's 360 degree degree
        print("chart_deg:", planet_chart_deg)

        planet_aspects = aspect_orbs[planet]

        for asp_planet in chart_dict:
            # Loop over the chart planets looking for aspects to other planets
            if asp_planet.name != planet_name:  # don't look for aspects to self
                asp_planet_speed = asp_planet.speed
                asp_planet_chart_deg = chart_dict[asp_planet][1].degree_360
                deg_diff = get_faster_planet_difference(planet, asp_planet, planet_chart_deg, asp_planet_chart_deg)

                # Loop over and calculate aspects
                for aspect in planet_aspects:
                    aspect_start_range = aspect.degree + aspect.orb
                    aspect_end_range = aspect.degree - aspect.orb

                    #print(aspect_start_range, " - ", aspect_end_range)

                    # Calculate the diff and direction of the aspect if found, add to list
                    p_aspect = None
                    calc_chart_diff = abs(deg_diff) - aspect.degree
                    if aspect_end_range <= deg_diff <= aspect_start_range: # There is an aspect here
                        if deg_diff == aspect.degree:  # the aspect is exact
                            p_aspect = ChartAspect(aspect.name, AspectDirection.EXACT, calc_chart_diff, [planet, asp_planet])
                        else:
                            a_direction = determine_aspect_direction(deg_diff, calc_chart_diff)

                            p_aspect = ChartAspect(aspect.name, a_direction, calc_chart_diff, [planet, asp_planet])
                            if planet not in aspects_by_planet:
                                aspects_by_planet[planet] = []
                            aspects_by_planet[planet].append(p_aspect)
                            print(aspects_by_planet[planet])

    return aspects_by_planet


def calc_garment_dict(garment, chart_dict, aspect_orbs):
    '''Put planets (and aspect start-end ranges) into a dict for the garment organized by garment degree incs'''
    return None


def calc_chart_info(a_chart, garment_type):
    '''Calculate all of the chart data that we'll want to use for patterns and printing'''
    # Start by taking in the chart data, and putting the Planet and Sign objects in
    raw_chart_data = a_chart.chart_data  # May look like:  { 'SUN' : ['VIRGO',8], 'MOON' : ['SCORPIO', 2], ....
    astra_calc_chart = AstraChartCalc(raw_chart_data)  # we'll populate with our converted output

    chart_dict = create_chart_dict(raw_chart_data)
    astra_calc_chart.planet_sign_degrees = chart_dict

    # Calculate the Aspect orbs and store that
    aspect_orbs = calc_aspect_orbs(chart_dict)
    astra_calc_chart.aspect_orbs = aspect_orbs

    # Calculate the actual aspects of the chart
    planet_aspects = calc_planet_aspects(chart_dict, aspect_orbs)
    astra_calc_chart.planet_aspects = planet_aspects

    # Create the ordered dict by garment inc degrees
    # this contains a dict of the chart's degrees by deg increments for garment
    garment = Garment(garment_type)
    print(garment.garment_dict)
    #TODO calc the garment dict organized
    calc_garment_dict(garment, chart_dict, aspect_orbs)

    return astra_calc_chart


def create_astra_chart(chart_name, person_name, raw_astra_data):
    '''Create an instance of the AstraChart class with basic info'''
    a_chart = AstraChart(chart_name, person_name, raw_astra_data)
    return a_chart


def calc_chart(argv):
    chartname = ''
    pattname = 'SCARF'
    try:
        opts, args = getopt.getopt(argv, "hc:p:b:", ["chart=", "patt="])
    except getopt.GetoptError:
        print('chartCalculator.py -c <chart-name> -p <pattern-style>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('chartCalculator.py -c <chart-name> -p <pattern-style>')
            sys.exit()
        elif opt in ("-c", "--chart"):
            chartname = arg
        elif opt in ("-p", "--patt"):
            pattname = arg.upper()
        elif opt in "-b":
            chartname = ''

    if chartname == '':
        logging.info("Creating blank astra chart")
        blank_chart = create_astra_chart("Blank Chart", 'None', None)
        calc_chart_info(blank_chart, GarmentType.HAT)
        # write_any_astra_chart_to_xcel("blank chart", 'HAT', "blank", None)
    else:
        logging.info("Chart argument given:" + chartname)

        if chartname == 'gchart':
            usechart = create_astra_chart(chartname, 'Genevieve', chartData.gchart)
        elif chartname == 'bchart':
            usechart = create_astra_chart(chartname, 'Brian', chartData.bchart)
        elif chartname == 'jchart':
            usechart = create_astra_chart(chartname, 'Jacob', chartData.jchart)
        elif chartname == 'rchart':
            usechart = create_astra_chart(chartname, 'Rebecca', chartData.rchart)
        else:
            findchart = chartData.get_chart(chartname)
            if findchart is None:
                print('Couldn\'t find the chart you are looking for..')
                return
            else:
                usechart = create_astra_chart(chartname, chartData.get_chart_person(chartname), findchart)

        logging.info(usechart)
        try:
            garment = GarmentType[pattname]
        except KeyError:
            garment = GarmentType.HAT

        chart_info = calc_chart_info(usechart, garment)
        print()
        print(" Here's the calculated chart info: ")
        print(chart_info)
        # write_any_astra_chart_to_xcel(chartname, pattname, usechart.person, usechart)


if __name__ == "__main__":
    calc_chart(sys.argv[1:])
