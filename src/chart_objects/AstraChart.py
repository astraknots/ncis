#!/usr/bin/python
import logging

import constants
import dignities
import translate

sign_idx = 0
deg_idx = 1
sun_idx = 0


def find_planet_dignity_scores(planet_list, sign):
    planet_dignities = {}
    sign_dignity = {}
    for planet in planet_list:
        dignity = dignities.get_planet_dignity(planet.upper(), sign.upper())
        dscore = dignities.get_planet_dignity_score(planet.upper(), dignity, sign.upper())
        planet_dignities[planet] = {sign: (dignity, dscore)}

    return planet_dignities


class AstraChart:
    # Raw chart info
    chartname = ""
    person = ""
    raw_chart_data = {}
    # Calculated & organized chart data --> see subclass AstraChartCalc
    chart_degrees = None  # Legacy: used for chartWriter

    def __init__(self, chartname, person, raw_chart_data):
        self.chart_degrees = None
        self.chartname = chartname
        self.person = person
        self.raw_chart_data = raw_chart_data  # Currently the chart data is a dict, see chartData.py

    def get_str_rep(self):
        return f"Chart Info: {self.chartname} for {self.person} \n Raw Chart Data: {self.raw_chart_data}"

    def __str__(self):
        return self.get_str_rep()

    def __repr__(self):
        return self.get_str_rep()


    # Older methods for initial version of chartWriter
    def find_planets_at_sign_and_degree(self, sign_name, sign_deg, cap):
        '''Return list of planets found or empty list. By sign and degree (Alt: 360 degree)'''
        # logging.info("Looking for planets at " + str(sign_deg) + ' ' + sign_name)

        found_planets = []

        for planet in constants.PLANETS:
            chart_sign = self.raw_chart_data[planet][0]
            chart_deg = self.raw_chart_data[planet][1]
            if chart_sign == sign_name and str(chart_deg) == str(sign_deg):
                # logging.info("Found Planet " + planet + " at " + str(chart_deg) + " of " + chart_sign)
                if cap:
                    found_planets.append(planet.capitalize())
                else:
                    found_planets.append(planet)

        return found_planets

    def find_aspect_center_at_360_degree(self, orbs_by_planet, deg, cap):
        '''Return a list of planet aspects on the 360 degree chart (Alt: by sign and degree)'''
        found_aspects = []

        for planet in constants.PLANETS:
            chart_aspect_list = orbs_by_planet[planet]
            # logging.debug(chart_aspect_list)
            for aspect in constants.ASPECTS:
                deg_list = chart_aspect_list[aspect]  # like [308. 324]
                # logging.debug("Deg list:" + str(chart_aspect_list[aspect]))
                if deg in deg_list:
                    logging.debug("Found: " + planet + " " + aspect + " at " + str(deg))
                    if cap:
                        found_aspects.append(planet.capitalize() + " " + aspect.capitalize())
                    else:
                        found_aspects.append(planet + " " + aspect)

        return found_aspects

    def translate_chart_to_degrees_for_planets(self):
        '''Return the chart with the 360 degree version'''
        chart_degrees = translate.translateChartToDegreesForPlanets(self.raw_chart_data)
        self.chart_degrees = chart_degrees
        return chart_degrees

    def get_chart_in_360degrees_for_planets(self):
        '''Get or set and get the chart in 360 Degrees by planets'''
        if self.chart_degrees:
            return self.chart_degrees
        else:
            return self.translate_chart_to_degrees_for_planets()
