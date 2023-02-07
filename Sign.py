from enum import Enum


class Element(Enum):
    WATER = (4, 8, 12)
    FIRE = (1, 5, 9)
    AIR = (3, 7, 11)
    EARTH = (2, 6, 10)


class Mode(Enum):
    CARDINAL = (1, 10, 7, 4)
    FIXED = (5, 2, 11, 8)
    MUTABLE = (9, 6, 3, 12)


class Sign:
    name = None
    degree_base = None  # 360 degree base
    element = None
    mode = None
    natural_house = None

    def __init__(self, name, degree_base, element, mode, natural_house):
        self.name = name
        self.degree_base = degree_base
        self.element = element
        self.mode = mode
        self.natural_house = natural_house


Aries = Sign('ARIES', 0, Element.FIRE, Mode.CARDINAL, 1)
Taurus = Sign('TAURUS', 30, Element.EARTH, Mode.FIXED, 2)
Gemini = Sign('GEMINI', 60, Element.AIR, Mode.MUTABLE, 3)
Cancer = Sign('CANCER', 90, Element.WATER, Mode.CARDINAL, 4)
Leo = Sign('LEO', 120, Element.FIRE, Mode.FIXED, 5)
Virgo = Sign('VIRGO', 150, Element.EARTH, Mode.MUTABLE, 6)
Libra = Sign('LIBRA', 180, Element.AIR, Mode.CARDINAL, 7)
Scorpio = Sign('SCORPIO', 210, Element.WATER, Mode.FIXED, 8)
Sagittarius = Sign('SAGITTARIUS', 240, Element.FIRE, Mode.MUTABLE, 9)
Capricorn = Sign('CAPRICORN', 270, Element.EARTH, Mode.CARDINAL, 10)
Aquarius = Sign('AQUARIUS', 300, Element.AIR, Mode.FIXED, 11)
Pisces = Sign('PISCES', 330, Element.WATER, Mode.MUTABLE, 12)

Signs = [Aries, Taurus, Gemini, Cancer, Leo, Virgo, Libra, Scorpio, Sagittarius, Capricorn, Aquarius, Pisces]
