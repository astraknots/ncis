#!/usr/bin/python

import sys, getopt
import translate, calculateOrbs
#import xlsxwriter
import constants, aspects, shapes, modesElements
from itertools import groupby
from collections import Counter

def addPossPatternsForSpan(sign_degree_dict, rowNum, numRowsRepeat, possPatterns):
    '''Add potential patterns for span by sign aspects'''
    #For now only add possibles if there aren't any
    if len(possPatterns) == 0:
        rowAspects = aspects.addSignAspectsForSpan(sign_degree_dict, rowNum, numRowsRepeat, [])
        possPatterns = getPatternsForAspectShapes(rowAspects)
        return possPatterns
    else:
        return possPatterns

def getPatternsForAspectShapes(aspects):
    poss_shapes = []
    for asp in aspects:
        #print("asp:", asp, "add:", constants.PATTERN_ASPECT_SHAPES[asp])
        for ashape in constants.PATTERN_ASPECT_SHAPES[asp]:
            poss_shapes.append(ashape)
    #print("poss shapes:", poss_shapes, " for aspects:", aspects)

    poss_patts = []
    for patt in constants.PATTERN_SHAPES:
        match_shapes = constants.PATTERN_SHAPES[patt]
        for shp in match_shapes:
            for pshp in poss_shapes:
                if shp == pshp:
                    if patt not in poss_patts:
                        poss_patts.append(patt)
    #print("poss patts:", poss_patts, " for aspects:", aspects)

    somePatts = shapes.determineBestPatternsForShapeMatch(poss_patts, aspects)

    return getJustPatternNames(somePatts)

def determineBestPatternBySomething(possPatts, numRowsRepeat, rowNum, sign_degree_dict, rowAspects):
    ##print("This row ", rowNum, " repeats ", numRowsRepeat)
    bestPatt = ''

    if type(possPatts[0]) is list:
        #1. First narrow by score, but only if they got scored
        narrowedByScorePatts = narrowPatternsByScore(possPatts)
        isBest = pickIfOnePattern(narrowedByScorePatts)
        if isBest not in ['None', 'Nope']:
            ##print("..Found best pattern by narrowing score ", isBest)
            return isBest
        ''' This shouldn't happen
        elif isBest in ['None']:
            print("---Score killed all options!")'''
    else:
        narrowedByScorePatts = possPatts

    # Let's look at the mult-add as it relates to the element and mode of this degree
    maxRow = aspects.getValidMaxRow(rowNum + numRowsRepeat)
    print(sign_degree_dict[rowNum], "-", sign_degree_dict[maxRow])

    narrowedByModeElements = modesElements.narrowPatternsByModesElements(narrowedByScorePatts, sign_degree_dict[rowNum], sign_degree_dict[maxRow])

    isBest = pickIfOnePattern(narrowedByModeElements)
    if isBest not in ['None', 'Nope']:
        ##print("..Found best pattern by narrowing by modes/elements ", isBest)
        return isBest
    elif isBest not in ['None']:
        narrowedByNumAspects = aspects.narrowByNumAspectStuff(narrowedByModeElements, rowAspects)
        isBest = pickIfOnePattern(narrowedByNumAspects)
        if isBest not in ['None', 'Nope']:
            ##print("...Found best pattern by narrowing by numAspects ", isBest)
            return isBest
        elif isBest not in ['None']:
            #print("Couldn't narrow by num aspects (1)", narrowedByNumAspects)
            #print("Forcing match:", narrowedByNumAspects)
            bestPatt = forceRankPatternMatch(narrowedByNumAspects, sign_degree_dict[rowNum])
        else:
            #print("Forcing match (1):", narrowedByModeElements)
            bestPatt = forceRankPatternMatch(narrowedByModeElements, sign_degree_dict[rowNum])
    else:
        #print("No match when narrow by mode/element", narrowedByModeElements)
        narrowedByNumAspects = aspects.narrowByNumAspectStuff(narrowedByScorePatts, rowAspects)
        isBest = pickIfOnePattern(narrowedByNumAspects)
        if isBest not in ['None', 'Nope']:
            ##print("...Found best pattern by narrowing narrowedByScorePatts by numAspects ", isBest)
            return isBest
        elif isBest not in ['None']:
            #print("Couldn't narrow by num aspects", narrowedByNumAspects)
            #print("Forcing match:", narrowedByNumAspects)
            bestPatt = forceRankPatternMatch(narrowedByNumAspects, sign_degree_dict[rowNum])
        else:
            #print("Forcing match:", narrowedByScorePatts)
            bestPatt = forceRankPatternMatch(narrowedByScorePatts, sign_degree_dict[rowNum])

    return bestPatt

def subtractFromLarger(v1, v2):
    if v1 > v2:
        return v1 - v2
    else:
        return v2 - v1

