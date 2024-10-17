from src.knit_structure.enums.NeedleDirection import NeedleDirection
from src.knit_structure.enums.Side import Side
from src.knit_structure.enums.StitchLeg import StitchLeg
from src.knit_structure.enums.StitchPart import StitchPart


class IntoStitch:
    # work into the next stitch leg
    into_st_leg = StitchLeg.FRONT_LEG # StitchLeg: FRONT_LEG, BACK_LEG
    # OR into a different part near the stitch
    into_st_part = None # StitchParts: BAR, BELOW_L, BELOW_R
    num_rows_below = 0  # valid range: [0-4];  max = 4?

    # AND/OR indicate a Side working into, or holding to
    into_side = None  # valid options: Side: FRONT, BACK; could also be for an action, like 'hold front'

    # How many sts are worked into or at the same time (i.e. k2tog = 2 together): NOT for repeats
    num_worked_into = 1  # valid range: [0-4];  max = 4?

    needle_direction = None # NeedleDirection: KNIT_DIRECTION (as if to knit), or PURL_DIRECTION (as if to purl)

    def __init__(self, into_st=None, num_worked_into=1, num_rows_below=0, needle_dir=None):
        self.into_st_part = into_st
        self.num_worked_into = num_worked_into
        self.num_rows_below = num_rows_below
        self.needle_direction = needle_dir

    def get_str_rep(self):
        str_rep = f" into {self.into_st.value} of {self.num_worked_into} stitch(es)"
        return str_rep
        '''str_rep = ""
        if self.num_worked_into > 0:
            str_rep += f" {self.into_st.value}"
            if self.into_st != StitchPart.BAR:
                if self.into_st in (StitchPart.BELOW_L, StitchPart.BELOW_R) and self.num_rows_below > 0:
                    if self.num_worked_into > 1:
                        str_rep += f" of {self.num_worked_into} stitches {self.num_rows_below} rows below"
                    elif self.num_worked_into == 1:
                        str_rep += f" of stitch {self.num_rows_below} rows below"
                elif self.num_worked_into > 1:
                    str_rep += f" of {self.num_worked_into} stitches (together)"
                else:
                    str_rep += f" of {self.num_worked_into} stitch"
            if self.needle_direction:
                str_rep += f" {self.needle_direction.value}"
            return str_rep
        else:
            return ""
            '''

    def __str__(self):
        return self.get_str_rep()

    def __repr__(self):
        return self.get_str_rep()
