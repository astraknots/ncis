from src.knit_structure.enums.StitchAction import StitchAction


class StitchInstruction:
    stitch_action = StitchAction.NONE  # StitchAction: K, P, SLIP, HOLD
    needle_instr = None # NeedleInstruction() #TODO: Rework the needle instruction to take needle and direction and action
    worked = None # WorkingYarn()
    into = None # IntoStitch()
    st_side = None   # Side: FRONT, BACK

    def __init__(self, _stitch_action=StitchAction.NONE, _needle_instr=None, _working_yarn=None, _into_st=None, _st_side=None):
        self.worked = _working_yarn
        self.into = _into_st
        self.needle_instr = _needle_instr
        self.stitch_action = _stitch_action
        self.st_side = _st_side

    def get_str_rep(self):
        str_rep = ""
        if self.stitch_action != StitchAction.NONE:
            str_rep += f"{self.stitch_action.value} "

        if self.needle_instr:
            str_rep += f" {self.needle_instr} "
        if self.worked:
            str_rep += f" {self.worked} "
        if self.into:
            str_rep += f" {self.into} "
        if self.st_side:
            str_rep += f" {self.st_side.value} "

        '''if self.resulting_stitch_action in [StitchAction.HOLD]:
            str_rep = f"{self.resulting_stitch_action} {self.into.into_st.value}"
        if self.resulting_stitch_type in [StitchType.Sl]:
            str_rep = f"{self.worked} {self.resulting_stitch_type.value} into {self.into} {self.needle} "
        elif self.resulting_stitch_type in [StitchType.HOLD]:
            str_rep = f"{self.resulting_stitch_type.value} {self.into}"
        else:
            str_rep = f"{self.resulting_stitch_type.value} {self.worked} into {self.into}" '''
        return str_rep

    def __str__(self):
        return self.get_str_rep()

    def __repr__(self):
        return self.get_str_rep()
