from src.knit_structure.Side import Side
from src.knit_structure.enums.Needle import Needle
from src.knit_structure.enums.StitchType import StitchType
from src.knit_structure.enums.WrapDirection import WrapDirection


class WorkingYarn:
    wrap_direction = WrapDirection.NORMAL
    num_wraps = 1  # If wrap_direction = NONE, this should be 0
    wy_held = Side.BACK

    def __init__(self, wrap_direction=WrapDirection.NORMAL, num_wraps=1, wy_held=Side.BACK):
        self.wrap_direction = wrap_direction
        self.num_wraps = num_wraps
        self.wy_held = wy_held

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
