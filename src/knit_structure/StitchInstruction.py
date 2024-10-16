from src.knit_structure.IntoStitch import IntoStitch
from src.knit_structure.WorkingYarn import WorkingYarn
from src.knit_structure.enums.Needle import Needle
from src.knit_structure.enums.StitchType import StitchType


class StitchInstruction:
    resulting_stitch_type = StitchType.K
    worked = WorkingYarn()
    into = IntoStitch()
    from_needle = Needle.LHN
    to_needle = Needle.RHN

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