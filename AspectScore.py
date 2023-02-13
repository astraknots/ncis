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


class AspectScore:
    intensity = 0
    exactness = 0
    collective_planet_speed = 0

    def __init__(self, *args):
        if len(args) > 0:
            self.intensity = args[0]
            self.exactness = args[1]
            self.collective_planet_speed = args[2]

    def get_str_rep(self):
        return f"Intensity: {self.intensity}, Exactness:{self.exactness}, Collective Planet Speed:{self.collective_planet_speed}"

    def __str__(self):
        return self.get_str_rep()

    def __repr__(self):
        return self.get_str_rep()

    def determine_aspect_intensity(self, name):
        ai = get_aspect_intensity(name)
        self.intensity = ai.value
        if ai == AspectIntensity.NONE:
            print("............Couldn't find AspectIntensity for:", name)
        return ai.value

    def determine_aspect_exactness(self, aspect, calc_chart_diff):
        if calc_chart_diff == 0:
            exactness = 1
        else:
            exactness = 1 / calc_chart_diff
        if aspect.direction == AspectDirection.APPLYING:
            exactness = exactness + 8
        elif aspect.direction == AspectDirection.SEPARATING:
            exactness = exactness + 5
        elif aspect.direction == AspectDirection.EXACT:
            exactness = exactness + 10
        self.exactness = exactness
        return exactness

    def determine_coll_planet_speed(self, p1, p2):
        if isinstance(p1, Planet) and isinstance(p2, Planet):
            self.collective_planet_speed = p1.speed + p2.speed
        return self.collective_planet_speed
