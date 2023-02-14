import getopt
import logging
import sys

import chartData
from src.chart_objects import AspectType, Planet, PlanetDignity, Sign
from src.chart_objects.ChartAspect import ChartAspect
from src.chart_objects.AstraChart import AstraChart
from src.chart_objects.AstraChartCalc import AstraChartCalc
from src.chart_objects.ChartDegree import ChartDegree
from src.chart_objects.ChartPlanet import ChartPlanet
from src.pattern.Garment import Garment, GarmentType
from src.chart_objects.AspectType import AspectDirection


def create_chart_planet_deg_dict(raw_chart_data):
    '''Take in the raw chart data in strings, translate to our objects, return a dict'''
    # TODO: Generalize this to build off an existing AstraChartCalc
    chart_sign_degrees_by_planet = {}
    for entry in raw_chart_data:
        logging.debug(str(entry) + " " + str(raw_chart_data[entry]))

        planet = Planet.get_planet_by_name(entry)
        logging.debug(str(planet))

        sign_degree_raw = raw_chart_data[entry]
        sign = Sign.get_sign_by_name(sign_degree_raw[0])

        logging.debug(str(sign))

        chart_degree = ChartDegree(sign, sign_degree_raw[1])
        ChartDegree.calculate_and_set_360_degree_from_sign_degree(chart_degree, sign.name)

        logging.debug(str(chart_degree))

        chart_sign_degrees_by_planet[planet] = [sign, chart_degree]
    return chart_sign_degrees_by_planet


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
    elif deg_diff == 0:
        return AspectDirection.EXACT


def calc_planet_aspects(chart_sign_degrees_by_planet, aspect_orbs):
    aspects_by_planet = {}

    #Loop over the planets in the chart, then loop over every other planet and capture aspects and details

    for planet in chart_sign_degrees_by_planet:
        planet_name = planet.name
        planet_speed = planet.speed
        chart_sign_deg = chart_sign_degrees_by_planet[planet] # The planet's sign & degree in a list

        planet_chart_deg = chart_sign_deg[1].degree_360 # The planet's 360 degree degree
        logging.info("Calculating aspects for planet at chart_deg:" + str(planet_chart_deg))

        planet_aspects = aspect_orbs[planet]

        for asp_planet in chart_sign_degrees_by_planet:
            # Loop over the chart planets looking for aspects to other planets
            if asp_planet.name != planet_name:  # don't look for aspects to self
                asp_planet_chart_deg = chart_sign_degrees_by_planet[asp_planet][1].degree_360
                deg_diff = get_faster_planet_difference(planet, asp_planet, planet_chart_deg, asp_planet_chart_deg)

                # Loop over and calculate aspects
                for aspect in planet_aspects:
                    aspect_start_range = aspect.degree + aspect.orb
                    aspect_end_range = aspect.degree - aspect.orb

                    # Calculate the diff and direction of the aspect if found, add to list
                    p_aspect = None
                    calc_chart_diff = abs(deg_diff) - aspect.degree
                    if aspect_end_range <= deg_diff <= aspect_start_range: # There is an aspect here
                        if deg_diff == aspect.degree:  # the aspect is exact
                            p_aspect = ChartAspect(aspect.name, AspectDirection.EXACT, [planet, asp_planet])
                        else:
                            a_direction = determine_aspect_direction(deg_diff, calc_chart_diff)
                            p_aspect = ChartAspect(aspect.name, a_direction, [planet, asp_planet])

                        # attempt to set the aspect score
                        is_scored = p_aspect.set_aspect_score(calc_chart_diff)
                        if not is_scored:
                            print("Unable to set the aspect score.")

                        if planet not in aspects_by_planet:
                            aspects_by_planet[planet] = []
                        aspects_by_planet[planet].append(p_aspect)

    return aspects_by_planet


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


def get_planet_sign_dignity_for_planet(astra_calc_chart, planet):
    p_dig_list = astra_calc_chart.chart_dignities_by_planet[planet]
    planet_sign_dignity = None
    if len(p_dig_list) > 0:
        planet_sign_dignity = p_dig_list[0]
    return planet_sign_dignity

def calc_planet_dignities(chart_sign_degrees_by_planet):
    chart_dignities_by_planet = {}

    # Loop over the planets in the chart, capturing the appropriate PlanetDignity objects
    for planet in chart_sign_degrees_by_planet:
        chart_sign = chart_sign_degrees_by_planet[planet][0]
        full_planet_dignity_list = PlanetDignity.get_pdignity_by_planet(planet)
        this_planet_sign_dignity_list = []
        for p_dig in full_planet_dignity_list:
            if p_dig.sign == chart_sign:
                this_planet_sign_dignity_list.append(p_dig)

        chart_dignities_by_planet[planet] = this_planet_sign_dignity_list

    # TODO: Add House Dignity

    return chart_dignities_by_planet


def calc_chart_info(a_chart, garment_type):
    '''Calculate all of the chart data that we'll want to use for patterns and printing'''
    # Start by taking in the chart data, and putting the Planet and Sign objects in

    # Calculate the Planet, Sign, Chart Degrees & Planet Dignity
    chart_sign_degrees_by_planet = create_chart_planet_deg_dict(a_chart.raw_chart_data)

    # Calculate the Aspect orbs and store that
    aspect_orbs_by_planet = calc_aspect_orbs(chart_sign_degrees_by_planet)

    # Calculate the actual aspects of the chart
    chart_aspects_by_planet = calc_planet_aspects(chart_sign_degrees_by_planet, aspect_orbs_by_planet)

    # Create our dict for the dignities
    chart_dignities_by_planet = calc_planet_dignities(chart_sign_degrees_by_planet)

    # Create our calc chart object to store this in
    astra_calc_chart = AstraChartCalc(a_chart, chart_sign_degrees_by_planet, aspect_orbs_by_planet,
                                      chart_aspects_by_planet, chart_dignities_by_planet)

    # Create the ordered dict by garment inc degrees
    # this contains a dict of the chart's degrees by deg increments for garment
    garment = Garment(garment_type)
    calc_garment_dict(garment, astra_calc_chart)
    print(garment)

    return astra_calc_chart


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
        blank_chart = AstraChart("Blank Chart", 'None', None)
        calc_chart_info(blank_chart, GarmentType.HAT)
        # write_any_astra_chart_to_xcel("blank chart", 'HAT', "blank", None)
    else:
        logging.info("Chart argument given:" + chartname)

        if chartname == 'gchart':
            usechart = AstraChart(chartname, 'Genevieve', chartData.gchart)
        elif chartname == 'bchart':
            usechart = AstraChart(chartname, 'Brian', chartData.bchart)
        elif chartname == 'jchart':
            usechart = AstraChart(chartname, 'Jacob', chartData.jchart)
        elif chartname == 'rchart':
            usechart = AstraChart(chartname, 'Rebecca', chartData.rchart)
        else:
            findchart = chartData.get_chart(chartname)
            if findchart is None:
                print('Couldn\'t find the chart you are looking for..')
                return
            else:
                usechart = AstraChart(chartname, chartData.get_chart_person(chartname), findchart)

        logging.info(usechart)
        try:
            garment = GarmentType[pattname]
        except KeyError:
            garment = GarmentType.HAT

        chart_info = calc_chart_info(usechart, garment)
        print()
        #print(" Here's the calculated chart info: ")
        #print(chart_info)
        # write_any_astra_chart_to_xcel(chartname, pattname, usechart.person, usechart)


if __name__ == "__main__":
    calc_chart(sys.argv[1:])
