from src.chart_objects.AstraChart import AstraChart


class AstraChartCalc(AstraChart):
    # Moved to base class; raw_astra_chart = {} # looks like: { 'SUN' : ['VIRGO',8], 'MOON' : ['SCORPIO', 2], 'ASC' : ['LEO', 17], ' .....
    chart_sign_degrees_by_planet = {} # by Planet, of sign & ChartDegree => {Planet: [Sign, ChartDegree], ... }
    # looks like printed: SUN (speed:7) : [VIRGO (house: 6, element: EARTH, mode: MUTABLE), 158 = 8 Virgo]
    # MOON (speed:10) : [SCORPIO (house: 8, element: WATER, mode: FIXED), 212 = 2 Scorpio]
    # looked like raw: {<Planet.Planet object at 0x100a1e250>: [<Sign.Sign object at 0x100a1dc50>,
    # <ChartDegree.ChartDegree object at 0x100a49350>], ....
    aspect_orbs_by_planet = {} # by Planet: {Planet: {Aspect : [Deg,Deg], Aspect : [Deg, Deg]}}
    chart_aspects_by_planet = {} # by Planet: aspects made between planets for all aspects {Planet = [ChartAspect, ..], ...}
    chart_dignities_by_planet = {} # PlanetDignity list by Planet: {Planet: [PlanetDignity, HouseDignity], ... }

    def __init__(self, astra_chart, *args):
        super().__init__(astra_chart.chartname, astra_chart.person, astra_chart.raw_chart_data)
        self.chart_sign_degrees_by_planet = args[0]
        if len(args) > 1:
            self.aspect_orbs_by_planet = args[1]
            if len(args) > 2:
                self.chart_aspects_by_planet = args[2]
                if len(args) > 3:
                    self.chart_dignities_by_planet = args[3]

    def get_str_rep(self):
        str_rep = "***PLANET : [SIGN, DEGREE]\n"
        for planet in self.chart_sign_degrees_by_planet:
            str_rep = str_rep + "   " + str(planet) + " : " + str(self.chart_sign_degrees_by_planet[planet]) + "\n"

        str_rep = str_rep + "***ASPECT [ORB-DEGREE-RANGE]\n"
        str_rep = str_rep + str(self.aspect_orbs_by_planet)
        for planet in self.aspect_orbs_by_planet:
            str_rep = str_rep + str(planet) + " : " + str(self.chart_sign_degrees_by_planet[planet]) + "\n"
            planet_dict = self.aspect_orbs_by_planet[planet]
            for aspect in planet_dict:
                degree = planet_dict[aspect]
                str_rep = str_rep + "   " + str(aspect) + " : " + str(degree) + "\n"

        str_rep = str_rep + "***Aspects By PLANET [DIRECTION ASPECT (P1, P2) Score, Exactness, Collective Speed]***\n"
        for planet in self.chart_aspects_by_planet:
            str_rep = str_rep + str(planet) + " : " + "\n"
            for aspect in self.chart_aspects_by_planet[planet]:
                str_rep = str_rep + "   " + str(aspect) + "\n"

        return str_rep

    def __str__(self):
        return self.get_str_rep()

    def __repr__(self):
        return self.get_str_rep()

    def order_chart_by_garment_degree_range(self, garment):
        # TODO: Assert that the aspect orbs and planet degree signs are set
        # TODO: determine if this is the right place for this method
        garment_degree_dict = {}

