import getopt
import sys

import calculateOrbs
import chartData
import constants
import re
import scarf
import xlsxwriter
import logging

import translate
import util as putil
from AstraChart import AstraChart
from AstraXslxChart import AstraXslxChart

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def write_any_astra_chart_to_xcel(wname, garment_type, sheet_name, achart):
    """Write an astrology Chart to a spreadsheet"""
    wchart = AstraXslxChart(wname)
    wchart.create_chart_booksheet(sheet_name)
    # this changes based on the pattern and how many degrees are represented by a stitch
    wchart.set_garment(garment_type)
    deg_increments = wchart.degree_inc()

    #logging.info("Creating a blank astrology chart workbook named:" + wname)

    ## Constants ##
    # columns in spreadsheet
    USER_CHART_PLANET_COL = 1
    SHEET_DEGREE_SIGN_COL = 2
    SHEET_DEGREE_COL = 3
    SHEET_PLANET_COLOR_COL_START = 4

    # iterating rows in spreadsheet
    row_cnt = 0
    # loop through signs array
    sign_cnt = 0

    # set width of first 2 columns
    wchart.set_col_width(0, SHEET_DEGREE_SIGN_COL, 22)

    ## Section for top of sheet headers ##
    wchart.write_to_sheet_format(row_cnt, USER_CHART_PLANET_COL, "Planet / Orb", wchart.get_bold_format())
    wchart.write_to_sheet_format(row_cnt, SHEET_DEGREE_SIGN_COL, "Degree Sign", wchart.get_bold_format())
    wchart.write_to_sheet_format(row_cnt, SHEET_DEGREE_COL, "Degree range start", wchart.get_bold_format())
    p_cnt = SHEET_PLANET_COLOR_COL_START
    for planet in constants.PLANETS:
        wchart.write_to_sheet_format(row_cnt, p_cnt, planet.capitalize(), wchart.get_bold_format())
        p_cnt += 1
        #wchart.get_cell_color_format(constants.PLANET_COLORS[planet]))
    row_cnt += 1

    ## End section for top of sheet headers ##

    ## Section to prepare chart data ##
    if achart:
        orbs_by_planet = calculateOrbs.calcOrbsByPlanet(achart.get_chart_in_360degrees_for_planets())
    ## End section to prepare chart data

    # Loop over 360 chart degrees
    for deg in range(constants.MIN_SIGN_DEGREES, constants.MAX_CHART_DEGREES, deg_increments):
        #  write out chart degrees in Col C
        wchart.write_to_sheet(row_cnt, SHEET_DEGREE_COL, str(deg))

        # increment counter to next sign after 30
        if deg % constants.MAX_SIGN_DEGREES == constants.MIN_SIGN_DEGREES:
            if deg != constants.MIN_SIGN_DEGREES:
                sign_cnt += 1

        # Get sign name from array
        sign_name = constants.SIGNS[sign_cnt]
        sign_deg = str(deg % constants.MAX_SIGN_DEGREES)
        # Add row of ex: '0 Aries" etc
        wchart.write_to_sheet(row_cnt, SHEET_DEGREE_SIGN_COL, sign_deg + ' ' + sign_name.capitalize())

        wchart.set_row_cnt(row_cnt)
        ## Section for writing specifics of a chart out ##
        if achart:
            write_astra_chart(achart, wchart, sign_name, sign_deg)
            write_orbs_to_sheet(achart, wchart, orbs_by_planet, deg)

        ## End section for writing chart specifics
        row_cnt += 1

    # Close the workbook
    wchart.close_book()


def createWorkbook(wname):
    ''' Create an new Excel file and add a worksheet.'''
    workbook = xlsxwriter.Workbook(wname + '.xlsx')

    return workbook


