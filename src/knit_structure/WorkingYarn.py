from src.knit_structure.enums.Side import Side
from src.knit_structure.enums.WrapDirection import WrapDirection
from src.knit_structure.enums.YarnAction import YarnAction


# with working yarn {yarn_action}:HELD to {to_side}
# with working yarn {yarn_action}:WRAPPED in a {wrap_direction} direction
# {num_wraps} times
class WorkingYarn:
    num_wraps = 1  # If wrap_direction = NONE, this must be 0; valid values: 0-?
    yarn_action = None  # valid values: YarnActions: HOLD, HELD, WRAP, WRAPPED
    wrap_direction = None  # valid values: WrapDirection: NORMAL, TWISTED, NONE
    to_side = None # valid values: Side.NONE, Side.BACK, Side.FRONT

    def __init__(self, _wrap_direction=None, _num_wraps=1, _yarn_action=None, _to_side=None):
        self.wrap_direction = _wrap_direction
        self.num_wraps = _num_wraps
        self.yarn_action = _yarn_action
        self.to_side = _to_side

    def get_str_rep(self):
        str_rep = ""
        if self.yarn_action:
            str_rep += f"with working yarn {self.yarn_action.value} "
            if self.to_side:
                str_rep += f"to {self.to_side.value} "
            if self.wrap_direction:
                str_rep += f"in a {self.wrap_direction.value} direction, "
        if self.num_wraps > 1:
            str_rep += f" {self.num_wraps} times "
        return str_rep

    def __str__(self):
        return self.get_str_rep()

    def __repr__(self):
        return self.get_str_rep()
