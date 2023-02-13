from enum import Enum

from Planet import PlanetName
from Sign import Signs, SignName


class Dignity(Enum):
    RULERSHIP = 4
    EXHAULTATION = 3
    DETRIMENT = 2
    FALL = 1
    PEREGRINE = 0


class PlanetDignity:
    planet = None # The planet with dignity
    dtype = None  # The type of planet dignity
    sign = None   # The sign of dignity
    score = None  # The bonus score (according to my spreadsheet of matching modes/elements/genders)
                  # +3 for Rulership, +2 for Detriment, see spreadsheet for the rest

    def __init__(self, *args):
        self.planet = args[0]
        self.dtype = args[1]
        self.sign = args[2]

        if self.dtype == Dignity.RULERSHIP:
            self.score = 4
        elif self.dtype == Dignity.DETRIMENT:
            self.score = 2
        else:
            if len(args) > 3:
                self.score = args[3]
            else:
                self.score = 0  # probably should throw an error? or just assume no bonus


PLANET_SIGN_RULERS = {'SUN': ('LEO'), 'MOON': ('CANCER'), 'MERCURY': ('GEMINI', 'VIRGO'), 'VENUS': ('TAURUS', 'LIBRA'), 'MARS': ('ARIES', 'SCORPIO'), 'JUPITER': ('SAGITTARIUS', 'PISCES'), 'SATURN': ('CAPRICORN', 'AQUARIUS'), 'URANUS': ('AQUARIUS'), 'NEPTUNE': ('PISCES'), 'PLUTO': ('SCORPIO')}
PLANET_SIGN_DETRIMENT = {'SUN': ('AQUARIUS'), 'MOON': ('CAPRICORN'), 'MERCURY': ('SAGITTARIUS', 'PISCES'), 'VENUS': ('SCORPIO', 'ARIES'), 'MARS': ('LIBRA', 'TAURUS'), 'JUPITER': ('GEMINI', 'VIRGO'), 'SATURN': ('CANCER', 'LEO'), 'URANUS': ('LEO'), 'NEPTUNE': ('VIRGO'), 'PLUTO': ('TAURUS')}
PLANET_SIGN_EXHAULTATION = {'SUN': ('ARIES'), 'MOON': ('TAURUS'), 'MERCURY': ('VIRGO'), 'VENUS': ('PISCES'), 'MARS': ('CAPRICORN'), 'JUPITER': ('CANCER'), 'SATURN': ('LIBRA'), 'URANUS': ('SCORPIO'), 'NEPTUNE': ('CANCER', 'LEO'), 'PLUTO': ('ARIES', 'PISCES')}
PLANET_SIGN_FALL = {'SUN': ('LIBRA'), 'MOON': ('SCORPIO'), 'MERCURY': ('PISCES'), 'VENUS': ('VIRGO'), 'MARS': ('CANCER'), 'JUPITER': ('CAPRICORN'), 'SATURN': ('ARIES'), 'URANUS': ('TAURUS'), 'NEPTUNE': ('CAPRICORN', 'AQUARIUS'), 'PLUTO': ('VIRGO', 'LIBRA')}

#PLANET_DIGNITY_SCORES - based on how many of gender/heat, element, moisture, cardinality match with the energies of the ruler of the sign
# Detriment are all 2
# Rulership is all 4
PLANET_EXHAULTATION_SCORES = {'SUN': (3), 'MOON': (1), 'MERCURY': (3), 'VENUS': (2), 'MARS': (2), 'JUPITER': (3), 'SATURN': (3), 'URANUS': (1), 'NEPTUNE': (3, 0), 'PLUTO': (0, 3)}
PLANET_FALL_SCORES = {'SUN': (1), 'MOON': (3), 'MERCURY': (2), 'VENUS': (1.5), 'MARS': (1), 'JUPITER': (1), 'SATURN': (2), 'URANUS': (1), 'NEPTUNE': (1, 1), 'PLUTO': (1, 1)}

sun_leo = PlanetDignity(PlanetName.SUN, Dignity.RULERSHIP, Signs.Leo)
moon_cancer = PlanetDignity(PlanetName.MOON, Dignity.RULERSHIP, Signs.Cancer)
sun_aquarius = PlanetDignity(PlanetName.SUN, Dignity.DETRIMENT, Signs.Aquarius)
moon_capricorn = PlanetDignity(PlanetName.MOON, Dignity.DETRIMENT, Signs.Capricorn)
sun_aries = PlanetDignity(PlanetName.SUN, Dignity.EXHAULTATION, Signs.Aries, 3)
moon_taurus = PlanetDignity(PlanetName.MOON, Dignity.EXHAULTATION, Signs.Taurus, 1)
sun_libra = PlanetDignity(PlanetName.SUN, Dignity.FALL, Signs.Libra, 1)
moon_scorpio = PlanetDignity(PlanetName.MOON, Dignity.FALL, Signs.Scorpio, 3)