def write_astra_chart(achart, xchart, sign_name, sign_deg):
    '''Write out the specific astra info of a chart'''
    USER_CHART_PLANET_COL = 1

    # Loop through each degree looking for matching planets and write them in, with formatting
    start_deg = int(sign_deg)
    end_deg = int(sign_deg) + xchart.degree_inc()
    user_chart_planets = ''
    planets = []
    for single_deg in range(start_deg, end_deg):
        # Write a planet from the chart here if present
        planets = achart.find_planets_at_sign_and_degree(sign_name, single_deg, True)
        if len(planets) > 0:
            user_chart_planets += str(single_deg) + ": [" + ' '.join(planets) + "] "

    if user_chart_planets != '':
        xchart.write_to_sheet(xchart.row_cnt, USER_CHART_PLANET_COL, user_chart_planets)


def write_orbs_to_sheet(achart, xchart, orbs_by_planet, deg):
    '''Write out orbs of a chart'''
    USER_CHART_PLANET_COL = 1

    # Loop through each degree looking for matching Orbs and write them in, with formatting
    start_deg = int(deg)
    end_deg = int(deg) + xchart.degree_inc()
    chart_planet_orbs = ''
    aspects = []
    for single_deg in range(start_deg, end_deg):
        # Write a planet from the chart here if present
        aspects = achart.find_aspect_center_at_360_degree(orbs_by_planet, single_deg, True)
        if len(aspects) > 0:
            chart_planet_orbs += str(single_deg) + ": [" + ' '.join(aspects) + "] "

    if chart_planet_orbs != '':
        xchart.write_to_sheet(xchart.row_cnt, USER_CHART_PLANET_COL, chart_planet_orbs)


def writePatternToXcel(wname, patWidth, sPat, chart_degrees):
    '''Write the whole pattern to Xcel'''
    # Create the workbook
    workbook = createWorkbook(wname)

    # Add the Beginning (CO instruction)
    worksheet = workbook.add_worksheet()
    worksheet.write('A1', 'CO ' + str(patWidth) + ' sts')

    # Write out pattern rows
    writePatternByRow(worksheet, sPat, patWidth, chart_degrees)

    # Close the workbook
    workbook.close()


def writePatternByRow(worksheet, sPat, patWidth, chart_degrees):
    '''Write out the pattern row by row into the worksheet'''

    # Start from the first cell, second row. Rows and columns are zero indexed.
    row = 1
    col = 0

    rowcount = 1
    for instr in sPat:
        pattName = instr[0]
        repeatStr = instr[1]
        repcount = re.findall(r'\d+', repeatStr)
        repeat = int(repcount[0])

        ## Start what scarf.fitRepeatsToRowWidth does ... TODO : this isnt work properly yet!

        # Write out which pattern to work with filler sts
        patstr = getPattInstrToWrite(pattName, patWidth)
        worksheet.write(row, col, str(patstr))
        row += 1  # increment row after writing this

        # Get some general info
        mult_add = constants.PATTERN_MULT_ADD[pattName]
        # Figure out how many times to repeat the stitch
        intSub = scarf.calcIntSub(mult_add, patWidth)
        # Store the starting count so we can see if we are missing rows at the end
        startCnt = rowcount
        missingRows = 0

        # Next, determine the number of repeats
        numRepeats = determineNumRepeats(pattName, repeat)

        # Loop over reps, writing rows and special instructions --> adjusts rowcount to track where we are
        for rep in range(numRepeats):
            maxcnt = 0
            for pattInstr in putil.PATTERN_INSTRUCTIONS[pattName]:

                # Determine if special planet placement and write
                planetText = getPlanetPlacementText(chart_degrees, rowcount)
                if planetText:
                    worksheet.write(row, col, str(planetText))
                    row += 1  # increment row after writing this

                # Fix repeat text
                pattInstr = fixRepeatStrInPatternInstruction(pattInstr, intSub)

                # Write Row instruction
                prtstr = re.sub(r'Row \d+', 'Row ' + str(rowcount), pattInstr)
                worksheet.write(row, col, str(prtstr))
                row += 1  # increment row after writing this

                # Inc rowcount
                rowcount += 1
                maxcnt += 1

                if maxcnt == repeat or maxcnt == missingRows:
                    missingRows = 0
                    break  # Bail out of this loop

            # Write any missing rows  ... same as regular writing but with a bound: missingRows
            pattRowsPrinted = rowcount - startCnt
            if pattRowsPrinted < repeat:
                # Print some more rows
                # print("----Here's some missing: ", repeat - pattRowsPrinted)
                missingRows = repeat - pattRowsPrinted
                # rowcount = printMissingRows(pattName, intSub, rowcount, missingRows, chart_degrees)

        ## End what scarf.fitRepeatsToRowWidth does


