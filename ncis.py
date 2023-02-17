#!/usr/bin/python

import getopt
import logging
import re
import sys

import calculateOrbs
from src.chart import chartData
import chartWriter
import scarf
import translate

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def main(argv):
    chartname = ''
    usechart = []
    try:
        opts, args = getopt.getopt(argv, "hc:", ["chart="])
    except getopt.GetoptError:
        print('ncis.py -c <chart-name>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('ncis.py -c <chart-name>')
            sys.exit()
        elif opt in ("-c", "--chart"):
            chartname = arg

    if chartname == '':
        print('You must specify chartname for data. Try ncis.py -c <chartname>')
        return
    else:
        if chartname == 'gchart':
            usechart = chartData.gchart
        elif chartname == 'bchart':
            usechart = chartData.bchart
        elif chartname == 'jchart':
            usechart = chartData.jchart
        elif chartname == 'rchart':
            usechart = chartData.rchart
        else:
            print('Couldn\'t find the chart you are looking for..')
            return

    logging.info("User chart:")
    logging.info(usechart)
    chart_degrees = translate.translateChartToDegreesForPlanets(usechart)
    sign_degree_dict = translate.translateChartToSigns(usechart)

    orb_degree_dict = calculateOrbs.calcOrbsOfInfluence(chart_degrees, sign_degree_dict)

    scarf_pattern = scarf.figureScarfPattern(orb_degree_dict, sign_degree_dict)

    '''possible_patterns2 = getPatternsForRowCountExpand(grouped_byAspect)
possible_patterns3 = getPatternsForMaxRowCount(grouped_byAspect)'''

    '''for x in range(0,88):
        print(str(len(possible_patterns1[x][2])), " - ", str(len(possible_patterns2[x][2])), " - ", str(len(possible_patterns3[x][2])))	'''



    print(" --------------------")
    sPat = scarf.figurePatternRows(scarf_pattern)

    # Pattern Width : 35 sts
    patWidth = scarf.findRowWidthForPattern()

    print("THE PATTERN :", sPat)
    print("CO ", patWidth, " sts.")

    chartWriter.writePatternToXcel(chartname, patWidth, sPat, chart_degrees)

    rowcount = 1
    for instr in sPat:
        #print(constants.PATTERN_MULT_ADD[instr[0]])
        pattName = instr[0]
        repeat = instr[1]
        repcount = re.findall(r'\d+', repeat)
        #print("REPEAT:", repeat, " ", int(repcount[0]))
        rowcount = scarf.fitRepeatsToRowWidth(pattName, patWidth, rowcount, int(repcount[0]), chart_degrees)
        #rowcount = rowcount + 1
        #print(pattName)
        #print(repeat)


if __name__ == "__main__":
    main(sys.argv[1:])

