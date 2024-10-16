from src.knit_structure.enums.StitchPart import StitchPart


class IntoStitch:
    # default values are for a K stitch
    into_st = StitchPart.FRONT  # valid options: FRONT, BACK, BAR, BELOW_L, BELOW_R
    num_worked_into = 1  # valid range: [0-4];  max = 4?
    num_rows_below = 0  # valid range: [0-4];  max = 4?

    def __init__(self, into_st=StitchPart.FRONT, num_worked_into=1, num_rows_below=0):
        self.into_st = into_st
        self.num_worked_into = num_worked_into
        self.num_rows_below = num_rows_below

    def get_str_rep(self):
        if self.num_worked_into > 0:
            str_rep = f"into {self.into_st.value}"
            if self.into_st != StitchPart.BAR:
                if self.into_st in (StitchPart.BELOW_L, StitchPart.BELOW_R) and self.num_rows_below > 0:
                    if self.num_worked_into > 1:
                        str_rep += f" of {self.num_worked_into} stitches {self.num_rows_below} rows below"
                    elif self.num_worked_into == 1:
                        str_rep += f" of stitch {self.num_rows_below} rows below"
                elif self.num_worked_into > 1:
                    str_rep += f" of {self.num_worked_into} stitches"
                else:
                    str_rep += f" of {self.num_worked_into} stitch"
            return str_rep
        else:
            return ""

    def __str__(self):
        return self.get_str_rep()

    def __repr__(self):
        return self.get_str_rep()
