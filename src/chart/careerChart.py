import getopt
import logging
import sys

from src.chart import chartData
from src.chart.chartCalculator import calc_chart_info, create_chart_planet_deg_dict, calc_planet_dignities, \
    calc_aspect_orbs, calc_planet_aspects
from src.chart.chart_objects.AstraChart import AstraChart
from src.chart.chart_objects.AstraChartCalc import AstraChartCalc


def calc_basic_chart_info(a_chart):
    '''Calculate all of the chart data that we'll want to use for patterns and printing'''
    # Start by taking in the chart data, and putting the Planet and Sign objects in

    # Calculate the Planet, Sign, Chart Degrees & Planet Dignity
    chart_sign_degrees_by_planet = create_chart_planet_deg_dict(a_chart.raw_chart_data)

    # Create our dict for the dignities
    chart_dignities_by_planet = calc_planet_dignities(chart_sign_degrees_by_planet)

    # Calculate the Aspect orbs and store that
    aspect_orbs_by_planet = calc_aspect_orbs(chart_sign_degrees_by_planet)

    # Calculate the actual aspects of the chart
    chart_aspects_by_planet = calc_planet_aspects(chart_sign_degrees_by_planet, chart_dignities_by_planet, aspect_orbs_by_planet)

    # Create our calc chart object to store this in
    astra_calc_chart = AstraChartCalc(a_chart, chart_sign_degrees_by_planet, aspect_orbs_by_planet,
                                      chart_aspects_by_planet, chart_dignities_by_planet)

    return astra_calc_chart


def create_astra_calc_chart(chartname, whichchart='Natal'):
    if chartname == '':
        logging.info("Creating blank career chart")
        blank_chart = AstraChart("Blank Chart", 'None', None)
        calc_chart_info(blank_chart)
        # write_any_astra_chart_to_xcel("blank chart", 'HAT', "blank", None)
    else:
        logging.info(whichchart + " Chart argument given:" + chartname)

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
        astra_calc_chart = calc_basic_chart_info(usechart)

        print()
        print(" Here's the calculated natal chart info: ")
        print(astra_calc_chart)
        return astra_calc_chart


def calc_career_chart(argv):
    chartname = ''
    career_chartname = ''
    #pattname = 'SCARF'
    try:
        opts, args = getopt.getopt(argv, "hn:c:b:", ["natalchart=", "careerchart="])
    except getopt.GetoptError:
        print('careerChart.py -n <natal-chart-name> -c <career-chart-name>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('careerChart.py -n <natal-chart-name> -c <career-chart-name>')
            sys.exit()
        elif opt in ("-n", "--natalchart"):
            chartname = arg
        elif opt in ("-c", "--careerchart"):
            career_chartname = arg
        elif opt in "-b":
            chartname = ''

    astra_chart_natal = create_astra_calc_chart(chartname)
    astra_chart_career = create_astra_calc_chart(career_chartname)

       # garment = patternCalculator.calc_pattern(astra_calc_chart, pattname)
       # xslx_writer.write_chart_and_pattern(garment, astra_calc_chart)
        # write_any_astra_chart_to_xcel(chartname, pattname, usechart.person, usechart)


if __name__ == "__main__":
    calc_career_chart(sys.argv[1:])
