#!/usr/bin/python
import constants

RULER = 'RULERSHIP'
EXAULT = 'EXHAULTED'
DETRMT = 'DETRIMENT'
FALL = 'FALL'
NO_DIG = 'NO_DIGNITY'

def get_planet_dignity(planet, sign):
    '''Return the dignity this planet has. If none, return NO_DIGNITY '''
    if planet == 'ASC':
        return None
    rulership = constants.PLANET_SIGN_RULERS[planet]
    exhaulted = constants.PLANET_SIGN_EXHAULTATION[planet]
    detriment = constants.PLANET_SIGN_DETRIMENT[planet]
    fall = constants.PLANET_SIGN_FALL[planet]
    if sign in rulership:
        return RULER
    elif sign in exhaulted:
        return EXAULT
    elif sign in detriment:
        return DETRMT
    elif sign in fall:
        return FALL
    else:
        return NO_DIG


def get_planet_dignity_score(planet, dignity, sign):
    '''Return the dignity score for this planet and dignity. NO_DIGNITY = 0'''
    if dignity == RULER:
        return 4
    elif dignity == DETRMT:
        return 2
    elif dignity == EXAULT:
        exhault_scores = constants.PLANET_EXHAULTATION_SCORES[planet]
        if isinstance(exhault_scores, int):
            return exhault_scores
        else:
            planets_exaults = constants.PLANET_SIGN_EXHAULTATION[planet]
            if planets_exaults[0] == sign:
                escore = exhault_scores[0]
            else:
                escore = exhault_scores[1]
            return escore
    elif dignity == FALL:
        fall_scores = constants.PLANET_FALL_SCORES[planet]
        if isinstance(fall_scores, int):
            return fall_scores
        else:
            planets_falls = constants.PLANET_SIGN_FALL[planet]
            if planets_falls[0] == sign:
                fscore = fall_scores[0]
            else:
                fscore = fall_scores[1]
            return fscore
    else:
        return 0


def get_planet_dignity_w_score(planet, sign):
    '''Return the dignity this planet has, along w the score of that dignity. If none, return NO_DIGNITY '''
    dignity = get_planet_dignity(planet, sign)
    if dignity == RULER:
        return dignity + ' 4'
    elif dignity == DETRMT:
        return dignity + ' 2'
    elif dignity == EXAULT:
        exhault_scores = constants.PLANET_EXHAULTATION_SCORES[planet]
        return dignity
    elif dignity == FALL:
        fall_scores = constants.PLANET_FALL_SCORES[planet]
        return dignity
    else:
        return NO_DIG


def get_printable_planet_dignities(planet_dignities, sign):
    if len(planet_dignities) <= 0:
        return ''
    printable_dig = ''
    for planet in constants.PLANETS:
        if planet in planet_dignities:
            dig = planet_dignities[planet]
            if dig:
                printable_dig += str(dig[sign][0]) + ' [' + str(dig[sign][1]) + ']'

    return printable_dig