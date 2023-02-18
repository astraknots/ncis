from src.chart.chart_objects.ChartPlanet import ChartPlanet
from src.chart.chart_objects.Planet import Planet
from src.chart.chart_objects.enums.AspectDirection import AspectDirection
from src.chart.chart_objects.enums.AspectIntensity import AspectIntensity
from src.chart.chart_objects.enums.AspectName import AspectName
from src.chart.chart_objects.enums.PlanetDirection import PlanetDirection
from src.pattern.pattern_objects.enums.PatternStitchBase import PatternStitchBase


class StitchDeterminer:
    # Stored input off chart cals
    chart_aspect = None # ChartAspect
        # has AspectName
        # has aspect_direction = None # AspectDirection
    aspect_direction = None

    aspect_score = None # AspectScore
        # has aspect_intensity = AspectIntensity.NONE
        # has degree_from_exact or exactness. Range: 0-10
        # has collective_planet_speed = 0
    aspect_intensity = AspectIntensity.NONE
    deg_from_exact = -1

    planet1_speed = 0 # ChartAspect.planets_in_aspect[0].speed
    planet2_speed = 0 # ChartAspect.planets_in_aspect[1].speed
    collective_planet_speed = 0 # AspectScore.collective_planet_speed
    planet1_direction = PlanetDirection.DIRECT
    planet2_direction = PlanetDirection.DIRECT
    planet1_calc_score = 0 #ChartPlanet.dignity_score
    planet2_calc_score = 0

    # Stored output from calcs
    shape_suggestion = ""   # determine from aspect intensity
    stitch_width_exactness = 0        # determine from exactness
    aspect_base_kp = PatternStitchBase.KNIT
    planet_base_kp = [PatternStitchBase.KNIT, PatternStitchBase.KNIT]
    stitch_width_pspeed = [0, 0]

    def __init__(self, *args):
        self.chart_aspect = args[0]
        if self.chart_aspect is not None:
            self.aspect_score = self.chart_aspect.aspect_score
            self.aspect_direction = self.chart_aspect.direction
            self.determine_kp_direction_from_aspect()

            if len(self.chart_aspect.planets_in_aspect) >= 2:
                p1 = self.chart_aspect.planets_in_aspect[0]
                if isinstance(p1, ChartPlanet):
                    self.planet1_speed = p1.planet.speed
                    self.planet1_direction = p1.direction
                    self.determine_kp_direction_from_planet(1, p1)
                    #self.determine_sw_from_planet_speed(1, p1)
                    if p1.sign_dignity is not None:
                        self.planet1_calc_score = p1.get_calc_dignity_score()

                p2 = self.chart_aspect.planets_in_aspect[1]
                if isinstance(p2, ChartPlanet):
                    self.planet2_speed = p2.planet.speed
                    self.planet2_direction = p2.direction
                    self.determine_kp_direction_from_planet(2, p2)
                    #self.determine_sw_from_planet_speed(2, p2)
                    if p2.sign_dignity is not None:
                        self.planet2_calc_score = p2.get_calc_dignity_score()

            if self.aspect_score is not None:
                self.aspect_intensity = self.aspect_score.aspect_intensity
                self.shape_suggestion = suggest_shape(self.aspect_intensity)
                self.deg_from_exact = self.aspect_score.deg_from_exact
                self.get_st_width_from_exact()
                #self.collective_planet_speed = self.aspect_score.collective_planet_speed

    def get_str_rep(self):
        # Exactness Stitch Width: {self.stitch_width_exactness}

        return f"STITCH DETERMINER FOR: {self.chart_aspect} \n" \
               f"{self.shape_suggestion} \n " \
               f"Aspect K/P:{self.aspect_base_kp} \n " \
               f"Planets K/P: {self.planet_base_kp} Planet Scores: {self.planet1_calc_score}, {self.planet2_calc_score} \n " \
               f"Orb Width: {self.chart_aspect.get_aspect_orb()}"

    def __str__(self):
        return self.get_str_rep()

    def __repr__(self):
        return self.get_str_rep()

    def get_st_width_from_exact(self):
        self.stitch_width_exactness = 10 - abs(self.deg_from_exact)

    def determine_kp_direction_from_aspect(self):
        if self.aspect_direction.value > 0:
            self.aspect_base_kp = PatternStitchBase.KNIT
        else:
            self.aspect_base_kp = PatternStitchBase.PURL

    def determine_kp_direction_from_planet(self, planet_num, chart_planet):
        if chart_planet.direction.value > 0:
            self.planet_base_kp[planet_num - 1] = PatternStitchBase.KNIT
        else:
            self.planet_base_kp[planet_num - 1] = PatternStitchBase.PURL

    def determine_sw_from_planet_speed(self, planet_num, chart_planet):
        self.stitch_width_pspeed[planet_num - 1] = chart_planet.planet.speed


def suggest_shape(aspect_intensity):
    if aspect_intensity.name == AspectName.CONJ.name:
        return "Lines, circles, or Chains"
    elif aspect_intensity.name == AspectName.SEXTILE.name:
        return "Stars, Snowflake, or Leaves"
    elif aspect_intensity.name == AspectName.TRINE.name:
        return "Diamonds, Triangles, or Leaves"
    elif aspect_intensity.name == AspectName.SQUARE.name:
        return "Squares, or Diamonds"
    elif aspect_intensity.name == AspectName.OPPOSITION.name:
        return "Circles, Chains, or Honeycomb"
    elif aspect_intensity.name == AspectName.QUINCUNX.name:
        return "Waves"
    elif aspect_intensity.name == AspectName.SESQUISQUARE.name:
        return "Zigzag"
    elif aspect_intensity.name == AspectName.SEMISQUARE.name:
        return "Chevron"
    elif aspect_intensity.name == AspectName.SEMISEXTILE.name:
        return "Snowflake"

    return ""