def forceRankPatternMatch(possPatts, signAtRowNum):
    # Choose the pattern with the (mult+add) closest to the signAtRowNum score
    meetScore = constants.SIGN_SCORE[signAtRowNum]
    ##print("meetScore:", meetScore)
    bestPatts = []
    closeCnt = 0
    for patt in possPatts:
        mult = constants.PATTERN_MULT_ADD[patt][0]
        add = constants.PATTERN_MULT_ADD[patt][1]
        totCnt = mult + add
        compareCnt = subtractFromLarger(meetScore, totCnt)
        ##print("patt", patt, "totCnt:", totCnt, " closeCnt:", closeCnt, " bestPatts:", bestPatts, "compareCnt", compareCnt)
        if compareCnt < closeCnt or len(bestPatts) == 0:
            bestPatts.append(patt)
            closeCnt = compareCnt

    if len(bestPatts) > 1:
        #Choose the pattern with the highest stitch count mult and add, added tog
        maxCnt = 0
        bestPatt = ''
        for patt in possPatts:
            mult = constants.PATTERN_MULT_ADD[patt][0]
            add = constants.PATTERN_MULT_ADD[patt][1]
            totCnt = mult + add
            if totCnt > maxCnt:
                bestPatt = patt
                maxCnt = totCnt
    else:
        bestPatt = bestPatts[0]

    ##print("..Forcing match chose:", bestPatt)
    return bestPatt


def determineHighScore(possPatts):
    bestScore = 0
    for score, patt in possPatts:
        escore = eval(score)
        if escore > bestScore:
            bestScore = escore
    #print("Best score:", bestScore)
    return bestScore

def narrowPatternsByScore(possPatts):
    narrowedPatts = []
    highScore = determineHighScore(possPatts)
    for score, patt in possPatts:
        #print("score:", eval(score), " for patt", patt)
        if eval(score) >= highScore:
            narrowedPatts.append(patt)
    return narrowedPatts

def pickIfOnePattern(bestPatts):
    if len(bestPatts) == 1:
        #print("...picking best patt:", bestPatts[0], type(bestPatts), type(bestPatts[0]))
        if type(bestPatts[0]) is list:
            return bestPatts[0][1]
        else:
            return bestPatts[0]
    elif len(bestPatts) == 0:
        return 'None'
    else:
        return 'Nope'

def getJustPatternNames(scoredPatts):
    justPatts = []
    for patt in scoredPatts:
        justPatts.append(patt[1])
    return justPatts


def getPatternsForRowCount(grouped_byAspect):
    possible_patterns = []
    for aspList, cnt in grouped_byAspect:
        possible_patterns.append([aspList, cnt, getPatternsForCnt(cnt)])
    return possible_patterns


def getPatternsForRowCountExpand(grouped_byAspect):
    possible_patterns = []
    for aspList, cnt in grouped_byAspect:
        possible_patterns.append([aspList, cnt, getPatternsForCntExpand(cnt)])
    return possible_patterns


def getPatternsForMaxRowCount(grouped_byAspect):
    possible_patterns = []
    for aspList, cnt in grouped_byAspect:
        possible_patterns.append([aspList, cnt, getPatternsForCntMaxExpand(cnt)])
    return possible_patterns


def getPatternsForCnt(cnt):
    poss_pats = []
    for pat in constants.PATTERN_ROWS:
        # print(pat, constants.PATTERN_ROWS[pat])
        if constants.PATTERN_ROWS[pat] == cnt:
            poss_pats.append(pat)
    return poss_pats

def getPatternsMatchingRows(possPatts, numRows):
    matches = []
    for pat in possPatts:
        if constants.PATTERN_ROWS[pat] == numRows:
            matches.append(pat)
    return matches

def getPatternsForCntExpand(cnt):
    poss_pats = []
    for pat in constants.PATTERN_ROWS:
        # print(pat, constants.PATTERN_ROWS[pat])
        if constants.PATTERN_ROWS[pat] == cnt:
            # Add all patterns that repeat over this exact #of rows
            poss_pats.append(pat)
        elif cnt > 1 and constants.PATTERN_ROWS[pat] % cnt == 0:
            # Add all patterns that repeat over multiple of this #of rows, can be repeated
            poss_pats.append(pat)
        elif constants.PATTERN_ROWS[pat] == 1:
            # Add all patterns that are only over a single row, since they can be repeated
            poss_pats.append(pat)
    return poss_pats


def getPatternsForCntMaxExpand(cnt):
    poss_pats = []
    for pat in constants.PATTERN_ROWS:
        # print(pat, constants.PATTERN_ROWS[pat])
        if constants.PATTERN_ROWS[pat] == cnt:
            # Add all patterns that repeat over this exact #of rows
            poss_pats.append(pat)
        elif cnt > 1 and constants.PATTERN_ROWS[pat] % cnt == 0:
            # Add all patterns that repeat over multiple of this #of rows, can be repeated
            poss_pats.append(pat)
        elif constants.PATTERN_ROWS[pat] == 1:
            # Add all patterns that are only over a single row, since they can be repeated
            poss_pats.append(pat)
        elif constants.PATTERN_ROWS[pat] < cnt:
            # Add all patterns that are less than this total #of rows, would be partial but possibly better shape match
            poss_pats.append(pat)
    return poss_pats



