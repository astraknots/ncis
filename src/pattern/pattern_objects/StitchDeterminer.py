from src.chart.chart_objects.ChartPlanet import ChartPlanet
from src.chart.chart_objects.Planet import Planet
from src.chart.chart_objects.enums import Element
from src.chart.chart_objects.enums.AspectDirection import AspectDirection
from src.chart.chart_objects.enums.AspectIntensity import AspectIntensity
from src.chart.chart_objects.enums.AspectName import AspectName
from src.chart.chart_objects.enums.PlanetDirection import PlanetDirection
from src.pattern.pattern_objects.enums.PatternStitchBase import PatternStitchBase

RIGHT_SIDE = "RS"
WRONG_SIDE = "WS"


class StitchDeterminer:
    # Stored input off chart cals
    chart_aspect = None  # ChartAspect
    # has AspectName
    # has aspect_direction = None # AspectDirection
    aspect_direction = None

    aspect_score = None  # AspectScore
    # has aspect_intensity = AspectIntensity.NONE
    # has degree_from_exact or exactness. Range: 0-10
    # has collective_planet_speed = 0
    aspect_intensity = AspectIntensity.NONE
    deg_from_exact = -1

    planet1_speed = 0  # ChartAspect.planets_in_aspect[0].speed
    planet2_speed = 0  # ChartAspect.planets_in_aspect[1].speed
    collective_planet_speed = 0  # AspectScore.collective_planet_speed
    planet1_direction = PlanetDirection.DIRECT
    planet2_direction = PlanetDirection.DIRECT
    planet1_calc_score = 0  # ChartPlanet.dignity_score
    planet2_calc_score = 0

    # Stored output from calcs
    shape_suggestion = ""  # determine from aspect intensity
    stitch_width_exactness = 0  # determine from exactness
    aspect_base_kp = PatternStitchBase.KNIT
    aspect_base_side = RIGHT_SIDE
    planet_base_kp = [PatternStitchBase.KNIT, PatternStitchBase.KNIT]  # TODO: This is not getting written out correctly
    stitch_width_pspeed = [0, 0]

    def __init__(self, *args):
        self.chart_aspect = args[0]
        if self.chart_aspect is not None:
            self.aspect_score = self.chart_aspect.aspect_score
            self.aspect_direction = self.chart_aspect.direction
            self.determine_kp_direction_from_aspect()
            self.determine_rs_ws_from_aspect_direction()

            if len(self.chart_aspect.planets_in_aspect) >= 2:
                p1 = self.chart_aspect.planets_in_aspect[0]
                if isinstance(p1, ChartPlanet):
                    self.planet1_speed = p1.planet.speed
                    self.planet1_direction = p1.direction
                    self.determine_kp_direction_from_planet(1, p1)
                    # self.determine_sw_from_planet_speed(1, p1)
                    if p1.sign_dignity is not None:
                        self.planet1_calc_score = p1.get_calc_dignity_score()

                p2 = self.chart_aspect.planets_in_aspect[1]
                if isinstance(p2, ChartPlanet):
                    self.planet2_speed = p2.planet.speed
                    self.planet2_direction = p2.direction
                    self.determine_kp_direction_from_planet(2, p2)
                    # self.determine_sw_from_planet_speed(2, p2)
                    if p2.sign_dignity is not None:
                        self.planet2_calc_score = p2.get_calc_dignity_score()

            if self.aspect_score is not None:
                self.aspect_intensity = self.aspect_score.aspect_intensity
                self.shape_suggestion = suggest_shape(self.aspect_intensity)
                self.deg_from_exact = self.aspect_score.deg_from_exact
                self.get_st_width_from_exact()
                # self.collective_planet_speed = self.aspect_score.collective_planet_speed

    def get_str_rep(self):
        # Exactness Stitch Width: {self.stitch_width_exactness}
        return f"{self.planet_base_kp} in {self.shape_suggestion[0] if self.aspect_base_side == RIGHT_SIDE else self.shape_suggestion[1]} \n " \
                f" for {self.stitch_width_exactness} stitches on the {self.aspect_base_side} over {self.chart_aspect.get_aspect_orb()} stitches \n " \
                f" Aspecting Planet Dignity Scores: {self.planet1_calc_score}, {self.planet2_calc_score}"

        '''return f"STITCH DETERMINER FOR: {self.chart_aspect} \n" \
               f"Stitches: {self.shape_suggestion[0] if self.aspect_base_side == RIGHT_SIDE else self.shape_suggestion[1]} \n " \
               f"Aspect K/P:{self.aspect_base_kp} \n " \
               f"Aspect RS/WS:{self.aspect_base_side} \n " \
               f"Planets K/P: {self.planet_base_kp} Planet Scores: {self.planet1_calc_score}, {self.planet2_calc_score} \n " \
               f"Orb Width: {self.chart_aspect.get_aspect_orb()}" '''

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

    def determine_rs_ws_from_aspect_direction(self):
        if self.aspect_direction.value > 0:
            self.aspect_base_side = RIGHT_SIDE
        else:
            self.aspect_base_side = WRONG_SIDE

    def determine_kp_direction_from_planet(self, planet_num, chart_planet):
        if chart_planet.element.name in ("WATER", "FIRE"):   # TODO: This is not getting written out correctly
        #if chart_planet.direction.value > 0:
            self.planet_base_kp[planet_num - 1] = PatternStitchBase.KNIT
        else:
            self.planet_base_kp[planet_num - 1] = PatternStitchBase.PURL

    def determine_sw_from_planet_speed(self, planet_num, chart_planet):
        self.stitch_width_pspeed[planet_num - 1] = chart_planet.planet.speed


def suggest_shape(aspect_intensity):
    if aspect_intensity.name == AspectName.CONJ.name:
        return ["YO, M1L, M1R", "kfb, kbf"]  # "Lines, circles, or Chains"
    elif aspect_intensity.name == AspectName.SEXTILE.name:
        return ["Sl 1 wyib", "Sl 1 wyif"]  # "Stars, Snowflake, or Leaves"
    elif aspect_intensity.name == AspectName.TRINE.name:
        return ["Ktbl", "Ptbl"]  # "Diamonds, Triangles, or Leaves"
    elif aspect_intensity.name == AspectName.SQUARE.name:
        return ["k2tog, p2tog, ssk, skp, spp", "p2tog, k2tog, ssp, spp, spp"]  # "Squares, or Diamonds"
    elif aspect_intensity.name == AspectName.OPPOSITION.name:
        return ["Cables, Chains, or Honeycomb", "P"]
    elif aspect_intensity.name == AspectName.QUINCUNX.name:
        return ["LLI, RLI", "P"]  # "Waves"
    elif aspect_intensity.name == AspectName.SESQUISQUARE.name:
        return ["s2kp2", "P"]  # "Zigzag"
    elif aspect_intensity.name == AspectName.SEMISQUARE.name:
        return ["sk2p, k3tog, p3tog", "P, p3tog, k3tog"]  # "Chevron"
    elif aspect_intensity.name == AspectName.SEMISEXTILE.name:
        return ["LI", "P"]  # "Snowflake"

    return ""
