from src.knit_structure.enums.Needle import Needle


class NeedleInstruction():
    from_needle = Needle.LHN
    to_needle = Needle.RHN

    def __init__(self, from_n=Needle.LHN, to_n=Needle.RHN):
        self.from_needle = from_n
        self.to_needle = to_n

    def get_str_rep(self):
        str_rep = ""
        if self.from_needle:
            str_rep = f" from {self.from_needle.value}"
        if self.to_needle:
            str_rep += f" to {self.to_needle.value}"
        return str_rep

    def __str__(self):
        return self.get_str_rep()

    def __repr__(self):
        return self.get_str_rep()