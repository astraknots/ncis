import getopt
import sys

import chartData
import constants
import re
import scarf
import xlsxwriter
import logging

import util as putil

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def createWorkbook(wname):
    ''' Create an new Excel file and add a worksheet.'''
    workbook = xlsxwriter.Workbook(wname + '.xlsx')

    return workbook


def write_blank_astra_chart_to_xcel(wname):
    """Write a blank astrology Chart to a spreadsheet"""
    logging.info("Creating a blank astrology chart workbook named:" + wname)
    # Create the workbook
    workbook = createWorkbook(wname)

    # Add blank chart worksheet
    worksheet = workbook.add_worksheet("blank chart")

    ## Constants ##
    # loop through signs array
    sign_cnt = 0
    # columns in spreadsheet
    degree_sign_col = 2
    degree_col = 3
    # iterating rows in spreadsheet
    row_cnt = 0
    # iterating the chart and signs
    max_sign_degrees = 30
    min_sign_degrees = 0
    max_chart_degrees = 360
    deg_increments = 3  # this changes based on the pattern and how many degrees are represented by a stitch

    # set width of first 2 columns
    worksheet.set_column(0, degree_sign_col, 15)

    # Loop through and write out chart degrees in Col C //scarf - deg = 1 st
    for deg in range(min_sign_degrees, max_chart_degrees, deg_increments):
        # print(str(deg))
        worksheet.write(row_cnt, degree_col, str(deg))

        # increment counter to next sign after 30
        if deg % max_sign_degrees == min_sign_degrees:
            if deg != min_sign_degrees:
                sign_cnt += 1

        # Get sign name from array
        sign_name = constants.SIGNS[sign_cnt]
        sign_deg = str(deg % max_sign_degrees)
        # Add row of ex: '0 Aries" etc
        # print("sign + deg=", sign_deg + ' ' + sign_name.capitalize())
        worksheet.write(row_cnt, degree_sign_col, sign_deg + ' ' + sign_name.capitalize())
        row_cnt += 1
        # print("sign_cnt = " + str(sign_cnt))
        # print("sign_name = " + constants.SIGNS[sign_cnt])

    # Close the workbook
    workbook.close()


def find_planet_at_degree(user_chart, sign_name, sign_deg):
    '''Look for a planet at the sign and degree given, return blank if not found'''
    logging.info("Looking for a planet at " + str(sign_deg) + ' ' + sign_name)

    for planet in constants.PLANETS:
        chart_sign = user_chart[planet][0]
        chart_deg = user_chart[planet][1]
        logging.info("Planet " + planet + " at " + str(chart_deg) + " of " + chart_sign)
        if chart_sign == sign_name and str(chart_deg) == str(sign_deg):
            return planet.capitalize()

    return ''


def find_planets_at_degree(user_chart, sign_name, sign_deg):
    '''Look for planets at the sign and degree given, concatonate if multiple found return blank if not found'''
    logging.info("Looking for planets at " + str(sign_deg) + ' ' + sign_name)

    found_planets = ''

    for planet in constants.PLANETS:
        chart_sign = user_chart[planet][0]
        chart_deg = user_chart[planet][1]
        if chart_sign == sign_name and str(chart_deg) == str(sign_deg):
            logging.info("Found Planet " + planet + " at " + str(chart_deg) + " of " + chart_sign)
            found_planets += planet.capitalize() + ":(" + str(chart_deg) + ") "

    return found_planets


def write_astra_chart_to_xcel(chartname, user_chart):
    '''Write a user's astra chart to xcel'''
    logging.info("Creating astrology chart workbook named:" + chartname)
    logging.info("Chart data:")
    logging.info(user_chart)
    # Create the workbook
    workbook = createWorkbook(chartname)

    # Add blank chart worksheet
    worksheet = workbook.add_worksheet(chartname)

    ## Constants ##
    # loop through signs array
    sign_cnt = 0
    # columns in spreadsheet
    user_chart_planet_col = 1
    degree_sign_col = 2
    degree_col = 3
    # iterating rows in spreadsheet
    row_cnt = 0
    # iterating the chart and signs
    max_sign_degrees = 30
    min_sign_degrees = 0
    max_chart_degrees = 360
    deg_increments = 3  # this changes based on the pattern and how many degrees are represented by a stitch

    # set width of first 2 columns
    worksheet.set_column(0, degree_sign_col, 20)

    # Loop through and write out chart degrees in Col C //scarf - deg = 1 st
    for deg in range(min_sign_degrees, max_chart_degrees, deg_increments):
        # print(str(deg))
        worksheet.write(row_cnt, degree_col, str(deg))

        # increment counter to next sign after 30
        if deg % max_sign_degrees == min_sign_degrees:
            if deg != min_sign_degrees:
                sign_cnt += 1

        # Get sign name from array
        sign_name = constants.SIGNS[sign_cnt]
        sign_deg = str(deg % max_sign_degrees)
        # Add row of ex: '0 Aries" etc
        logging.info("sign + deg=" + str(sign_deg) + " " + sign_name.capitalize())
        worksheet.write(row_cnt, degree_sign_col, sign_deg + ' ' + sign_name.capitalize())

        ## Begin section different from the base blank chart ##

        # Modify if the degree increments for the pattern/chart differ from 1
        start_deg = int(sign_deg)
        end_deg = int(sign_deg) + deg_increments
        user_chart_planets = ''
        for single_deg in range(start_deg, end_deg):
            # Write a planet from the chart here if present
            user_chart_planet = find_planets_at_degree(user_chart, sign_name, single_deg)
            user_chart_planets += user_chart_planet + ' '

        if user_chart_planets != '':
            worksheet.write(row_cnt, user_chart_planet_col, user_chart_planets)

        ## End section diff from blank base

        row_cnt += 1
        # print("sign_cnt = " + str(sign_cnt))
        # print("sign_name = " + constants.SIGNS[sign_cnt])

    # Close the workbook
    workbook.close()

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
        write_blank_astra_chart_to_xcel('blank_chart')
    else:
        logging.info("Chart argument given:" + chartname)
        usechart = []
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
        write_astra_chart_to_xcel(chartname, usechart)


if __name__ == "__main__":
    chart_writer(sys.argv[1:])
