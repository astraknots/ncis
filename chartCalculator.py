import getopt
import logging
import sys

import Planet
import Sign
import chartData
import constants
from AstraChart import AstraChart
from AstraChartCalc import AstraChartCalc
from ChartDegree import ChartDegree
from Garment import Garment


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


def calc_chart_info(a_chart, garment):
    # Start by taking in the chart data, and putting the Planet and Sign objects in
    raw_chart_data = a_chart.chart_data  # May look like:  { 'SUN' : ['VIRGO',8], 'MOON' : ['SCORPIO', 2], ....
    astra_calc_chart = AstraChartCalc(raw_chart_data)  # we'll populate with our converted output

    chart_dict = create_chart_dict(raw_chart_data)
    astra_calc_chart.planet_sign_degrees = chart_dict

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
        calc_chart_info(blank_chart, Garment.HAT)
        #write_any_astra_chart_to_xcel("blank chart", 'HAT', "blank", None)
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
            garment = Garment[pattname]
        except KeyError:
            garment = Garment.HAT

        chart_info = calc_chart_info(usechart, garment)
        print()
        print(" Here's the calculated chart info: ")
        print(chart_info)
        #write_any_astra_chart_to_xcel(chartname, pattname, usechart.person, usechart)


if __name__ == "__main__":
    calc_chart(sys.argv[1:])
