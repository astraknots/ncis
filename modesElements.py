#!/usr/bin/python

import constants
import patterns


def narrowPatternsByModesElements(possPatts, sign1, sign2):
    narrowedPatts = narrowedPatts2 = narrowedPatts3 = narrowedPatts4 = narrowedPatts5 = narrowedPatts6 = narrowedPatts7 = []
    modes = getModesForSigns(sign1, sign2)
    elements = getElementsForSigns(sign1, sign2)

    # Try to narrow by mode, element to mult, add (permutations) but exact
    narrowedPatts = narrowPattsByMode(modes, possPatts)
    isBest = patterns.pickIfOnePattern(narrowedPatts)
    if isBest not in ['None', 'Nope']:
        ##print("..Matched best patt by mode:", isBest)
        return [isBest]
    elif isBest not in ['None']:
        # Narrowing by modes produced multiple matches
        narrowedPatts2 = narrowPattsByElement(elements, narrowedPatts)
        isBest = patterns.pickIfOnePattern(narrowedPatts2)
        if isBest not in ['None', 'Nope']:
            ##print("..Matched best patt by mode/element:", isBest)
            return [isBest]
    else:
        # Narrowing by modes produced no matches, try just by element
        narrowedPatts3 = narrowPattsByElement(elements, possPatts)
        isBest = patterns.pickIfOnePattern(narrowedPatts3)
        if isBest not in ['None', 'Nope']:
            ##print("..Matched best patt by element:", isBest)
            return [isBest]

    # Try to narrow by mode, element to mult, add (permutations) with multiples
    narrowedPatts4 = narrowPattsByModeMult(modes, possPatts)
    isBest = patterns.pickIfOnePattern(narrowedPatts4)
    if isBest not in ['None', 'Nope']:
        ##print("..Matched best patt by mode mult:", isBest)
        return [isBest]
    elif isBest not in ['None']:
        # Narrowing by modes mult produced multiple matches
        narrowedPatts5 = narrowPattsByElementMult(elements, narrowedPatts4)
        isBest = patterns.pickIfOnePattern(narrowedPatts5)
        if isBest not in ['None', 'Nope']:
            ##print("..Matched best patt by mode/element mult:", isBest)
            return [isBest]
    else:
        # Narrowing by modes mult produced no matches, try element mult
        narrowedPatts6 = narrowPattsByElement(elements, possPatts)
        isBest = patterns.pickIfOnePattern(narrowedPatts6)
        if isBest not in ['None', 'Nope']:
            ##print("..Matched best patt by element mult:", isBest)
            return [isBest]

   # print("1:", narrowedPatts, "2:", narrowedPatts2, "3:", narrowedPatts3, "4:", narrowedPatts4, "5:",
    #          narrowedPatts5, "6:", narrowedPatts6)

    # Pick the smallest narrowed so far, if that's empty, then all
    nextList = pickShortestNonEmptyList([narrowedPatts, narrowedPatts2, narrowedPatts3, narrowedPatts4, narrowedPatts5, narrowedPatts6], possPatts)
    #print("next list:", nextList)

    # Try the multxadd = an element or mode score
    #print(" -- Try narrowPattsByAddMult on", nextList)
    narrowedPatts7 = narrowPattsByAddMultElementFirst(modes, elements, nextList)
    isBest = patterns.pickIfOnePattern(narrowedPatts7)
    if isBest not in ['None', 'Nope']:
        ##print("..Matched best patt by addxmult = mode/element score:", isBest)
        return [isBest]
    elif isBest not in ['None']:
        narrowedPatts8 = narrowPattsByAddMultModeFirst(modes, elements, narrowedPatts7)
        isBest = patterns.pickIfOnePattern(narrowedPatts8)
        if isBest not in ['None', 'Nope']:
            ##print("..Matched best patt by addxmult(2) = mode/element score:", isBest)
            return [isBest]
    else:
        narrowedPatts8 = narrowPattsByAddMultModeFirst(modes, elements, nextList)
        isBest = patterns.pickIfOnePattern(narrowedPatts8)
        if isBest not in ['None', 'Nope']:
            ##print("..Matched best patt by addxmult(3) = mode/element score:", isBest)
            return [isBest]

    # Go by just the scores of this sign's mode and element
    #print(" -- Try narrowBySignScore on", narrowedPatts7)
    nextList2 = narrowBySignScore(sign1, sign2, narrowedPatts7)
    isBest = patterns.pickIfOnePattern(nextList2)
    if isBest not in ['None', 'Nope']:
        return [isBest]

    return nextList2

