from enum import Enum


def get_aspect_intensity(name):
    for an_ai in AspectIntensity:
        if str(name) == str(an_ai.name):
            return an_ai
    return AspectIntensity.NONE


class AspectIntensity(Enum):
    CONJ = 5
    SEXTILE = 7
    SQUARE = -5
    TRINE = 8
    OPPOSITION = -10
    SEMISEXTILE = 3
    QUINCUNX = -2
    SEMISQUARE = -3
    BIQUINTILE = 2
    QUINTILE = 1
    SESUISQUARE = -1
    NONE = 0


def determine_aspect_intensity(name):
    ai = get_aspect_intensity(name)
    if ai == AspectIntensity.NONE:
        print("............Couldn't find AspectIntensity for:", name)
    return ai.value
