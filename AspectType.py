from enum import Enum

import constants


class AspectDirection(Enum):
    SEPARATING = -1
    APPLYING = 1
    CENTERED = 0


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
            self.direction = AspectDirection.CENTERED
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
Semisquare = AspectType(AspectName.SEMISQUARE, 3, 45)
Square = AspectType(AspectName.SQUARE, 8, 90)
Trine = AspectType(AspectName.TRINE, 8, 120)
Quincunx = AspectType(AspectName.QUINCUNX, 2, 150)
Opposition = AspectType(AspectName.OPPOSITION, 10, 180)
Quincunx_Sep = AspectType('QUINCUNX_B', 2, 210)
Trine_Sep = AspectType('TRINE_B', 8, 240)
Square_Sep = AspectType('SQUARE_B', 8, 270)
Sextile_Sep = AspectType('SEXTILE_B', 6, 300)
Semisextile_Sep = AspectType('SEMISEXTILE_B', 2, 330)
# Sesqui-square: 2.5
# Quintile: 0.8
# Bi-quintile: 0.8

AspectTypes = [Conjunction, Semisextile, Sextile, Semisquare, Square, Trine, Quincunx, Opposition, Quincunx_Sep,
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
