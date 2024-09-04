from src.chart.chart_objects.enums.PlanetDirection import PlanetDirection


class ChartPlanet:
    planet = None  # the Planet so we can connect to speed and other basics
    direction = PlanetDirection.DIRECT
    element = None # a Sign.Element that this planet is in in the chart
    sign_degree = None  # a ChartDegree object where the planet falls in sign & degree of the chart
    planet_name = None  # PlanetName.name of the planet in the chart this is for
    sign_dignity = None # a PlanetDignity object
    #house_dignities = {} # Future
    dignity_score = 0   # calculated score for the dignity = planet_speed +/- (based on direction)
    # sign_dignity (planet_sign_dignity_score + planet_bonus_dignity) + house_dignity

    def __init__(self, *args):
        self.planet = args[0]
        self.planet_name = args[0].name
        if len(args) > 1:
            self.sign_degree = args[1]
            self.set_planet_element()
            if len(args) > 2:
                self.sign_dignity = args[2]
              #  if len(args) > 3:
                #    self.dignity_score = args[3]

    def get_str_rep(self):
        s_dig = "No Dignity"
        if self.sign_dignity is not None:
            s_dig = str(self.sign_dignity)
        return f"Chart Planet: {str(self.planet)} {self.direction} in {self.sign_degree} \n ({s_dig})"

    def __str__(self):
        return self.get_str_rep()

    def __repr__(self):
        return self.get_str_rep()

    def get_calc_dignity_score(self):
        if self.direction.value > 0:
            self.dignity_score = self.planet.speed + self.sign_dignity.sign_dignity_score
        else:  #Retrograde or Station
            self.dignity_score = self.planet.speed - self.sign_dignity.sign_dignity_score
        return self.dignity_score

    def set_planet_element(self):
        self.element = self.sign_degree[0].element
