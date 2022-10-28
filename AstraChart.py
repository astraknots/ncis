#!/usr/bin/python
import logging

import constants
import translate

sign_idx = 0
deg_idx = 1
sun_idx = 0


class AstraChart:
    def __init__(self, chartname, person, chart_data):
        self.chart_degrees = None
        self.chartname = chartname
        self.person = person
        self.chart_data = chart_data  # Currently the chart data is a dict, see chartData.py

    def print_info(self):
        print(self.chartname + " for " + self.person)
        print()
        print(self.chart_data)

    def chartname(self):
        print("The chart's name is: ", self.chartname)
        return self.chartname

    def chart_for(self):
        print("The chart is for: ", self.person)
        return self.person

    def sun_sign(self):
        sun_planet = constants.PLANETS[sun_idx]
        return self.chart_data[sun_planet][sign_idx]

    def sun_sign_degree(self):
        sun_planet = constants.PLANETS[sun_idx]
        return self.chart_data[sun_planet][deg_idx]

    def find_planets_at_sign_and_degree(self, sign_name, sign_deg, cap):
        '''Return list of planets found or empty list. By sign and degree (Alt: 360 degree)'''
        # logging.info("Looking for planets at " + str(sign_deg) + ' ' + sign_name)

        found_planets = []

        for planet in constants.PLANETS:
            chart_sign = self.chart_data[planet][0]
            chart_deg = self.chart_data[planet][1]
            if chart_sign == sign_name and str(chart_deg) == str(sign_deg):
                #logging.info("Found Planet " + planet + " at " + str(chart_deg) + " of " + chart_sign)
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
            #logging.debug(chart_aspect_list)
            for aspect in constants.ASPECTS:
                deg_list = chart_aspect_list[aspect]  # like [308. 324]
                #logging.debug("Deg list:" + str(chart_aspect_list[aspect]))
                if deg in deg_list:
                    logging.debug("Found: " + planet + " " + aspect + " at " + str(deg))
                    if cap:
                        found_aspects.append(planet.capitalize() + " " + aspect.capitalize())
                    else:
                        found_aspects.append(planet + " " + aspect)

        return found_aspects

    def translate_chart_to_degrees_for_planets(self):
        '''Return the chart with the 360 degree version'''
        chart_degrees = translate.translateChartToDegreesForPlanets(self.chart_data)
        self.chart_degrees = chart_degrees
        return chart_degrees

    def get_chart_in_360degrees_for_planets(self):
        '''Get or set and get the chart in 360 Degrees by planets'''
        if self.chart_degrees:
            return self.chart_degrees
        else:
            return self.translate_chart_to_degrees_for_planets()


