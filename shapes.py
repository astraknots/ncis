#!/usr/bin/python

import constants


def determineMatchScore(pattShapes, aspects):
    matchScore = 0
    for asp in aspects:
        #print("Aspect shapes:", constants.PATTERN_ASPECT_SHAPES[asp])
        for shape in pattShapes:
            # print("Shape:", shape)
            if shape in constants.PATTERN_ASPECT_SHAPES[asp]:
                # print("******Shape Match!:", shape, constants.PATTERN_ASPECT_SHAPES[asp])
                matchScore += 1

    return matchScore

def determineBestPatternsForShapeMatch(possPatterns, aspects):
    best_patterns = []
    # print("Determining best pattern for:", str(len(possPatterns)), "poss patterns ", str(len(aspects)), " aspects")
    bestPatt = ''
    maxMatchScore = 0

    for patt in possPatterns:
        #print(">>>>>>>", constants.PATTERN_SHAPES[patt])
        ms = determineMatchScore(constants.PATTERN_SHAPES[patt], aspects)
        if ms > 0 and ms >= maxMatchScore:
            # print("....................replacing bestPatt:", bestPatt, " with:", patt, " for higher score:", ms, " > ", maxMatchScore)
            bestPatt = patt
            maxMatchScore = ms
            best_patterns.append([str(ms) + "/" + str(len(aspects)), patt])

    #bestPatt = cullBestPatterns(best_patterns, aspects, 0)
    # print("Leaving determineBestPatternForShapeMatch with bestPatt =", bestPatt)
    return best_patterns

