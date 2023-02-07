from enum import Enum



class SignDegreeBase(Enum):
    ARIES = 0
    TAURUS = 30
    GEMINI = 60
    CANCER =90
    LEO = 120
    VIRGO = 150
    LIBRA = 180
    SCORPIO = 210
    SAGITTARIUS = 240
    CAPRICORN = 270
    AQUARIUS = 300
    PISCES = 330


class AspectOrb(Enum):
    CONJ = 10
    SEMISEXTILE = 2
    SEXTILE = 6
    SEMISQUARE = 3
    SQUARE = 8
    TRINE = 8
    QUINCUNX = 2
    OPPOSITION = 10
    BIG3 = 9
    SEMISEXTILE_B = 2
    SEXTILE_B = 6
    SQUARE_B = 8
    TRINE_B = 8


class AspectDegree(Enum):
    # 0 - 180 are applying
    CONJ = 0
    SEMISEXTILE = 30
    SEXTILE = 60
    SEMISQUARE = 45
    SQUARE = 90
    TRINE = 120
    QUINCUNX = 150
    OPPOSITION = 180
    # 181 - 360 (0) are separating
    SEMISEXTILE_B = 330
    SEXTILE_B = 300
    SQUARE_B = 270
    TRINE_B = 240


class Garment(Enum):
    HAT = 4
    SLOUCHY_HAT = 3
    SCARF = 1
    COWL = 2