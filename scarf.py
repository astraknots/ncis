#!/usr/bin/python

from itertools import groupby

import aspects
import astrology_aspects as _aspects
import constants
import patterns
import shapes
import util as putil
import re
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


ASPECTS_FOR_DEG_IDX = 0  # Index of the list of aspect patterns for this row
NUM_ROWS_IDX = 1         # Index of the number of rows this aspect pattern repeats
LIST_POSS_PATTS_IDX = 2  # Index of the list of possible patterns


def group_by_aspect(orb_degree_dict):
    ret_group = []
    # Calc nominal value
    for d in range(1, 361):
        ret_list = orb_degree_dict[d]
        logging.debug("orb_degree_dict[d]:")
        logging.debug(orb_degree_dict[d])
        ret_group.append(ret_list)

    grouped_byList = [(k, sum(1 for i in g)) for k, g in groupby(ret_group)]
    logging.debug("grouped_byList:")
    logging.debug(grouped_byList)
    return grouped_byList


def group_by_element(patternList):
    grouped_byList = [(k, sum(1 for i in g)) for k, g in groupby(patternList)]
    return grouped_byList


def figure_scarf_pattern(orb_degree_dict, sign_degree_dict):
    grouped_by_aspect = group_by_aspect(orb_degree_dict)
    logging.debug("aspects by rows:")
    logging.debug(grouped_by_aspect)

    # This groups repeating rows of aspects with possible patterns
    possible_patterns_for_row_cnt = patterns.get_patterns_for_row_count(grouped_by_aspect)
    logging.debug("possible_patterns_for_row_cnt")
    logging.debug(possible_patterns_for_row_cnt)

    scarf_pattern = []
    i = 1

    for p in possible_patterns_for_row_cnt:
        logging.debug("***** Starting on row (i=:" + str(i) + ") ***** orb_degree_dict[i]:" )
        logging.debug(orb_degree_dict[i])
        logging.debug("sign_degree_dict[i]")
        logging.debug(sign_degree_dict[i])
        logging.debug("Repeat for " + str(p[NUM_ROWS_IDX]) + " rows. Poss patts for rowcnt:")
        logging.debug(p[LIST_POSS_PATTS_IDX])

        best_patt = ''

        # Start with simplifying if there really is only 1 pattern that fits this many rows
        if len(p[LIST_POSS_PATTS_IDX]) == 1:
            logging.debug("..Only pattern for " + str(p[NUM_ROWS_IDX]) + " rows:")
            logging.debug(p[LIST_POSS_PATTS_IDX])
            best_patt = p[LIST_POSS_PATTS_IDX][0]
        else:
            best_patt = determine_best_pattern(i, p[ASPECTS_FOR_DEG_IDX], p[LIST_POSS_PATTS_IDX], p[NUM_ROWS_IDX], sign_degree_dict)

        scarf_pattern.append([best_patt, p[NUM_ROWS_IDX]])
        i += p[NUM_ROWS_IDX]

    return scarf_pattern


def determine_best_pattern(row_num, row_aspects, poss_patterns, num_rows_repeat, sign_degree_dict):
    """Try to figure out the best pattern for all this info"""

    # Add additional aspects for patterns repeating over rows that cross signs
    row_aspects = aspects.add_sign_aspects_for_span(sign_degree_dict, row_num, num_rows_repeat, row_aspects)

    poss_patterns = patterns.add_poss_patterns_for_span(sign_degree_dict, row_num, num_rows_repeat, poss_patterns)

    maxRow = _aspects.adjust_degree_for_360(row_num + num_rows_repeat)
    print("Determining best pattern for row num:", row_num, " with aspects:", row_aspects, " repeating for ",
          num_rows_repeat, "rows in sign(s):", sign_degree_dict[row_num], "-", sign_degree_dict[maxRow],
          " with poss patts by rowCnt, sign aspects:", poss_patterns)

    bestPattsByShape = shapes.determineBestPatternsForShapeMatch(poss_patterns, row_aspects)
    isBest = patterns.pickIfOnePattern(bestPattsByShape)
    if isBest not in ['Nope', 'None']:
        ##print("..Found best pattern by shape match", isBest)
        return isBest
    elif isBest in ['None']:
        # do something else
        ##print("Unable to determine by shape", possPatterns)
        bestPatt = patterns.determineBestPatternBySomething(poss_patterns, num_rows_repeat, row_num, sign_degree_dict,
                                                            row_aspects)
        return bestPatt
    else:
        # narrow further
        ##print("Narrowed by shape to", bestPattsByShape)
        bestPatt = patterns.determineBestPatternBySomething(bestPattsByShape, num_rows_repeat, row_num, sign_degree_dict, row_aspects)
        return bestPatt


