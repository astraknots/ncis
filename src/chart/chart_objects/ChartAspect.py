from src.chart.chart_objects.AspectScore import AspectScore


class ChartAspect:
    name = None      #AspectName
    direction = None #AspectDirection, either Applying or Separating (or Exact)
    planets_in_aspect = []  # list 2 of Planet objects
    aspect_score = None  # an AspectScore which gives the intensity and exactness of the aspect, and collective planet speed

    def __init__(self, *args):
        self.name = args[0]
        if len(args) > 1:
            self.direction = args[1]
            if len(args) > 2:
                self.planets_in_aspect = args[2]
                if len(args) > 3:
                    self.aspect_score = args[3]

    def set_aspect_score(self, deg_from_exact):
        if self.name is not None and self.direction is not None:
            score = AspectScore(self.name, deg_from_exact, self.planets_in_aspect)
            self.aspect_score = score
            return True
        else:
            return False

    def get_str_rep(self):
        if self.name is not None and self.direction is not None:
            planets_str = ""
            if len(self.planets_in_aspect) == 2:
                planets_str = self.planets_in_aspect[0].name + ", " + self.planets_in_aspect[1].name
            score_str = ""
            if self.aspect_score is not None:
                return f"{self.direction.name} {self.name} ({planets_str}) : Score={self.aspect_score}"
            else:
                return f"{self.direction.name} {self.name} ({planets_str})"

    def __str__(self):
        return self.get_str_rep()

    def __repr__(self):
        return self.get_str_rep()
