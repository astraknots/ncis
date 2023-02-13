from enum import Enum

import Sign
from Dignity import PlanetDignity, Dignity


class BigThree(Enum):
    SUN = True
    MOON = True
    ASC = True
    MERCURY = False
    VENUS = False
    MARS = False
    SATURN = False
    JUPITER = False
    URANUS = False
    NEPTUNE = False
    PLUTO = False


class Planet:
    name = None
    color = None
    speed = None
    dignities = []

    def __init__(self, *args): #name, color, speed, dignities):
        self.name = args[0]
        self.color = args[1]
        self.speed = args[2]
        if len(args) > 3:
            self.dignities = args[3]

    def __iter__(self):
        return self.name

    def get_str_rep(self):
        return f"{self.name} (speed:{self.speed})"

    def __str__(self):
        return self.get_str_rep()

    def __repr__(self):
        return self.get_str_rep()

    def is_big_three(self):
        for big in BigThree:
            if big.name == self.name:
                return big.value



sun_leo = PlanetDignity(Dignity.RULERSHIP, Sign.Leo)

Sun = Planet('SUN', 'yellow', 7, [sun_leo])
Moon = Planet('MOON', 'blue', 10)
Ascendant = Planet('ASC', 'lime', 0)
Mercury = Planet('MERCURY', 'orange', 9)
Venus = Planet('VENUS', 'green', 8)
Mars = Planet('MARS', 'red', 6)
Jupiter = Planet('JUPITER', 'magenta', 5)
Saturn = Planet('SATURN', 'brown', 4)
Uranus = Planet('URANUS', 'cyan', 3)
Neptune = Planet('NEPTUNE', 'purple', 2)
Pluto = Planet('PLUTO', 'silver', 1)

Planets = [Sun, Moon, Ascendant, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto]


def get_planet_by_name(planet_name):
    for p in Planets:
        if p.name == planet_name:
            return p
    print("No planet found by name: ", planet_name)
