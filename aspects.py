#!/usr/bin/python

import constants
import astrology_signs as signs
import astrology_aspects as aspects
import astrology_planets as planets
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def add_sign_aspects_for_span(sign_degree_dict, row_num, num_rows_repeat, row_aspects):
    """Add aspects for sign to list if there are no row aspects, """
    """Add additional aspects for patterns repeating over rows that cross signs, and sign aspects if no row aspects"""
    # If there are no aspects for this row, add the aspects associated with the sign of this row
    if len(row_aspects) == 0:
        logging.debug("sign_degree_dict[row_num]:")
        logging.debug(sign_degree_dict[row_num])
        row_aspects.append(aspects.get_aspect_by_name(sign_degree_dict[row_num].aspect))

    #
    max_row = aspects.adjust_degree_for_360(row_num + num_rows_repeat)
    if sign_degree_dict[row_num] != sign_degree_dict[max_row]:
        logging.debug("sign_degree_dict[max_row]:" + str(max_row))
        logging.debug(sign_degree_dict[max_row])
        row_aspects.append(aspects.get_aspect_by_name(sign_degree_dict[max_row].aspect))

    # TODO: If the numRowsRepeat > 30, get the sign in the middle too
    if num_rows_repeat > 30:
        logging.warning("Consider getting sign in the middle since this repeats over 30 rows")

    return row_aspects


def pickIfOnePattern(bestPatts):
    if len(bestPatts) == 1:
        ##print("...picking best patt:", bestPatts[0], type(bestPatts), type(bestPatts[0]))
        if type(bestPatts[0]) is list:
            return bestPatts[0][1]
        else:
            return bestPatts[0]
    elif len(bestPatts) == 0:
        return 'None'
    else:
        return 'Nope'


def narrowByNumAspectStuff(possPatts, rowAspects):
    nextList3 = nextList4 = nextList5 = []

    # Try to pick based on numAspects closest to add as tie-breaker
    numAspects = len(rowAspects)

    #print(" -- Try narrowByNumAspectsMultPlusAdd on", possPatts)
    nextList3 = narrowByNumAspectsMultPlusAdd(numAspects, possPatts)
    isBest = pickIfOnePattern(nextList3)
    if isBest not in ['None', 'Nope']:
        ##print("..Found best pattern by narrowing by numAspects to mult+add ", isBest)
        return [isBest]
    elif isBest not in ['None']:
        # Try to narrow by mod
        #print(" -- Try (1) narrowByNumAspectsMod on", nextList3)
        nextList5 = narrowByNumAspectsMod(numAspects, nextList3)
        isBest = pickIfOnePattern(nextList5)
        if isBest not in ['None', 'Nope']:
            ##print("..Found best pattern by narrowing by numAspects to mult+add then mod of add ", isBest)
            return [isBest]
        elif isBest not in ['None']:
            # Try if the mult or add matches numAspects
            #print(" -- Try narrowByNumAspectsMatchAdd on", nextList5)
            nextList4 = narrowByNumAspectsMatchAdd(numAspects, nextList5)
            isBest = pickIfOnePattern(nextList4)
            if isBest not in ['None', 'Nope']:
                ##print("..Found best pattern by narrowing by numAspects eq add/mult", isBest)
                return [isBest]
            #elif isBest not in ['None']:
                #print(" -- Unable to narrow ", nextList5, " narrowByNumAspectsMatchAdd (1)")
    else:
        #print(" -- Try (2) narrowByNumAspectsMod on", possPatts)
        nextList4 = narrowByNumAspectsMod(numAspects, possPatts)
        isBest = pickIfOnePattern(nextList4)
        if isBest not in ['None', 'Nope']:
            ##print("..Found best pattern by narrowing by numAspects to mod of add/mult ", isBest)
            return [isBest]
        elif isBest not in ['None']:
            #print(" -- Try narrowByNumAspectsMatchAdd on", nextList4)
            nextList5 = narrowByNumAspectsMatchAdd(numAspects, nextList4)
            isBest = pickIfOnePattern(nextList5)
            if isBest not in ['None', 'Nope']:
                ##print("..Found best pattern by narrowing by numAspects eq add/mult", isBest)
                return [isBest]
            #elif isBest not in ['None']:
                #print(" -- Unable to narrow ", nextList5, " narrowByNumAspectsMatchAdd")
        else:
            ##print(" -- Try (2) narrowByNumAspectsMatchAdd on", possPatts)
            nextList5 = narrowByNumAspectsMatchAdd(numAspects, possPatts)
            isBest = pickIfOnePattern(nextList5)
            if isBest not in ['None', 'Nope']:
                ##print("..Found best pattern by narrowing by numAspects eq add/mult (2)", isBest)
                return [isBest]
            #elif isBest not in ['None']:
                #print(" -- Unable to narrow ", nextList5, " narrowByNumAspectsMatchAdd (2)")


    return nextList4


