from AspectScore import AspectScore
from AspectType import AspectName, AspectDirection


class ChartAspect:
    name = None      #AspectName
    direction = None #AspectDirection
    calc_chart_diff = None  # int, positive or negative
    planets_in_aspect = []  # list 2 of Planet objects
    score = None

    def __init__(self, *args):
        self.name = args[0]
        if len(args) > 1:
            self.direction = args[1]
            if len(args) > 2:
                self.calc_chart_diff = args[2]
                if len(args) > 3:
                    self.planets_in_aspect = args[3]

    def get_aspect_score(self):
        if self.name is not None and self.direction is not None and self.calc_chart_diff is not None:
            score = AspectScore()
            AspectScore.determine_aspect_exactness(score, self, self.calc_chart_diff)
            AspectScore.determine_aspect_intensity(score, self.name)
            self.score = score
            return True
        else:
            return False

    def get_str_rep(self):
        if self.name is not None and self.direction is not None:
            planets_str = ""
            if len(self.planets_in_aspect) == 2:
                planets_str = self.planets_in_aspect[0].name + ", " + self.planets_in_aspect[1].name
            score_str = ""
            if self.score is not None:
                return f"{self.direction.name} {self.name} ({self.calc_chart_diff}, {planets_str}) : Score={self.score}"
            else:
                return f"{self.direction.name} {self.name} ({self.calc_chart_diff}, {planets_str})"

    def __str__(self):
        return self.get_str_rep()

    def __repr__(self):
        return self.get_str_rep()
