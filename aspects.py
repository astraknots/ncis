#!/usr/bin/python

import sys, getopt
import translate
# import xlsxwriter
import constants
from itertools import groupby
from collections import Counter


def addSignAspectsForSpan(sign_degree_dict, rowNum, numRowsRepeat, rowAspects):
    '''Add additional aspects for patterns repeating over rows that cross signs, or sign aspects if none'''
    if len(rowAspects) == 0:
        rowAspects.append(constants.SIGN_ASPECT[sign_degree_dict[rowNum]])

    maxRow = getValidMaxRow(rowNum + numRowsRepeat)
    if sign_degree_dict[rowNum] != sign_degree_dict[maxRow]:
        rowAspects.append(constants.SIGN_ASPECT[sign_degree_dict[maxRow]])
    # TODO: If the numRowsRepeat > 30, get the sign in the middle too
    return rowAspects


def getValidMaxRow(maxRow):
    if maxRow > 360:
        maxRow -= 360
    return maxRow


def getAspectOrb(aspect, planet):
    if planet in constants.BIG_THREE:
        asp_orb = constants.ORBS['BIG3']
    else:
        asp_orb = constants.ORBS[aspect]
    return asp_orb


def get_aspect_score(aspect):
    score = constants.ASPECT_WEIGHTS[aspect]
    return score

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

    # print(" -- Try narrowByNumAspectsMultPlusAdd on", possPatts)
    nextList3 = narrowByNumAspectsMultPlusAdd(numAspects, possPatts)
    isBest = pickIfOnePattern(nextList3)
    if isBest not in ['None', 'Nope']:
        ##print("..Found best pattern by narrowing by numAspects to mult+add ", isBest)
        return [isBest]
    elif isBest not in ['None']:
        # Try to narrow by mod
        # print(" -- Try (1) narrowByNumAspectsMod on", nextList3)
        nextList5 = narrowByNumAspectsMod(numAspects, nextList3)
        isBest = pickIfOnePattern(nextList5)
        if isBest not in ['None', 'Nope']:
            ##print("..Found best pattern by narrowing by numAspects to mult+add then mod of add ", isBest)
            return [isBest]
        elif isBest not in ['None']:
            # Try if the mult or add matches numAspects
            # print(" -- Try narrowByNumAspectsMatchAdd on", nextList5)
            nextList4 = narrowByNumAspectsMatchAdd(numAspects, nextList5)
            isBest = pickIfOnePattern(nextList4)
            if isBest not in ['None', 'Nope']:
                ##print("..Found best pattern by narrowing by numAspects eq add/mult", isBest)
                return [isBest]
            # elif isBest not in ['None']:
            # print(" -- Unable to narrow ", nextList5, " narrowByNumAspectsMatchAdd (1)")
    else:
        # print(" -- Try (2) narrowByNumAspectsMod on", possPatts)
        nextList4 = narrowByNumAspectsMod(numAspects, possPatts)
        isBest = pickIfOnePattern(nextList4)
        if isBest not in ['None', 'Nope']:
            ##print("..Found best pattern by narrowing by numAspects to mod of add/mult ", isBest)
            return [isBest]
        elif isBest not in ['None']:
            # print(" -- Try narrowByNumAspectsMatchAdd on", nextList4)
            nextList5 = narrowByNumAspectsMatchAdd(numAspects, nextList4)
            isBest = pickIfOnePattern(nextList5)
            if isBest not in ['None', 'Nope']:
                ##print("..Found best pattern by narrowing by numAspects eq add/mult", isBest)
                return [isBest]
            # elif isBest not in ['None']:
            # print(" -- Unable to narrow ", nextList5, " narrowByNumAspectsMatchAdd")
        else:
            ##print(" -- Try (2) narrowByNumAspectsMatchAdd on", possPatts)
            nextList5 = narrowByNumAspectsMatchAdd(numAspects, possPatts)
            isBest = pickIfOnePattern(nextList5)
            if isBest not in ['None', 'Nope']:
                ##print("..Found best pattern by narrowing by numAspects eq add/mult (2)", isBest)
                return [isBest]
            # elif isBest not in ['None']:
            # print(" -- Unable to narrow ", nextList5, " narrowByNumAspectsMatchAdd (2)")

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
                trymod = mult + add
                ##print("2: trymod ", trymod)
                if numAspects >= trymod:
                    ##print("2: mult", mult, "add", add, "numAspects % trymod", numAspects % trymod)
                    if numAspects % trymod == 0 and patt not in narrowAspNum:
                        narrowAspNum.append(patt)
                else:
                    ##print("2: mult", mult, "add", add, "trymod % numAspects ", trymod % numAspects)
                    if trymod % numAspects == 0 and patt not in narrowAspNum:
                        narrowAspNum.append(patt)
            # else:
            ##print("NarrowAspNum=", narrowAspNum)
    return narrowAspNum


def getFirstNonZero(trylist):
    for a in trylist:
        if a > 0:
            return a


def getAspectsForDegree(orbs_by_planet, d, sign_for_degree):
    aspect_list = []

    # Add aspects for planet orbs
    for planet in constants.PLANETS:
        asps = orbs_by_planet[planet]
        for aspect in constants.ASPECTS:
            deg_range = asps[aspect]
            if isDegInRange(d, deg_range):
                aspect_list.append(aspect)

    # Add aspect for sign
    aspect_for_sign = constants.SIGN_ASPECT[sign_for_degree]
    aspect_list.append(aspect_for_sign)
    return aspect_list


def isDegInRange(deg, rang):
    return rang[0] <= deg <= rang[1]


def adjustDegFor360(degree):
    adj_degree = degree
    if degree > constants.MAX_CHART_DEGREES:
        adj_degree = degree - constants.MAX_CHART_DEGREES
    elif degree < constants.MIN_CHART_DEGREES:
        adj_degree = degree + constants.MAX_CHART_DEGREES
    return adj_degree
