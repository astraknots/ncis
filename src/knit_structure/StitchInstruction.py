from src.knit_structure.enums.StitchAction import StitchAction


class StitchInstruction:
    stitch_action = StitchAction.NONE  # StitchAction: K, P, SLIP, HOLD
    needle_instr = None # NeedleInstruction(from_needle, to_needle, needle_action, needle, needle_direction)
    worked = None # WorkingYarn()
    into = None # IntoStitch()
    st_side = None   # Side: FRONT, BACK
    row_instr = None
    def __init__(self, _stitch_action=StitchAction.NONE, _needle_instr=None, _working_yarn=None, _into_st=None, _st_side=None, _row_instr=None):
        self.worked = _working_yarn
        self.into = _into_st
        self.needle_instr = _needle_instr
        self.stitch_action = _stitch_action
        self.st_side = _st_side
        self.row_instr = _row_instr

    def get_str_rep(self):
        str_rep = ""
        if self.row_instr:
            str_rep += f" {self.row_instr} "

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

        return str_rep

    def __str__(self):
        return self.get_str_rep()

    def __repr__(self):
        return self.get_str_rep()
