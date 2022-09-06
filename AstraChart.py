#!/usr/bin/python
import logging

import constants

sign_idx = 0
deg_idx = 1
sun_idx = 0


class AstraChart:
    def __init__(self, chartname, person, chart_data):
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
