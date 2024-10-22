from src.knit_structure.enums.StitchAction import StitchAction


class StitchInstruction:
    name = ""
    stitch_action = StitchAction.NONE  # StitchAction: K, P, SLIP, HOLD
    needle_instr = None # NeedleInstruction(from_needle, to_needle, needle_action, needle, needle_direction)
    working_yarn = None # WorkingYarn()
    into = None # IntoStitch()
    st_side = None   # Side: FRONT, BACK
    row_instr = None  # RowRndInstruction
    def __init__(self, _name="", _stitch_action=StitchAction.NONE, _needle_instr=None, _working_yarn=None, _into_st=None, _st_side=None, _row_instr=None):
        self.name = _name
        self.working_yarn = _working_yarn
        self.into = _into_st
        self.needle_instr = _needle_instr
        self.stitch_action = _stitch_action
        self.st_side = _st_side
        self.row_instr = _row_instr

    def get_str_rep(self):
        str_rep = ""
        if self.name != "":
            str_rep += f"{self.name}: "
        if self.row_instr:
            str_rep += f" {self.row_instr} "

        if self.stitch_action != StitchAction.NONE:
            str_rep += f"{self.stitch_action.value} "

        if self.needle_instr:
            str_rep += f" {self.needle_instr} "
        if self.working_yarn:
            str_rep += f" {self.working_yarn} "
        if self.into:
            str_rep += f" {self.into} "
        if self.st_side:
            str_rep += f" {self.st_side.value} "

        return str_rep

    def __str__(self):
        return self.get_str_rep()

    def __repr__(self):
        return self.get_str_rep()

    def to_dict(self):
        dict_instr = {}
        st_instr = {}
        st_instr["name"] = self.name
        if self.stitch_action:
            st_instr["stitch_action"] = self.stitch_action.value
        if self.needle_instr:
            st_instr["needle_instr"] = self.needle_instr.to_dict()
        if self.working_yarn:
            st_instr["working_yarn"] = self.working_yarn.to_dict()
        if self.into:
            st_instr["into"] = self.into.to_dict()
        if self.st_side:
            st_instr["st_side"] = self.st_side.value
        if self.row_instr:
            st_instr["row_instr"] = self.row_instr.to_dict()
        dict_instr["StitchInstruction"] = st_instr
        return dict_instr