def figure_pattern_rows(scarf_pattern):
    groupedByStitch = group_by_element(scarf_pattern)
    # print("Groupd By Stitch", groupedByStitch)
    pattern_rows = []
    for stitchRows, repeat in groupedByStitch:
        stitch = stitchRows[0]
        stitchRepeat = stitchRows[1]
        ##print("stitch: ", stitch, " stitch rep:", stitchRepeat, " repeat:", repeat)
        pattern_rows.append([stitch, "Repeat for " + str(stitchRepeat * repeat) + " rows"])

    return pattern_rows


def figure_pattern_width(scarf_pattern_w_rows):
    tot = len(scarf_pattern_w_rows)
    rowWidth = find_row_width_for_patterns(scarf_pattern_w_rows)
    '''fRw(scarf) = lcm(fRw(scarfMult[0], fRw(scarfMult[1]), fRw(scarfMult[2]))'''


def gcd(a, b):
    """Return greatest common divisor using Euclid's Algorithm."""
    while b:
        a, b = b, a % b
    return a


def lcm(a, b):
    """Return lowest common multiple."""
    return a * b // gcd(a, b)


def rowLenForMultAdd(m1, a1, m2, a2):
    if a1 == 0 and a2 == 0:
        return lcm(m1, m2)


def get_mult_from_list(multAddList):
    listOfNums = []
    for mult, add in multAddList:
        if mult not in listOfNums:
            listOfNums.append(mult)
    return listOfNums


def get_add_from_list(multAddList):
    listOfNums = []
    for mult, add in multAddList:
        if add not in listOfNums:
            listOfNums.append(add)
    return listOfNums


def get_lcm_from_list(numList):
    tot = len(numList)
    half = tot // 2
    ##print(tot, " start getlcmfromlist with:", numList, ", ", numList[:half], " - ", numList[half:])
    if tot == 1:
        return numList[0]
    elif tot == 2:
        return lcm(numList[:half][0], numList[half:][0])
    else:
        return lcm(get_lcm_from_list(numList[:half]), get_lcm_from_list(numList[half:]))


def get_largest(numList):
    largest = 0
    for num in numList:
        if num > largest:
            largest = num

    return largest


def mult_covers_all_adds(pattList, lcm):
    for mult, add in pattList:
        if (lcm - add) % mult != 0:
            return False
    return True


def find_best_row_len(some_patts):
    multList = get_mult_from_list(some_patts)
    lcm = get_lcm_from_list(multList)
    ##print(" LCM:", lcm)

    if mult_covers_all_adds(some_patts, lcm):
        return lcm
    else:
        # Try adding the largest add and then keep going
        largestAdd = get_largest(multList)
        ##print("largest add:", largestAdd)
        while not mult_covers_all_adds(some_patts, lcm):
            lcm += largestAdd
            ##print("Added largestAdd to get:", lcm)
        return lcm


def find_row_width_for_patterns(s_pat):
    even_add_pats = []
    odd_add_pats = []
    for instr in s_pat:
        pattern = instr[0]
        mult_add = constants.PATTERN_MULT_ADD[pattern]
        the_add = mult_add[1]
        if the_add == 0 or the_add % 2 == 0: # Even
            if mult_add not in even_add_pats:
                even_add_pats.append(mult_add)
        else:   #Odd
            if mult_add not in odd_add_pats:
                odd_add_pats.append(mult_add)

    ##print("Evens:", even_add_pats)
    #rowLenEven = findBestRowLen(even_add_pats)
    #print("Best even row len", rowLenEven)

    ##print("Odds:", odd_add_pats)
    #rowLenOdd = findBestRowLen(odd_add_pats)
    #print("Best odd row len", rowLenOdd)

    return 0


