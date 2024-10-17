from src.knit_structure.enums.WrapDirection import WrapDirection


class WorkingYarn:
    wrap_direction = WrapDirection.NORMAL  # valid values: WrapDirection: NORMAL, TWISTED, NONE
    num_wraps = 1  # If wrap_direction = NONE, this must be 0; valid values: 0-?
    wy_held = None  # valid values: None, Side.BACK, Side.FRONT

    def __init__(self, wrap_direction=WrapDirection.NORMAL, num_wraps=1, wy_held=None):
        self.wrap_direction = wrap_direction
        if self.wrap_direction == WrapDirection.NONE:
            self.num_wraps = 0  # maybe i should throw an error if invalid args are passed
            # self.wy_held = Side.BACK  # for now, defaulting yarn held back
        else:
            self.num_wraps = num_wraps
        self.wy_held = wy_held  # for now i'll let this get overridden

    def get_str_rep(self):
        str_rep = ""
        if self.wy_held:
            str_rep += f"with working yarn held in {self.wy_held.value}"
        else:
            if self.wrap_direction == WrapDirection.TWISTED:
                str_rep += f"wrapping yarn "
                str_rep += f"in a {self.wrap_direction.value} direction"

            if self.num_wraps > 1:
                str_rep += f"wrapping yarn "
                str_rep += f"{self.num_wraps} times"

        return str_rep

    def __str__(self):
        return self.get_str_rep()

    def __repr__(self):
        return self.get_str_rep()
