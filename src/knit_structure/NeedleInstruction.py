
class NeedleInstruction:
    from_needle = None # Needle.LHN
    to_needle = None # Needle.RHN
    needle = None
    needle_direction = None  # NeedleDirection: KNIT_DIRECTION "as if to knit", PURL_DIRECTION
    needle_action = None   # NeedleAction: INSERT, HOLD

    def __init__(self, _from_needle=None, _to_needle=None, _needle_direction=None, _needle_action=None, _needle=None):
        self.from_needle = _from_needle
        self.to_needle = _to_needle
        self.needle_direction = _needle_direction
        self.needle_action = _needle_action
        self.needle = _needle

    def get_str_rep(self):
        str_rep = ""
        if self.needle_action:
            str_rep += f"{self.needle_action.value} "
        if self.needle:
            str_rep += f"{self.needle.value} "
        if self.from_needle:
            str_rep += f"from {self.from_needle.value} "
        if self.to_needle:
            str_rep += f"to {self.to_needle.value} "
        if self.needle_direction:
            str_rep += f"to {self.needle_direction.value} "
        return str_rep

    def __str__(self):
        return self.get_str_rep()

    def __repr__(self):
        return self.get_str_rep()

    def to_dict(self):
        dict_instr = {}
        n_instr = {}
        if self.from_needle:
            n_instr["from_needle"] = self.from_needle.value
        if self.to_needle:
            n_instr["to_needle"] = self.to_needle.value
        if self.needle:
            n_instr["needle"] = self.needle.value
        if self.needle_direction:
            n_instr["needle_direction"] = self.needle_direction.value
        if self.needle_action:
            n_instr["needle_action"] = self.needle_action.value
        dict_instr["NeedleInstruction"] = n_instr
        return dict_instr