##        rowcount = scarf.fitRepeatsToRowWidth(pattName, patWidth, rowcount, int(repcount[0]), chart_degrees)


def printMissingRows(pattName, intSub, rowcount, missingRows, chart_degrees):
    maxcnt = 0
    for pattInstr in putil.PATTERN_INSTRUCTIONS[pattName]:
        if 'rep from' in pattInstr:
            pattInstr = replaceRepStr(pattInstr, intSub)
            printPattRowWithCnt(rowcount, pattInstr, chart_degrees)
        else:
            printPattRowWithCnt(rowcount, pattInstr, chart_degrees)
        rowcount = rowcount + 1
        maxcnt = maxcnt + 1
        if maxcnt == missingRows:
            # Bail out
            return rowcount
    return rowcount


def writePattRowWithCnt(rowcount, pattInstr, chart_degrees):
    ''''''
    planetText = getPlanetPlacementText(chart_degrees, rowcount)
    # if planetText:
    # write(planetText)
    prtstr = re.sub(r'Row \d+', 'Row ' + str(rowcount), pattInstr)
    # write(prtstr)


def getPlanetPlacementText(chart_degrees, rowcount):
    '''Determine if there is a planet at this degree where a marker should be placed'''
    # Move the chart degree back the asc degree, since we started the pattern at the asc as row 1
    planetText = None
    ascDeg = chart_degrees['ASC']
    for a_planet in chart_degrees:
        planetDeg = scarf.rectifyDegreeByAsc(ascDeg, chart_degrees[a_planet])
        if rowcount == planetDeg:
            planetText = "--> Place ", a_planet, " button on the following row. <--"

    return planetText


def writePattInstr(pattName, mult_add, rowWidth, rowcount, chart_degrees):
    '''Write out the pattern instruction with any special marker placements'''
    for pattInstr in putil.PATTERN_INSTRUCTIONS[pattName]:
        pattInstr = fixRepeatStrInPatternInstruction(pattInstr, mult_add, rowWidth)
        writePattRowWithCnt(rowcount, pattInstr, chart_degrees)
        rowcount = rowcount + 1
    return rowcount


def fixRepeatStrInPatternInstruction(pattInstr, intSub):
    '''If the pattern instruction has a repeat sts instr, fix the printable wording to read better'''
    if 'rep from' in pattInstr:
        pattInstr = scarf.replaceRepStr(pattInstr, intSub)
    return pattInstr


def determineNumRepeats(pattName, repeat):
    '''Determines the number of times to repeat the pattern rows'''
    if constants.PATTERN_ROWS[pattName] < repeat:  # Repeat the pattern repeat/#rows
        # print(constants.PATTERN_ROWS[pattName], " ", repeat)
        numRepeats = repeat // constants.PATTERN_ROWS[pattName]
    elif constants.PATTERN_ROWS[pattName] > repeat:
        numRepeats = repeat
        # print("------Printing partial pattern")
        ##rowcount = printPartialPattInstr(pattName, intSub, rowcount, repeat, chart_degrees)
        ##return rowcount
    else:
        numRepeats = 1

    return numRepeats


def printPartialPattInstr(pattName, intSub, rowcount, repeat, chart_degrees):
    maxcnt = 0
    for pattInstr in putil.PATTERN_INSTRUCTIONS[pattName]:
        if 'rep from' in pattInstr:
            pattInstr = replaceRepStr(pattInstr, intSub)
            printPattRowWithCnt(rowcount, pattInstr, chart_degrees)
        else:
            printPattRowWithCnt(rowcount, pattInstr, chart_degrees)
        rowcount = rowcount + 1
        maxcnt = maxcnt + 1
        if maxcnt == repeat:
            # Bail out
            return rowcount
    return rowcount


