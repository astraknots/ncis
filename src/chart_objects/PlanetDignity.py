from enum import Enum

from src.chart_objects import Sign
from src.chart_objects.enums.DignityType import DignityType
from src.chart_objects.enums.PlanetName import PlanetName


class PlanetDignity:
    planet = None  # Planet - The planet with dignity
    dignity_type = None  # DignityType - The type of planet dignity
    sign = None  # Sign - The sign of dignity
    sign_dignity_score = None  # The bonus score (according to my spreadsheet of matching modes/elements/genders)

    # +3 for Rulership, +2 for Detriment, see spreadsheet for the rest
    # Range (0-8)

    def __init__(self, *args):
        self.planet = args[0]
        self.dignity_type = args[1]
        self.sign = args[2]

        if len(args) > 3:
            self.sign_dignity_score = args[3]
        else:
            self.sign_dignity_score = 0  # probably should throw an error? or just assume no bonus

        if self.dignity_type == DignityType.RULERSHIP:
            self.sign_dignity_score = self.sign_dignity_score + 4
        elif self.dignity_type == DignityType.EXHAULTATION:
            self.sign_dignity_score = self.sign_dignity_score + 3
        elif self.dignity_type == DignityType.DETRIMENT:
            self.sign_dignity_score = self.sign_dignity_score + 2
        elif self.dignity_type == DignityType.FALL:
            self.sign_dignity_score = self.sign_dignity_score + 1
        # else: PEREGRINE += 0

    def get_str_rep(self):
        return f"Planet Dignity: {self.planet} {self.dignity_type} in {self.sign} Score:{self.sign_dignity_score}"

    def __str__(self):
        return self.get_str_rep()

    def __repr__(self):
        return self.get_str_rep()

PLANET_SIGN_RULERS = {'SUN': ('LEO'), 'MOON': ('CANCER'), 'MERCURY': ('GEMINI', 'VIRGO'), 'VENUS': ('TAURUS', 'LIBRA'),
                      'MARS': ('ARIES', 'SCORPIO'), 'JUPITER': ('SAGITTARIUS', 'PISCES'),
                      'SATURN': ('CAPRICORN', 'AQUARIUS'), 'URANUS': ('AQUARIUS'), 'NEPTUNE': ('PISCES'),
                      'PLUTO': ('SCORPIO')}
PLANET_SIGN_DETRIMENT = {'SUN': ('AQUARIUS'), 'MOON': ('CAPRICORN'), 'MERCURY': ('SAGITTARIUS', 'PISCES'),
                         'VENUS': ('SCORPIO', 'ARIES'), 'MARS': ('LIBRA', 'TAURUS'), 'JUPITER': ('GEMINI', 'VIRGO'),
                         'SATURN': ('CANCER', 'LEO'), 'URANUS': ('LEO'), 'NEPTUNE': ('VIRGO'), 'PLUTO': ('TAURUS')}
PLANET_SIGN_EXHAULTATION = {'SUN': ('ARIES'), 'MOON': ('TAURUS'), 'MERCURY': ('VIRGO'), 'VENUS': ('PISCES'),
                            'MARS': ('CAPRICORN'), 'JUPITER': ('CANCER'), 'SATURN': ('LIBRA'), 'URANUS': ('SCORPIO'),
                            'NEPTUNE': ('CANCER', 'LEO'), 'PLUTO': ('ARIES', 'PISCES')}
PLANET_SIGN_FALL = {'SUN': ('LIBRA'), 'MOON': ('SCORPIO'), 'MERCURY': ('PISCES'), 'VENUS': ('VIRGO'),
                    'MARS': ('CANCER'), 'JUPITER': ('CAPRICORN'), 'SATURN': ('ARIES'), 'URANUS': ('TAURUS'),
                    'NEPTUNE': ('CAPRICORN', 'AQUARIUS'), 'PLUTO': ('VIRGO', 'LIBRA')}

# PLANET_DIGNITY_SCORES - based on how many of gender/heat, element, moisture, cardinality match with the energies of the ruler of the sign
# Detriment are all 2
# Rulership is all 4
PLANET_EXHAULTATION_SCORES = {'SUN': (3), 'MOON': (1), 'MERCURY': (3), 'VENUS': (2), 'MARS': (2), 'JUPITER': (3),
                              'SATURN': (3), 'URANUS': (1), 'NEPTUNE': (3, 0), 'PLUTO': (0, 3)}
PLANET_FALL_SCORES = {'SUN': (1), 'MOON': (3), 'MERCURY': (2), 'VENUS': (1.5), 'MARS': (1), 'JUPITER': (1),
                      'SATURN': (2), 'URANUS': (1), 'NEPTUNE': (1, 1), 'PLUTO': (1, 1)}

sun_leo = PlanetDignity(PlanetName.SUN, DignityType.RULERSHIP, Sign.get_sign_by_sign_name(Sign.SignName.LEO), 4)
moon_cancer = PlanetDignity(PlanetName.MOON, DignityType.RULERSHIP, Sign.get_sign_by_sign_name(Sign.SignName.CANCER), 4)

