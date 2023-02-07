from enum import Enum


class Cycle(Enum):
    SEPARATING = -1
    APPLYING = 1


class Aspect:
    name = None
    orb = None
    degree = None # of 360 degrees or in range of 0-359, where 0=360
    cycle = None # applying or separating

    def __init__(self, name, orb, degree):
        self.name = name
        self.orb = orb
        self.degree = degree
        if degree > 180:
            self.cycle = Cycle.SEPARATING
        else:
            self.cycle = Cycle.APPLYING


Conjunction = Aspect('CONJ', 10, 0)
Semisextile = Aspect('SEMISEXTILE', 2, 30)
Sextile = Aspect('SEXTILE', 6, 60)
Semisquare = Aspect('SEMISQUARE', 3, 45)
Square = Aspect('SQUARE', 8, 90)
Trine = Aspect('TRINE', 8, 120)
Quincunx = Aspect('QUINCUNX', 2, 150)
Opposition = Aspect('OPPOSITION', 10, 180)
Semisextile_Sep = Aspect('SEMISEXTILE_B', 2, 330)
Sextile_Sep = Aspect('SEXTILE_B', 6, 300)
Square_Sep = Aspect('SQUARE_B', 8, 270)
Trine_Sep = Aspect('TRINE_B', 8, 240)
#Sesqui-square: 2.5
#Quintile: 0.8
#Bi-quintile: 0.8

Aspects = [Conjunction, Semisextile, Sextile, Semisquare, Square, Trine, Quincunx, Opposition, Semisextile_Sep, Sextile_Sep, Square_Sep, Trine_Sep]
