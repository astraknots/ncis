from src.knit_structure.enums.StitchAction import StitchAction


class StitchInstruction:
    name = ""
    stitch_action = None  # StitchAction: K, P, SLIP, HOLD
    needle_instr = None # NeedleInstruction(from_needle, to_needle, needle_action, needle, needle_direction)
    working_yarn = None # WorkingYarn()
    into = None # IntoStitch()
    st_side = None   # Side: FRONT, BACK
    row_instr = None  # RowRndInstruction()
    def __init__(self, _name="", _stitch_action=None, _needle_instr=None, _working_yarn=None, _into_st=None, _st_side=None, _row_instr=None):
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

        if self.stitch_action:
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

    @staticmethod
    def st_instr_from_dict(st_instr_dict):
        needle_instr = None
        working_yarn_instr = None
        into_instr = None
        row_instr = None

        for bkey in st_instr_dict:
            print(bkey, " ", st_instr_dict[bkey])
            match bkey:
                case "into":
                    into_instr = IntoStitch.into_st_from_dict(st_instr_dict[bkey]["IntoStitch"])

                case "needle_instr":
                    needle_instr = st_instr_dict[bkey]["NeedleInstruction"]
                    for ckey in needle_instr:
                        print(ckey, " ", needle_instr[ckey])

                case "working_yarn":
                    working_yarn_instr = st_instr_dict[bkey]["WorkingYarn"]
                    for ckey in working_yarn_instr:
                        print(ckey, " ", working_yarn_instr[ckey])

                case "row_instr":
                    row_instr = st_instr_dict[bkey]["RowRndInstruction"]
                    for ckey in row_instr:
                        print(ckey, " ", row_instr[ckey])

        st_action = StitchAction.from_str(st_instr_dict.get("stitch_action") or None)
        st_side = Side.from_str(st_instr_dict.get("st_side") or None)
        stitch_instruction = StitchInstruction(_name=st_instr["name"], _stitch_action=st_action, _needle_instr=needle_instr,
                                         _working_yarn=working_yarn_instr, _into_st=into_instr, _row_instr=row_instr,
                                         _st_side=st_side)
        return stitch_instruction