sun_aquarius = PlanetDignity(PlanetName.SUN, DignityType.DETRIMENT, Sign.get_sign_by_sign_name(Sign.SignName.AQUARIUS), 2)
moon_capricorn = PlanetDignity(PlanetName.MOON, DignityType.DETRIMENT, Sign.get_sign_by_sign_name(
    Sign.SignName.CAPRICORN), 2)

sun_aries = PlanetDignity(PlanetName.SUN, DignityType.EXHAULTATION, Sign.get_sign_by_sign_name(Sign.SignName.ARIES), 3)
moon_taurus = PlanetDignity(PlanetName.MOON, DignityType.EXHAULTATION, Sign.get_sign_by_sign_name(Sign.SignName.TAURUS), 1)

sun_libra = PlanetDignity(PlanetName.SUN, DignityType.FALL, Sign.get_sign_by_sign_name(Sign.SignName.LIBRA), 1)
moon_scorpio = PlanetDignity(PlanetName.MOON, DignityType.FALL, Sign.get_sign_by_sign_name(Sign.SignName.SCORPIO), 3)

sun_taurus = PlanetDignity(PlanetName.SUN, DignityType.PEREGRINE, Sign.get_sign_by_sign_name(Sign.SignName.TAURUS), 2)
sun_gemini = PlanetDignity(PlanetName.SUN, DignityType.PEREGRINE, Sign.get_sign_by_sign_name(Sign.SignName.GEMINI), 1)
sun_cancer = PlanetDignity(PlanetName.SUN, DignityType.PEREGRINE, Sign.get_sign_by_sign_name(Sign.SignName.CANCER), 0)
sun_virgo = PlanetDignity(PlanetName.SUN, DignityType.PEREGRINE, Sign.get_sign_by_sign_name(Sign.SignName.VIRGO), 1)
sun_scorpio = PlanetDignity(PlanetName.SUN, DignityType.PEREGRINE, Sign.get_sign_by_sign_name(Sign.SignName.SCORPIO), 1)
sun_sag = PlanetDignity(PlanetName.SUN, DignityType.PEREGRINE, Sign.get_sign_by_sign_name(Sign.SignName.SAGITTARIUS), 3)
sun_capricorn = PlanetDignity(PlanetName.SUN, DignityType.PEREGRINE, Sign.get_sign_by_sign_name(
    Sign.SignName.CAPRICORN), 1)
sun_pisces = PlanetDignity(PlanetName.SUN, DignityType.PEREGRINE, Sign.get_sign_by_sign_name(Sign.SignName.PISCES), 0)

moon_aries = PlanetDignity(PlanetName.MOON, DignityType.PEREGRINE, Sign.get_sign_by_sign_name(Sign.SignName.ARIES), 0)
moon_gemini = PlanetDignity(PlanetName.MOON, DignityType.PEREGRINE, Sign.get_sign_by_sign_name(Sign.SignName.GEMINI), 1)
moon_leo = PlanetDignity(PlanetName.MOON, DignityType.PEREGRINE, Sign.get_sign_by_sign_name(Sign.SignName.LEO), 0)
moon_virgo = PlanetDignity(PlanetName.MOON, DignityType.PEREGRINE, Sign.get_sign_by_sign_name(Sign.SignName.VIRGO), 1)
moon_libra = PlanetDignity(PlanetName.MOON, DignityType.PEREGRINE, Sign.get_sign_by_sign_name(Sign.SignName.LIBRA), 1)
moon_sag = PlanetDignity(PlanetName.MOON, DignityType.PEREGRINE, Sign.get_sign_by_sign_name(Sign.SignName.SAGITTARIUS), 0)
moon_aquarius = PlanetDignity(PlanetName.MOON, DignityType.PEREGRINE, Sign.get_sign_by_sign_name(
    Sign.SignName.AQUARIUS), 1)
moon_pisces = PlanetDignity(PlanetName.MOON, DignityType.PEREGRINE, Sign.get_sign_by_sign_name(Sign.SignName.PISCES), 3)

PlanetDignities = {DignityType.RULERSHIP: [sun_leo, moon_cancer],
                   DignityType.EXHAULTATION: [sun_aries, moon_taurus],
                   DignityType.FALL: [sun_libra, moon_scorpio],
                   DignityType.DETRIMENT: [sun_aquarius, moon_capricorn],
                   DignityType.PEREGRINE: [moon_aries, moon_gemini, moon_leo, moon_virgo, moon_libra, moon_sag,
                                           moon_aquarius,
                                           moon_pisces, sun_taurus, sun_gemini, sun_cancer, sun_virgo, sun_scorpio,
                                           sun_sag, sun_capricorn, sun_pisces]
                   }


def get_pdignity_by_planet(planet):
    p_dignity_list = []
    for p_dig in globals().keys():
        poss_p_dig = globals()[p_dig]
        if isinstance(poss_p_dig, PlanetDignity):
            if poss_p_dig.planet.name == planet.name:
                p_dignity_list.append(poss_p_dig)

    return p_dignity_list
