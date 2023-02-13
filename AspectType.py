from enum import Enum

import constants


class AspectDirection(Enum):
    SEPARATING = -1
    APPLYING = 1
    EXACT = 0


class AspectName(Enum):
    CONJ = 'CONJ'
    SEMISEXTILE = 'SEMISEXTILE'
    SEXTILE = 'SEXTILE'
    SEMISQUARE = 'SEMISQUARE'
    SQUARE = 'SQUARE'
    TRINE = 'TRINE'
    QUINCUNX = 'QUINCUNX'
    OPPOSITION = 'OPPOSITION'
    BIQUINTILE = 'BIQUINTILE'
    QUINTILE = 'QUINTILE'
    SESQUISQUARE = 'SESQUISQUARE'


class AspectType:
    name = None
    orb = None  # The allowed orb for this aspect
    degree = None  # of 360 degrees or in range of 0-359, where 0=360 - the degree apart that forms this aspect
    direction = None  # applying or separating

    def __init__(self, name, orb, degree):
        if isinstance(name, AspectName):
            self.name = name.value
        else:
            self.name = name
        self.orb = orb
        self.degree = degree
        if degree > 180:
            self.direction = AspectDirection.SEPARATING
        elif degree == 0:
            self.direction = AspectDirection.EXACT
        else:
            self.direction = AspectDirection.APPLYING

    def get_str_rep(self):
        return f"{self.name} (orb:{self.orb}, degree:{self.degree}, cycle:{self.direction})"

    def __str__(self):
        return self.get_str_rep()

    def __repr__(self):
        return self.get_str_rep()


Conjunction = AspectType(AspectName.CONJ, 10, 0)
Semisextile = AspectType(AspectName.SEMISEXTILE, 2, 30)
Sextile = AspectType(AspectName.SEXTILE, 6, 60)
Semisquare = AspectType(AspectName.SEMISQUARE, 2, 45) # show tension but also challenges that can help us grow and learn. However, any conflicts felt are not as immediately apparent as they are in the case of the square, making it easier to avoid them and miss an opportunity for growth.
Quintile = AspectType(AspectName.QUINTILE, 1, 72) # a greater emphasis on the purposeful manifestation of one's talents, or making something of them; be they artistic, scientific, or demonstrations of one's personal power. Thus quintiles appear with some frequency in the charts of both artists and repressive political leaders. In each case they suggest talent plus the ambition to make something of it in the world.
Square = AspectType(AspectName.SQUARE, 8, 90)
Trine = AspectType(AspectName.TRINE, 8, 120)
Sesuisquare = AspectType(AspectName.SESQUISQUARE, 2, 135) # s tend to indicate a smouldering conflict that one would prefer to ignore. Any relief would then tend to be short-lived. Sesquiquadrates therefore tend to indicate themes of a long-term and stubborn nature.
Biquintile = AspectType(AspectName.BIQUINTILE, 1, 144) # Individuals with such an aspect between two planets are often only vaguely aware of it. However, if someone is sensitive enough it can aid in developing creative powers which can help to find original solutions and throw a positive light on issues that initially appear problematic.
Quincunx = AspectType(AspectName.QUINCUNX, 2, 150)
Opposition = AspectType(AspectName.OPPOSITION, 10, 180)
Quincunx_Sep = AspectType(AspectName.QUINCUNX, 2, 210)
Trine_Sep = AspectType(AspectName.TRINE, 8, 240)
Square_Sep = AspectType(AspectName.SQUARE, 8, 270)
Sextile_Sep = AspectType(AspectName.SEXTILE, 6, 300)
Semisextile_Sep = AspectType(AspectName.SEMISEXTILE, 2, 330)
# Sesqui-square: 2.5
# Quintile: 0.8
# Bi-quintile: 0.8

AspectTypes = [Conjunction, Semisextile, Sextile, Semisquare, Quintile, Square, Trine, Biquintile, Quincunx, Opposition, Quincunx_Sep,
               Trine_Sep,
               Square_Sep, Sextile_Sep, Semisextile_Sep]


def get_aspect_by_name(aspect_name):
    for a in AspectTypes:
        if a.name == aspect_name:
            return a
    print("No aspect found by name: ", aspect_name)


def adjust_deg_for_360(degree):
    # TODO Assert that this only provides degrees in range of 0-359
    adj_degree = degree
    if degree > constants.MAX_CHART_DEGREES:
        adj_degree = degree - constants.MAX_CHART_DEGREES
    elif degree < constants.MIN_CHART_DEGREES:
        adj_degree = degree + constants.MAX_CHART_DEGREES
    return adj_degree
