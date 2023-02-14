

class ChartPlanet:
    planet = None
    sign_degree = None
    planet_name = None  # PlanetName.name of the planet in the chart this is for
    sign_dignities = {} # a dict by sign of the dignities for this planet
    dignity_score = 0   # calculated score for the dignity = planet_sign_dignity_score + planet_bonus_dignity + planet_speed + house_dignity

    def __init__(self, *args):
        self.planet = args[0]
        self.planet_name = args[0].name
        if len(args) > 1:
            self.sign_degree = args[1]
            if len(args) > 2:
                self.sign_dignities = args[2]
                if len(args) > 3:
                    self.dignity_score = args[3]

    def get_str_rep(self):
        return f"Chart Planet: {str(self.planet)} "

    def __str__(self):
        return self.get_str_rep()

    def __repr__(self):
        return self.get_str_rep()