from AspectType import AspectName, AspectDirection


class ChartAspect:
    aspect_name = None      #AspectName
    aspect_direction = None #AspectDirection
    calc_chart_diff = None  # int, positive or negative
    planets_in_aspect = []  # list 2 of Planet objects

    def __init__(self, *args):
        self.aspect_name = args[0]
        if len(args) > 1:
            self.aspect_direction = args[1]
            if len(args) > 2:
                self.calc_chart_diff = args[2]
                if len(args) > 3:
                    self.planets_in_aspect = args[3]

    def get_str_rep(self):
        if self.aspect_name is not None and self.aspect_direction is not None:
            planets_str = ""
            if len(self.planets_in_aspect) == 2:
                planets_str = self.planets_in_aspect[0].name + ", " + self.planets_in_aspect[1].name
            return f"{self.aspect_direction.name} {self.aspect_name} ({self.calc_chart_diff}, {planets_str})"

    def __str__(self):
        return self.get_str_rep()

    def __repr__(self):
        return self.get_str_rep()