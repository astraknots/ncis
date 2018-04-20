#!/usr/bin/python

import sys, getopt
import translate, calculateOrbs, scarf, chartWriter
import re, logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Start with a chart
gchart = { 'SUN' : ['PISCES',1], 'MOON' : ['CAPRICORN', 17], 'ASC' : ['VIRGO', 28], 'MERCURY' : ['AQUARIUS', 5], 'VENUS' : ['CAPRICORN', 25], 'MARS' : ['LIBRA', 19], 'JUPITER' : ['SCORPIO', 10], 'SATURN' : ['LIBRA', 21], 'URANUS' : ['SAGITTARIUS', 4], 'NEPTUNE' : ['SAGITTARIUS', 26], 'PLUTO' : ['LIBRA', 26]}

bchart = { 'SUN' : ['VIRGO',8], 'MOON' : ['SCORPIO', 2], 'ASC' : ['LEO', 17], 'MERCURY' : ['VIRGO', 7], 'VENUS' : ['LIBRA', 15], 'MARS' : ['TAURUS', 6], 'JUPITER' : ['AQUARIUS', 3], 'SATURN' : ['CANCER', 2], 'URANUS' : ['LIBRA', 20], 'NEPTUNE' : ['SAGITTARIUS', 4], 'PLUTO' : ['LIBRA', 3]}

jchart = { 'SUN' : ['SCORPIO',24], 'MOON' : ['CANCER', 28], 'ASC' : ['SAGITTARIUS', 16], 'MERCURY' : ['SCORPIO', 5], 'VENUS' : ['CAPRICORN', 4], 'MARS' : ['LIBRA', 7], 'JUPITER' : ['GEMINI', 7], 'SATURN' : ['TAURUS', 27], 'URANUS' : ['AQUARIUS', 17], 'NEPTUNE' : ['AQUARIUS', 4], 'PLUTO' : ['SAGITTARIUS', 12]}

rchart = { 'SUN' : ['CANCER',14], 'MOON' : ['VIRGO', 21], 'ASC' : ['CAPRICORN', 18], 'MERCURY' : ['GEMINI', 26], 'VENUS' : ['LEO', 8], 'MARS' : ['GEMINI', 22], 'JUPITER' : ['LIBRA', 2], 'SATURN' : ['LIBRA', 3], 'URANUS' : ['SCORPIO', 26], 'NEPTUNE' : ['SAGITTARIUS', 22], 'PLUTO' : ['LIBRA', 21]}

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
            usechart = gchart
        elif chartname == 'bchart':
            usechart = bchart
        elif chartname == 'jchart':
            usechart = jchart
        elif chartname == 'rchart':
            usechart = rchart
        else:
            print('Couldn\'t find the chart you are looking for..')
            return

    logging.info("User chart:")
    logging.info(usechart)
    chart_degrees = translate.translate_chart_to_degrees_for_planets(usechart)
    sign_degree_dict = translate.translate_chart_to_signs(usechart)

    orb_degree_dict = calculateOrbs.calc_orbs_of_influence(chart_degrees, sign_degree_dict)

    scarf_pattern = scarf.figure_scarf_pattern(orb_degree_dict, sign_degree_dict)

    '''possible_patterns2 = getPatternsForRowCountExpand(grouped_byAspect)
possible_patterns3 = getPatternsForMaxRowCount(grouped_byAspect)'''

    '''for x in range(0,88):
        print(str(len(possible_patterns1[x][2])), " - ", str(len(possible_patterns2[x][2])), " - ", str(len(possible_patterns3[x][2])))	'''



    print(" --------------------")
    sPat = scarf.figure_pattern_rows(scarf_pattern)

    # Pattern Width : 35 sts
    patWidth = scarf.find_row_width_for_pattern()

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
        rowcount = scarf.fit_repeats_to_row_width(pattName, patWidth, rowcount, int(repcount[0]), chart_degrees)
        #rowcount = rowcount + 1
        #print(pattName)
        #print(repeat)


if __name__ == "__main__":
    main(sys.argv[1:])