def getPattInstrToWrite(pattName, rowWidth):
    mult_add = constants.PATTERN_MULT_ADD[pattName]
    # Figure out if we need to add some filler stitches because it wont fit
    fillerSts = scarf.calcFillerSts(mult_add, rowWidth)

    return "...Work ", pattName, ", filling in ", fillerSts, " extra sts", " as:"


def fitRepeatsToRowWidth(pattName, rowWidth, rowcount, repeat, chart_degrees):
    mult_add = constants.PATTERN_MULT_ADD[pattName]
    # Figure out how many times to repeat the stitch
    intSub = scarf.calcIntSub(mult_add, rowWidth)
    # Figure out if we need to add some filler stitches because it wont fit
    fillerSts = scarf.calcFillerSts(mult_add, rowWidth)

    startCnt = rowcount

    if pattName in putil.PATTERN_INSTRUCTIONS:
        print("...Work ", pattName, ", filling in ", fillerSts, " extra sts", " as:")
        if constants.PATTERN_ROWS[pattName] < repeat:  # Repeat the pattern repeat/#rows
            # print(constants.PATTERN_ROWS[pattName], " ", repeat)
            numRepeats = repeat // constants.PATTERN_ROWS[pattName]
        elif constants.PATTERN_ROWS[pattName] > repeat:
            # print("------Printing partial pattern")
            rowcount = printPartialPattInstr(pattName, intSub, rowcount, repeat, chart_degrees)
            return rowcount
        else:
            numRepeats = 1

        for rep in range(numRepeats):
            # if rep > 0:
            #     print("REP: ", rep)
            rowcount = printPattInstr(pattName, intSub, rowcount, chart_degrees)

        pattRowsPrinted = rowcount - startCnt
        if pattRowsPrinted < repeat:
            # Print some more rows
            # print("----Here's some missing: ", repeat - pattRowsPrinted)
            missingRows = repeat - pattRowsPrinted
            rowcount = printMissingRows(pattName, intSub, rowcount, missingRows, chart_degrees)

    else:
        print(mult_add, " Repeat ", pattName, " ", intSub, " times, filling in ", fillerSts, " extra sts")
    return rowcount

    # Iterate over the data and write it out row by row.


'''    for item, cost in (expenses):
        worksheet.write(row, col,     item)
        worksheet.write(row, col + 1, cost)
        row += 1
'''


# Widen the first column to make the text clearer.
# worksheet.set_column('A:A', 20)

# Add a bold format to use to highlight cells.
# bold = workbook.add_format({'bold': True})

# Write some simple text.
# worksheet.write('A1', 'Hello')

# Text with formatting.
# worksheet.write('A2', 'World', bold)

# Write some numbers, with row/column notation.
# worksheet.write(2, 0, 123)
# worksheet.write(3, 0, 123.456)

# Insert an image.
# worksheet.insert_image('B5', 'logo.png')


def chart_writer(argv):
    chartname = ''
    try:
        opts, args = getopt.getopt(argv, "hc:b:", ["chart="])
    except getopt.GetoptError:
        print('chartWriter.py -c <chart-name>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('chartWriter.py -c <chart-name>')
            sys.exit()
        elif opt in ("-c", "--chart"):
            chartname = arg
        elif opt in "-b":
            chartname = ''

    if chartname == '':
        logging.info("Creating blank astra chart")
        write_any_astra_chart_to_xcel("blank chart", 'HAT', "blank", None)
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
            print('Couldn\'t find the chart you are looking for..')
            return

        usechart.print_info()
        write_any_astra_chart_to_xcel(chartname, 'HAT', usechart.person, usechart)


if __name__ == "__main__":
    chart_writer(sys.argv[1:])
