from AspectType import AspectName, AspectDirection
from enum import Enum

from Planet import Planet


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
    #self.intensity_nature = ai.value
    if ai == AspectIntensity.NONE:
        print("............Couldn't find AspectIntensity for:", name)
    return ai.value


class AspectScore:
    intensity_nature = 0
    deg_from_exact = None  # The exactness of the aspect:  int, positive or negative, degrees_from_exact
    collective_planet_speed = 0

    def __init__(self, *args):
        if len(args) > 0:
            self.intensity_nature = determine_aspect_intensity(args[0])
            self.deg_from_exact = args[1]
            self.collective_planet_speed = self.determine_coll_planet_speed(args[2])

    def get_str_rep(self):
        return f"Intensity: {self.intensity_nature}, Exactness:{self.deg_from_exact}, Collective Planet Speed:{self.collective_planet_speed}"

    def __str__(self):
        return self.get_str_rep()

    def __repr__(self):
        return self.get_str_rep()

    def determine_coll_planet_speed(self, *args):
        if isinstance(args[0], list):
            c_speed = 0
            for p in args[0]: # assuming it's a list of Planet
                if isinstance(p, Planet):
                    c_speed = c_speed + p.speed
                elif isinstance(p, int):
                    c_speed = c_speed + p
            self.collective_planet_speed = c_speed
        return self.collective_planet_speed