def narrowByNumAspectsMultPlusAdd(numAspects, possPatts):
    # Try to pick based on numAspects closest to mult+add as tie-breaker
    narrowAspNum = []
    ##print("numAspects:", numAspects, " pats:", possPatts)
    for patt in possPatts:
        mult = constants.PATTERN_MULT_ADD[patt][0]
        add = constants.PATTERN_MULT_ADD[patt][1]
        multAdd = mult + add
        ##print("mult+add", multAdd)
        if multAdd == numAspects and patt not in narrowAspNum:
            narrowAspNum.append(patt)

    return narrowAspNum

def narrowByNumAspectsMatchAdd(numAspects, possPatts):
    narrowAspNum = []
    ##print("match add numAspects:", numAspects, " pats:", possPatts)
    for patt in possPatts:
        mult = constants.PATTERN_MULT_ADD[patt][0]
        add = constants.PATTERN_MULT_ADD[patt][1]
        ##print("mult", mult, "add", add)
        if add == numAspects and patt not in narrowAspNum:
            narrowAspNum.append(patt)
        elif mult == numAspects and patt not in narrowAspNum:
            narrowAspNum.append(patt)
    return narrowAspNum

def narrowByNumAspectsMod(numAspects, possPatts):
    # Try to pick based on numAspects closest to mult+add as tie-breaker
    narrowAspNum = []
    ##print("numAspects:", numAspects, " pats:", possPatts)
    for patt in possPatts:
        mult = constants.PATTERN_MULT_ADD[patt][0]
        add = constants.PATTERN_MULT_ADD[patt][1]
        ##print("patt ", patt, " mult ", mult, "add ", add)
        if add > 0 and mult > 0:
            trymod = getFirstNonZero([add, mult])
            ##print("trymod ", trymod)
            if numAspects >= trymod:
                ##print("mult", mult, "add", add, "numAspects % trymod", numAspects % trymod)
                if numAspects % trymod == 0 and patt not in narrowAspNum:
                    narrowAspNum.append(patt)
            else:
                ##print("mult", mult, "add", add, "trymod % numAspects ", trymod % numAspects)
                if trymod % numAspects == 0 and patt not in narrowAspNum:
                    narrowAspNum.append(patt)
            if len(narrowAspNum) == 0:
                trymod = mult+add
                ##print("2: trymod ", trymod)
                if numAspects >= trymod:
                    ##print("2: mult", mult, "add", add, "numAspects % trymod", numAspects % trymod)
                    if numAspects % trymod == 0 and patt not in narrowAspNum:
                        narrowAspNum.append(patt)
                else:
                    ##print("2: mult", mult, "add", add, "trymod % numAspects ", trymod % numAspects)
                    if trymod % numAspects == 0 and patt not in narrowAspNum:
                        narrowAspNum.append(patt)
            #else:
                ##print("NarrowAspNum=", narrowAspNum)
    return narrowAspNum


def getFirstNonZero(trylist):
    for a in trylist:
        if a > 0:
            return a


def get_aspects_for_degree(orbs_by_planet, d, sign_for_degree):
    '''Get list of aspects for a particular degree and the aspect for the sign at this degree'''
    aspect_list = []

    #Add aspects for planet orbs
    for planet in planets.THE_PLANETS:
        asps = orbs_by_planet[planet.name]
        for aspect in aspects.THE_ASPECTS:
            deg_range = asps[aspect.name]
            if aspects.is_degree_in_range(d, deg_range):
                aspect_list.append(aspect)


    #Add aspect for sign
    logging.debug("Sign for degree:")
    logging.debug(sign_for_degree)
    aspect_for_sign = aspects.get_aspect_by_name(sign_for_degree.aspect)
    logging.debug("aspect_for_sign:")
    logging.debug(aspect_for_sign)

    aspect_list.append(aspect_for_sign)
    return aspect_list