def narrowPattsByAddMultModeFirst(modes, elements, possPatts):
    narrowed_patts = []
    scores = []

    for mode in modes:
        scores.extend(constants.MODE_SCORES[mode])
        narrowed_patts.extend(narrowPattsByScoresMultAdd(scores, possPatts))

    if len(narrowed_patts) == 0:
        for element in elements:
            scores.extend(constants.ELEMENT_SCORES[element])
        #print("scores:", scores, " on ", possPatts)
        narrowed_patts.extend(narrowPattsByScoresMultAdd(scores, possPatts))

    return narrowed_patts

def narrowPattsByAddMultElementFirst(modes, elements, possPatts):
    narrowed_patts = []
    scores = []
    for element in elements:
        scores.extend(constants.ELEMENT_SCORES[element])
        narrowed_patts.extend(narrowPattsByScoresMultAdd(scores, possPatts))

    if len(narrowed_patts) == 0:
        for mode in modes:
            scores.extend(constants.MODE_SCORES[mode])
        #print("scores:", scores, " on ", possPatts)
        narrowed_patts.extend(narrowPattsByScoresMultAdd(scores, possPatts))

    return narrowed_patts


def narrowBySignScore(sign1, sign2, nextList):
    narrowed_list = narrowed_list2 = narrowed_list3 = narrowed_list4 = []
    score1 = constants.SIGN_SCORE[sign1]
    score2 = constants.SIGN_SCORE[sign2]
    #print("score1 ", score1, " score2", score2)

    # Try to narrow by mult match score
    for patt in nextList:
        mult = constants.PATTERN_MULT_ADD[patt][0]
        if (mult == score1 or mult == score2) and patt not in narrowed_list:
            narrowed_list.append(patt)

    isBest = patterns.pickIfOnePattern(narrowed_list)
    if isBest not in ['None', 'Nope']:
        ##print("..Picked pattern:", isBest, " based on mult matching sign score")
        return [isBest]
    elif isBest not in ['None']:
        # continue to narrow, use mods
        for patt in narrowed_list:
            mult = constants.PATTERN_MULT_ADD[patt][0]
            if (mult % score1 == 0 or mult % score2 == 0) and patt not in narrowed_list2:
                narrowed_list2.append(patt)

        isBest = patterns.pickIfOnePattern(narrowed_list2)
        if isBest not in ['None', 'Nope']:
            ##print("..Picked pattern:", isBest, " based on mult matching sign score and mod")
            return [isBest]
        #elif isBest not in ['None']:
            #print("--For mult match sign (w mod) got", narrowed_list2, " from ", narrowed_list)

    for patt in nextList:
        adds = constants.PATTERN_MULT_ADD[patt][1]
        if (adds == score1 or adds == score2) and patt not in narrowed_list3:
            narrowed_list3.append(patt)

    isBest = patterns.pickIfOnePattern(narrowed_list3)
    if isBest not in ['None', 'Nope']:
        ##print("..Picked pattern:", isBest, " based on adds matching sign score")
        return [isBest]
    elif isBest not in ['None']:
        # continue to narrow, use mods
        for patt in narrowed_list3:
            adds = constants.PATTERN_MULT_ADD[patt][1]
            if (adds % score1 == 0 or adds % score2 == 0) and patt not in narrowed_list4:
                narrowed_list4.append(patt)

        isBest = patterns.pickIfOnePattern(narrowed_list4)
        if isBest not in ['None', 'Nope']:
            ##print("..Picked pattern:", isBest, " based on add matching sign score and mod")
            return [isBest]
        elif isBest not in ['None']:
            #print("--For add match sign (w mod) got", narrowed_list4, " from ", narrowed_list3)
            #print("still nada", narrowed_list4)
            for patt in narrowed_list4:
                print(patt, ":", constants.PATTERN_MULT_ADD[patt][0], "-", constants.PATTERN_MULT_ADD[patt][1])
            return narrowed_list4
        else:
            #print("still nada", narrowed_list3)
            for patt in narrowed_list3:
                print(patt, ":", constants.PATTERN_MULT_ADD[patt][0], "-", constants.PATTERN_MULT_ADD[patt][1])
            return narrowed_list3

    return ''

