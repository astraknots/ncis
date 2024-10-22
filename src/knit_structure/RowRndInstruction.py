from src.knit_structure.enums.RowsOrRounds import RowsOrRounds


class RowRndInstruction:
    row_instr_num = None
    row_or_rnd = None

    def __init__(self, _row_instr_num=None, _row_or_rnd=RowsOrRounds.NONE):
        self.row_instr_num = _row_instr_num
        self.row_or_rnd = _row_or_rnd

    def get_str_rep(self):
        str_rep = ""
        if self.row_or_rnd:
            str_rep += f"{self.row_or_rnd.value} "
        if self.row_instr_num:
            str_rep += f"{self.row_instr_num}: "
        return str_rep

    def __str__(self):
        return self.get_str_rep()

    def __repr__(self):
        return self.get_str_rep()