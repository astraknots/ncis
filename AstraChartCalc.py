

class AstraChartCalc:
    raw_astra_chart = {} # looks like: { 'SUN' : ['VIRGO',8], 'MOON' : ['SCORPIO', 2], 'ASC' : ['LEO', 17], ' .....
    planet_sign_degrees = {}
    # looks like printed: SUN (speed:7) : [VIRGO (house: 6, element: EARTH, mode: MUTABLE), 158 = 8 Virgo]
    # MOON (speed:10) : [SCORPIO (house: 8, element: WATER, mode: FIXED), 212 = 2 Scorpio]
    # looked like raw: {<Planet.Planet object at 0x100a1e250>: [<Sign.Sign object at 0x100a1dc50>,
    # <ChartDegree.ChartDegree object at 0x100a49350>], ....
    aspect_orbs = {} # by planet: {Planet = {Aspect : [Deg,Deg], Aspect : [Deg, Deg]}}
    planet_aspects = {} # aspects made between planets for all aspects

    def __init__(self, *args):
        self.raw_astra_chart = args[0]
        if len(args) > 1:
            self.planet_sign_degrees = args[1]
        if len(args) > 2:
            self.aspect_orbs = args[2]

    def get_str_rep(self):
        str_rep = "PLANET : [SIGN, DEGREE]\n"
        #for planet in self.planet_sign_degrees:
        #    str_rep = str_rep + "   " + str(planet) + " : " + str(self.planet_sign_degrees[planet]) + "\n"
        str_rep = str_rep + "  ASPECT [ORB-DEGREE-RANGE]\n"
        #str_rep = str_rep + str(self.aspect_orbs)
        for planet in self.aspect_orbs:
            str_rep = str_rep + str(planet) + " : " + str(self.planet_sign_degrees[planet]) + "\n"
            planet_dict = self.aspect_orbs[planet]
            for aspect in planet_dict:
                degree = planet_dict[aspect]
                str_rep = str_rep + "   " + str(aspect) + " : " + str(degree) + "\n"
        return str_rep

    def __str__(self):
        return self.get_str_rep()

    def __repr__(self):
        return self.get_str_rep()

    def order_chart_by_garment_degree_range(self, garment):
        # TODO: Assert that the aspect orbs and planet degree signs are set
        # TODO: determine if this is the right place for this method
        garment_degree_dict = {}