def pickShortestNonEmptyList(listOflists, allPoss):
    shortest = len(allPoss)
    slist = allPoss
    #print("allPoss len", shortest)
    for alist in listOflists:
        if len(alist) < shortest and len(alist) > 0:
            shortest = len(alist)
            slist = alist
    #print("shortest len", shortest, " list:", slist)
    return slist


def narrowPattsByScores(scores, possPatts):
    narrowed_patts = []
    for patt in possPatts:
        #print("patt ", patt)
        mult = constants.PATTERN_MULT_ADD[patt][0]
        adds = constants.PATTERN_MULT_ADD[patt][1]
        #print("mult ", mult, " add", adds)

        #print(" scores", scores)
        for score in scores:
            if mult == score and patt not in narrowed_patts:
                narrowed_patts.append(patt)
            elif adds == score and patt not in narrowed_patts:
                narrowed_patts.append(patt)
    #print("narrowPattsByScores=", narrowed_patts)
    return narrowed_patts

def narrowPattsByScoresMultAdd(scores, possPatts):
    narrowed_patts = []
    for patt in possPatts:
        ##print("patt ", patt)
        mult = constants.PATTERN_MULT_ADD[patt][0]
        adds = constants.PATTERN_MULT_ADD[patt][1]
        ##print("mult ", mult, " add", adds)

        ##print(" scores", scores, "mult * adds ", mult * adds)
        for score in scores:
            if mult * adds == score and patt not in narrowed_patts:
                narrowed_patts.append(patt)
    #print("narrowPattsByScores=", narrowed_patts)
    return narrowed_patts


def narrowPattsByScoresMult(scores, possPatts):
    narrowed_patts = []
    for patt in possPatts:
        #print("patt ", patt)
        mult = constants.PATTERN_MULT_ADD[patt][0]
        adds = constants.PATTERN_MULT_ADD[patt][1]
        #print("mult ", mult, " add", adds)

        #print(" scores", scores)
        for score in scores:
            #print("mult % score ", mult % score, " adds % score ", adds % score)
            if mult % score == 0 and patt not in narrowed_patts:
                narrowed_patts.append(patt)
            elif adds % score == 0 and patt not in narrowed_patts:
                narrowed_patts.append(patt)
    #print("narrowPattsByScoresMult=", narrowed_patts)
    return narrowed_patts

def narrowPattsByElement(elements, possPatts):
    narrowed_patts = []
    for element in elements:
        scores = constants.ELEMENT_SCORES[element]
        narrowed_patts.extend(narrowPattsByScores(scores, possPatts))
    #print("narrowPattsByElement=", narrowed_patts)
    return narrowed_patts

def narrowPattsByMode(modes, possPatts):
    narrowed_patts = []
    for mode in modes:
        scores = constants.MODE_SCORES[mode]
        narrowed_patts.extend(narrowPattsByScores(scores, possPatts))
    #print("narrowPattsByMode=", narrowed_patts)
    return narrowed_patts

def narrowPattsByElementMult(elements, possPatts):
    narrowed_patts = []
    for element in elements:
        scores = constants.ELEMENT_SCORES[element]
        narrowed_patts.extend(narrowPattsByScoresMult(scores, possPatts))

    return narrowed_patts

def narrowPattsByModeMult(modes, possPatts):
    narrowed_patts = []
    for mode in modes:
        scores = constants.MODE_SCORES[mode]
        narrowed_patts.extend(narrowPattsByScoresMult(scores, possPatts))

    return narrowed_patts

def getModesForSigns(sign1, sign2):
    modes = [constants.SIGN_MODE[sign1]]
    if constants.SIGN_MODE[sign2] not in modes:
        modes.append(constants.SIGN_MODE[sign2])
    ##print("modes ", modes)
    #for mode in modes:
       # print("mode score:", constants.MODE_SCORES[mode])

    return modes

def getElementsForSigns(sign1, sign2):
    elements = [constants.SIGN_ELEMENT[sign1]]
    if constants.SIGN_ELEMENT[sign2] not in elements:
        elements.append(constants.SIGN_ELEMENT[sign2])
    ##print("elements ", elements)
    #for element in elements:
       # print("element score:", constants.ELEMENT_SCORES[element])

    return elements