def rectify_degree_by_asc(ascDeg, chartPlanetDeg):
    #print("chartPlanetDeg:", chartPlanetDeg, " ascDeg:", ascDeg)
    if ascDeg > 360 or chartPlanetDeg > 360:
        raise ValueError('Chart or ASC degree should never exceed 360')
    tryDeg = chartPlanetDeg - ascDeg
    if tryDeg < 0:
        #print("Try deg < 0: ", tryDeg)
        return tryDeg + 360
    elif tryDeg > 360: # Don't think this case is really hit; see unit test but doesn't really handle for vals over 360
        raise ValueError('Difference of Chart degree minus ASC degree should never exceed 360')
        #print("Try deg > 360: ", tryDeg)
        #return tryDeg - 360
    else:
        #print("Rect deg: ", tryDeg)
        return tryDeg


def print_patt_row_with_cnt(rowcount, pattInstr, chart_degrees):
    '''Move the chart degree back the asc degree, since we started the pattern at the asc as row 1'''
    ascDeg = chart_degrees['ASC']
    for a_planet in chart_degrees:
        planetDeg = rectify_degree_by_asc(ascDeg, chart_degrees[a_planet])
        if rowcount == planetDeg:
            print("--> Place ", a_planet, " button on the following row. <--")
    #print(pattInstr)
    prtstr = re.sub(r'Row \d+', 'Row ' + str(rowcount), pattInstr)
    print(prtstr)


def replace_rep_str(pattInstr, intSub):
    '''Replaces the rep from * piece of a pattern with the number of repeats'''
    return pattInstr.replace('rep from *', 'rep from * (' + str(intSub) + ') times')


def print_patt_instr(pattName, intSub, rowcount, chart_degrees):
    for pattInstr in putil.PATTERN_INSTRUCTIONS[pattName]:
        if 'rep from' in pattInstr:
            pattInstr = replace_rep_str(pattInstr, intSub)
            print_patt_row_with_cnt(rowcount, pattInstr, chart_degrees)
        else:
            print_patt_row_with_cnt(rowcount, pattInstr, chart_degrees)
        rowcount = rowcount + 1
    return rowcount


def print_partial_patt_instr(pattName, intSub, rowcount, repeat, chart_degrees):
    # TODO: Need to move printing filler sts and that logic down to the indiv row level of a pattern
    maxcnt = 0
    for pattInstr in putil.PATTERN_INSTRUCTIONS[pattName]:
        if 'rep from' in pattInstr:
            pattInstr = replace_rep_str(pattInstr, intSub)
            print_patt_row_with_cnt(rowcount, pattInstr, chart_degrees)
        else:
            print_patt_row_with_cnt(rowcount, pattInstr, chart_degrees)
        rowcount = rowcount + 1
        maxcnt = maxcnt + 1
        if maxcnt == repeat:
            # Bail out
            return rowcount
    return rowcount


def print_missing_rows(pattName, intSub, rowcount, missingRows, chart_degrees):
    maxcnt = 0
    for pattInstr in putil.PATTERN_INSTRUCTIONS[pattName]:
        if 'rep from' in pattInstr:
            pattInstr = replace_rep_str(pattInstr, intSub)
            print_patt_row_with_cnt(rowcount, pattInstr, chart_degrees)
        else:
            print_patt_row_with_cnt(rowcount, pattInstr, chart_degrees)
        rowcount = rowcount + 1
        maxcnt = maxcnt + 1
        if maxcnt == missingRows:
            # Bail out
            return rowcount
    return rowcount


def calc_filler_sts(mult_add, rowWidth):
    '''Figure out if we need to add some filler stitches because it wont fit'''
    #TODO:  Def think there's a bug in here, not every row has same length of sts for add/mult of the whole pattern
    # subtract add from rowWidth
    add_ = mult_add[1]
    mult_ = mult_add[0]
    intSub = calc_int_sub(mult_add, rowWidth)
    # Figure out if we need to add some filler stitches because it wont fit
    fillerSts = rowWidth - intSub * mult_ + add_

    return fillerSts


