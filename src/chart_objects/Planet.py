from enum import Enum

from src.chart_objects.enums.BigThree import BigThree
from src.chart_objects.enums.PlanetName import PlanetName


class Planet:
    name = None
    color = None
    speed = None

    def __init__(self, *args):  # name, color, speed, dignities):
        self.name = args[0].name
        self.color = args[1]
        self.speed = args[2]

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


Sun = Planet(PlanetName.SUN, 'yellow', 7)
Moon = Planet(PlanetName.MOON, 'blue', 10)
Ascendant = Planet(PlanetName.ASC, 'lime', 0)
Mercury = Planet(PlanetName.MERCURY, 'orange', 9)
Venus = Planet(PlanetName.VENUS, 'green', 8)
Mars = Planet(PlanetName.MARS, 'red', 6)
Jupiter = Planet(PlanetName.JUPITER, 'magenta', 5)
Saturn = Planet(PlanetName.SATURN, 'brown', 4)
Uranus = Planet(PlanetName.URANUS, 'cyan', 3)
Neptune = Planet(PlanetName.NEPTUNE, 'purple', 2)
Pluto = Planet(PlanetName.PLUTO, 'silver', 1)

Planets = [Sun, Moon, Ascendant, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto]


def get_planet_by_name(planet_name):
    for p in Planets:
        if p.name == planet_name:
            return p
    print("No planet found by name: ", planet_name)
