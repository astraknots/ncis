

class ChartPlanet:
    planet_name = None  # PlanetName.name of the planet in the chart this is for
    sign_dignities = {} # a dict by sign of the dignities for this planet
    dignity_score = 0   # calculated score for the dignity = planet_sign_dignity_score + planet_bonus_dignity + planet_speed + house_dignity
