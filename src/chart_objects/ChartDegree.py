from enums import SignDegreeBase


class ChartDegree:
    sign = None
    sign_degree = -1
    degree_360 = -1

    def __init__(self, *args):
        if isinstance(args[0], str):
            self.sign = SignDegreeBase[args[0]]
        else:
            self.sign = args[0]
        self.sign_degree = args[1]
        if len(args) > 2:
            self.degree_360 = args[2]

    def get_str_rep(self):
        if self.degree_360 > 0:
            str_rep = f"{self.degree_360} = {self.sign_degree} {self.sign.name.capitalize()}"
        else:
            str_rep = f"NOTSET = {self.sign_degree} {self.sign.name.capitalize()}"
        return str_rep

    def __str__(self):
        return self.get_str_rep()

    def __repr__(self):
        return self.get_str_rep()

    def calculate_and_set_360_degree_from_sign_degree(self, chart_sign):
        # TODO: Assert that the calculated values are always between 0-359
        deg_base = SignDegreeBase[chart_sign]
        self.degree_360 = self.sign_degree + deg_base.value
