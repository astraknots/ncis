from src.knit_structure.enums.NeedleDirection import NeedleDirection
from src.knit_structure.enums.Side import Side
from src.knit_structure.enums.StitchLeg import StitchLeg
from src.knit_structure.enums.StitchPart import StitchPart


class IntoStitch:
    # work into the next stitch leg
    into_st_leg = StitchLeg.NONE # StitchLeg: FRONT_LEG, BACK_LEG
    # OR into a different part near the stitch
    into_st_part = None # StitchParts: BAR, BELOW_L, BELOW_R

    # AND/OR indicate a Side working into, or holding to, or inserting needle
    into_side = None  # valid options: Side: FRONT, BACK;

    # How many sts are worked into or at the same time (i.e. k2tog = 2 together): NOT for repeats
    num_worked_into = 1  # valid range: [0-4];  max = 4?

    needle_instr = None     # NeedleInstruction(from_needle, to_needle, needle_action, needle, needle_direction)

    num_rows_below = 0  # valid range: [0-4];  max = 4?

    def __init__(self, _into_st_leg=StitchLeg.NONE, _into_st_part=None, _num_worked_into=1, _needle_instr=None, _num_rows_below=0):
        self.into_st_leg = _into_st_leg
        self.into_st_part = _into_st_part
        self.num_worked_into = _num_worked_into
        self.needle_instr = _needle_instr
        self.num_rows_below = _num_rows_below

    def worked_into_sts(self):
        if self.num_worked_into > 1:
            return f"es "
        else:
            return f""

    def get_str_rep(self):
        str_rep = ""
        if self.into_st_leg != StitchLeg.NONE:
            str_rep += f"into {self.into_st_leg.value}"
            if self.num_worked_into > 1:
                str_rep += "s "
            else:
                str_rep += " "
            if self.num_worked_into > 0:
                str_rep += f"of {self.num_worked_into} stitch" + self.worked_into_sts()
        elif self.into_st_part:
            str_rep += f"into the "
            if self.into_st_part == StitchPart.BAR:
                str_rep += f" {self.into_st_part} "
            else:
                str_rep += f"stitch" + self.worked_into_sts()
                str_rep += f" {self.num_worked_into} "
        elif self.num_worked_into > 0:
            str_rep += f" {self.num_worked_into} stitch" + self.worked_into_sts()
        if self.needle_instr:
            str_rep += f" {self.needle_instr} "
        return str_rep

    def __str__(self):
        return self.get_str_rep()

    def __repr__(self):
        return self.get_str_rep()