def calc_int_sub(mult_add, rowWidth):
    '''Figure out how many times to repeat the stitch'''
    # TODO: this is another source of the bug since the add also doesn't necessarily apply for every row within the pattern
    add_ = mult_add[1]
    mult_ = mult_add[0]
    # Figure out how many times to repeat the stitch
    # subtract add from rowWidth
    divideMultsOver = rowWidth - add_
    intSub = divideMultsOver // mult_

    return intSub


def fit_repeats_to_row_width(pattName, rowWidth, rowcount, repeat, chart_degrees):
    # TODO: Need to loop over individual patt instructions (row by row) to determine filler, etc
    mult_add = constants.PATTERN_MULT_ADD[pattName]
    # Figure out how many times to repeat the stitch
    intSub = calc_int_sub(mult_add, rowWidth)
    # Figure out if we need to add some filler stitches because it wont fit
    fillerSts = calc_filler_sts(mult_add, rowWidth)

    startCnt = rowcount

    if pattName in putil.PATTERN_INSTRUCTIONS:
        print("...Work ", pattName, ", filling in ", fillerSts, " extra sts", " as:")
        if constants.PATTERN_ROWS[pattName] < repeat:  # Repeat the pattern repeat/#rows
            # print(constants.PATTERN_ROWS[pattName], " ", repeat)
            numRepeats = repeat // constants.PATTERN_ROWS[pattName]
        elif constants.PATTERN_ROWS[pattName] > repeat:
            print("------Printing partial pattern")
            rowcount = print_partial_patt_instr(pattName, intSub, rowcount, repeat, chart_degrees)
            return rowcount
        else:
            numRepeats = 1

        for rep in range(numRepeats):
            # if rep > 0:
            #     print("REP: ", rep)
            rowcount = print_patt_instr(pattName, intSub, rowcount, chart_degrees)

        pattRowsPrinted = rowcount - startCnt
        if pattRowsPrinted < repeat:
            # Print some more rows
            print("----Here's some missing: ", repeat - pattRowsPrinted)
            missingRows = repeat - pattRowsPrinted
            rowcount = print_missing_rows(pattName, intSub, rowcount, missingRows, chart_degrees)

    else:
        print(mult_add, " Repeat ", pattName, " ", intSub, " times, filling in ", fillerSts, " extra sts")
    return rowcount


'''
def fitRepeatsToRowWidth(pattName, rowWidth, rowcount, repeat, chart_degrees):
    mult_add = constants.PATTERN_MULT_ADD[pattName]
    #print(pattName, " ", mult_add)
    # subtract add from rowWidth
    add_ = mult_add[1]
    # Figure out how many times to repeat the stitch
    divideMultsOver = rowWidth - add_
    mult_ = mult_add[0]
    intSub = divideMultsOver // mult_
    # Figure out if we need to add some filler stitches because it wont fit
    fillerSts = rowWidth - intSub*mult_ + add_

    startCnt = rowcount

    if pattName in putil.PATTERN_INSTRUCTIONS:
        print("...Work ", pattName, ", filling in ", fillerSts, " extra sts", " as:")
        if constants.PATTERN_ROWS[pattName] < repeat: # Repeat the pattern repeat/#rows
            #print(constants.PATTERN_ROWS[pattName], " ", repeat)
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
            #print("----Here's some missing: ", repeat - pattRowsPrinted)
            missingRows = repeat - pattRowsPrinted
            rowcount = printMissingRows(pattName, intSub, rowcount, missingRows, chart_degrees)

    else:
        print(mult_add, " Repeat ", pattName, " ", intSub, " times, filling in ", fillerSts, " extra sts")
    return rowcount
    '''


def find_row_width_for_pattern():
    mul = get_mult_from_list(constants.PATTERN_MULT_ADD.values())
    # print("largest mult:", getLargest(mul))
    adl = get_add_from_list(constants.PATTERN_MULT_ADD.values())
    # print("largest add:", getLargest(adl))

    return get_largest(mul) + get_largest(adl)
