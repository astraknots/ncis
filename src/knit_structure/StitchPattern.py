from src.knit_structure.enums.IncOrDec import IncOrDec
from src.knit_structure.enums.MinPattWidth import MinPattWidth
from src.knit_structure.enums.RowsOrRounds import RowsOrRounds


class StitchPattern:
    name = ""
    ordered_sts = []
    height = 1  # min height is 1, describes the # of rows/rnds to form the pattern
    width = 1  # min width is 1, describes the number of sts wide to form the pattern
    min_width = MinPattWidth.NUM  # Optional: other than a specific numeric value (NUM) indicated by value in width,
    # could be EVEN or ODD to indicate number of sts for min width can be any even or odd number
    has_cross = False  # indicates whether this stitch pattern has a cable or cross in it
    rows_or_rnds = RowsOrRounds.NONE
    inc_or_dec = IncOrDec.NONE

    def __init__(self, name, _ordered_sts, _height=1, _width=1, _min_width=MinPattWidth.NUM, _has_cross=False, _rows_or_rnds=RowsOrRounds.NONE, _inc_or_dec=IncOrDec.NONE):
        self.name = name
        self.height = _height
        self.width = _width
        self.min_width = _min_width
        self.has_cross = _has_cross
        self.rows_or_rnds = _rows_or_rnds
        self.inc_or_dec = _inc_or_dec
        self.ordered_sts = _ordered_sts

    def worked_into_sts(self):
        if self.width > 1:
            return f"s "
        else:
            return f""
    def get_str_rep(self):
        str_rep = f"Work \"{self.name}\" pattern as: \n"
        cnt = 0
        num_sts = len(self.ordered_sts)
        if num_sts > 0:

            for a_patt in self.ordered_sts:
                cnt += 1
                str_rep += repr(a_patt)
                if cnt != num_sts:
                    str_rep += ",\n"

        if self.inc_or_dec != IncOrDec.NONE:
            str_rep += f"({self.inc_or_dec.value}) "

        if self.min_width == MinPattWidth.NUM:
            str_rep += f" \n-- Pattern repeats over {self.width} st" + self.worked_into_sts()
        elif self.min_width:
            str_rep += f" \n-- Pattern repeats over {self.min_width.value} num of sts "

        if self.height > 1:
            str_rep += f" over {self.height} "
            if self.rows_or_rnds != RowsOrRounds.NONE:
                str_rep += f" {self.rows_or_rnds.value}"
        return str_rep

    def __str__(self):
        return self.get_str_rep()

    def __repr__(self):
        return self.get_str_rep()

    def to_dict(self):
        dict_instr = {}
        st_instr = {}
        st_instr["name"] = self.name
        if self.width:
            st_instr["width"] = self.width
        if self.height:
            st_instr["height"] = self.height
        if self.min_width:
            st_instr["min_width"] = self.min_width.value
        if self.has_cross:
            st_instr["has_cross"] = self.has_cross
        if self.inc_or_dec:
            st_instr["inc_or_dec"] = self.inc_or_dec.value
        if self.rows_or_rnds:
            st_instr["rows_or_rnds"] = self.rows_or_rnds.value
        if len(self.ordered_sts) > 0:
            or_sts = []
            for a_st in self.ordered_sts:
                or_sts.append(a_st.to_dict())
            st_instr["ordered_sts"] = or_sts
        dict_instr["StitchPattern"] = st_instr
        return dict_instr
