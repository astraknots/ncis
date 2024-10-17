from src.knit_structure.IntoStitch import IntoStitch
from src.knit_structure.NeedleInstruction import NeedleInstruction
from src.knit_structure.WorkingYarn import WorkingYarn
from src.knit_structure.enums.Needle import Needle
from src.knit_structure.enums.StitchAction import StitchAction
from src.knit_structure.enums.StitchType import StitchType


class StitchInstruction:
    stitch_action = None  # StitchAction.HOLD
    stitch_type = StitchType.K # StitchType: K, P, YO, WRAP, Sl, DS
    needle = NeedleInstruction() #
    worked = WorkingYarn()
    into = IntoStitch()

    def __init__(self, stitch_action=None, stitch_type=StitchType.K, needle=NeedleInstruction(), worked=WorkingYarn(), into=IntoStitch()):
        self.stitch_type = stitch_type
        self.worked = worked
        self.into = into
        self.needle = needle
        self.stitch_action = stitch_action

    def get_str_rep(self):
        str_rep = f"{self.stitch_action} {self.stitch_type} {self.needle} {self.worked} {self.into}"
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
