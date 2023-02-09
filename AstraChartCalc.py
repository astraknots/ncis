

class AstraChartCalc:
    raw_astra_chart = {} # looks like: { 'SUN' : ['VIRGO',8], 'MOON' : ['SCORPIO', 2], 'ASC' : ['LEO', 17], ' .....
    planet_sign_degrees = {}
    # looks like printed: {SUN: (speed:7): [VIRGO: (house: 6, element: EARTH, mode: MUTABLE), [158]: (Virgo: 8)],
    # MOON: (speed:10): [SCORPIO: (house: 8, element: WATER, mode: FIXED), [212]: (Scorpio: 2)], ....
    # looked like raw: {<Planet.Planet object at 0x100a1e250>: [<Sign.Sign object at 0x100a1dc50>,
    # <ChartDegree.ChartDegree object at 0x100a49350>], ....


    def __init__(self, *args):
        raw_astra_chart = args[0]
        if len(args) > 1:
            planet_sign_degrees = args[1]

    def get_str_rep(self):
        str_rep = ""
        for planet in self.planet_sign_degrees:
            str_rep = str_rep + str(planet) + " : " + str(self.planet_sign_degrees[planet]) + "\n"
        return str_rep

    def __str__(self):
        return self.get_str_rep()

    def __repr__(self):
        return self.get_str_rep()
