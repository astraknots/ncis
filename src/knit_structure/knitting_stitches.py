import json
from types import SimpleNamespace

from src.knit_structure.IntoStitch import IntoStitch
from src.knit_structure.NeedleInstruction import NeedleInstruction
from src.knit_structure.RowRndInstruction import RowRndInstruction
from src.knit_structure.StitchPattern import StitchPattern
from src.knit_structure.enums.IncOrDec import IncOrDec
from src.knit_structure.enums.MinPattWidth import MinPattWidth
from src.knit_structure.enums.RowsOrRounds import RowsOrRounds
from src.knit_structure.enums.Side import Side
from src.knit_structure.StitchInstruction import StitchInstruction
from src.knit_structure.WorkingYarn import WorkingYarn
from src.knit_structure.enums.Needle import Needle
from src.knit_structure.enums.NeedleDirection import NeedleDirection
from src.knit_structure.enums.YarnAction import YarnAction
from src.knit_structure.enums.StitchLeg import StitchLeg
from src.knit_structure.enums.StitchAction import StitchAction
from src.knit_structure.enums.WrapDirection import WrapDirection

knit = StitchInstruction(_name="knit", _stitch_action=StitchAction.K, _into_st=IntoStitch(_into_st_leg=StitchLeg.FRONT_LEG,
                                                                            _num_worked_into=1))
alt_knit = StitchInstruction(_stitch_action=StitchAction.K, _into_st=IntoStitch(_into_st_leg=StitchLeg.FRONT_LEG,
                                                                                _num_worked_into=1,
                                                                                _needle_instr=NeedleInstruction(_needle_direction=NeedleDirection.KNIT_DIRECTION)),
                             _working_yarn=WorkingYarn(_to_side=Side.BACK, _yarn_action=YarnAction.HELD,
                                                       _wrap_direction=WrapDirection.NORMAL, _num_wraps=1))
ktbl = StitchInstruction(_name="ktbl", _stitch_action=StitchAction.K,
                         _into_st=IntoStitch(_into_st_leg=StitchLeg.BACK_LEG, _num_worked_into=1))
purl = StitchInstruction(_name="purl", _stitch_action=StitchAction.P, _into_st=IntoStitch(_into_st_leg=StitchLeg.FRONT_LEG,
                                                                            _num_worked_into=1))
k2tog = StitchInstruction(_name="k2tog", _stitch_action=StitchAction.K, _into_st=IntoStitch(_into_st_leg=StitchLeg.FRONT_LEG, _num_worked_into=2))
p2tog = StitchInstruction(_name="p2tog", _stitch_action=StitchAction.P, _into_st=IntoStitch(_into_st_leg=StitchLeg.FRONT_LEG, _num_worked_into=2))
sl1_knitwise_to_rhn = StitchInstruction(_name="sl1 knitwise", _stitch_action=StitchAction.SLIP,
                                        _into_st=IntoStitch(_needle_instr=NeedleInstruction(_from_needle=Needle.LHN, _to_needle=Needle.RHN, _needle_direction=NeedleDirection.KNIT_DIRECTION)))
sl1_knitwise_to_rhn_no_working = StitchInstruction(_stitch_action=StitchAction.SLIP,
                                                   _working_yarn=WorkingYarn(WrapDirection.NONE),
                                                   _into_st=IntoStitch(_into_st_leg=StitchLeg.FRONT_LEG,
                                                                       _num_worked_into=1,
                                                                       _needle_instr=NeedleInstruction(_needle_direction=NeedleDirection.KNIT_DIRECTION)))
sl1_purlwise_to_lhn = StitchInstruction(_stitch_action=StitchAction.SLIP,
                                        _into_st=IntoStitch(_needle_instr=NeedleInstruction(_from_needle=Needle.RHN, _to_needle=Needle.LHN, _needle_direction=NeedleDirection.PURL_DIRECTION)))
finish_ssk = StitchInstruction(_name="K2tog tbl", _stitch_action=StitchAction.K, _into_st=IntoStitch(_into_st_leg=StitchLeg.BACK_LEG,
                                                                                  _num_worked_into=2))

print(json.dumps(knit.to_dict()))
print(json.dumps(ktbl.to_dict()))
print(json.dumps(k2tog.to_dict()))
print(json.dumps(p2tog.to_dict()))


print(json.dumps(sl1_knitwise_to_rhn.to_dict()))
print(json.dumps(sl1_purlwise_to_lhn.to_dict()))
print(json.dumps(finish_ssk.to_dict()))

knit_st = StitchPattern(name='knit', _ordered_sts=[knit])
purl_st = StitchPattern(name='purl', _ordered_sts=[purl])
kbtl_st = StitchPattern(name='kbtl', _ordered_sts=[ktbl])
k2tog_st = StitchPattern(name='k2tog', _ordered_sts=[k2tog], _inc_or_dec=IncOrDec.DECREASE, _width=2, _min_width=MinPattWidth.EVEN)
p2tog_st = StitchPattern(name='p2tog', _ordered_sts=[p2tog], _inc_or_dec=IncOrDec.DECREASE, _width=2, _min_width=MinPattWidth.EVEN)

ssk_st = StitchPattern(name='ssk', _ordered_sts=[sl1_knitwise_to_rhn, sl1_knitwise_to_rhn, sl1_purlwise_to_lhn,
                                  sl1_purlwise_to_lhn, finish_ssk], _height=1, _width=2, _inc_or_dec=IncOrDec.DECREASE)

print(json.dumps(ssk_st.to_dict()))



sl1_purlwise_to_cn = StitchInstruction(_stitch_action=StitchAction.SLIP,
                                       _into_st=IntoStitch(_needle_instr=NeedleInstruction(_needle_direction=NeedleDirection.PURL_DIRECTION)),
                                       _needle_instr=NeedleInstruction(_to_needle=Needle.CN))
hold_back = StitchInstruction(_stitch_action=YarnAction.HOLD, _st_side=Side.BACK, _needle_instr=NeedleInstruction(_needle=Needle.CN))
knit_st_from_lhn = StitchInstruction(_stitch_action=StitchAction.K, _into_st=IntoStitch(_needle_instr=NeedleInstruction(_from_needle=Needle.LHN)))
knit_from_cn = StitchInstruction(_stitch_action=StitchAction.K, _into_st=IntoStitch(_needle_instr=NeedleInstruction(_from_needle=Needle.CN)))

c4b_st = StitchPattern(name='C4B', _ordered_sts=[sl1_purlwise_to_cn, sl1_purlwise_to_cn, hold_back, knit_st_from_lhn, knit_st_from_lhn, knit_from_cn, knit_from_cn],
                       _width=4, _height=1, _rows_or_rnds=RowsOrRounds.ROWS, _has_cross=True)




print(knit_st, "\n")
print("Alt Knit:", alt_knit, "\n")
print(kbtl_st, "\n")
print(purl_st, "\n")
print(k2tog_st, "\n")
print(p2tog_st, "\n")

print(ssk_st, "\n")
print(c4b_st, "\n")

'''Linen St
(odd number of sts; 2-rnd repeat)
Rnd 1: *K1, slip 1 wyif; repeat from * to last st of pattern section, k1.
Rnd 2: Slip 1 wyif, *k1, slip 1 wyif; repeat from * to end of pattern section. 
'''
linen_rnd_1 = StitchInstruction(_row_instr=RowRndInstruction(_row_instr_num=1, _row_or_rnd=RowsOrRounds.RND), _stitch_action=StitchAction.K, _into_st=IntoStitch(_num_worked_into=1))
sl1_wyif = StitchInstruction(_stitch_action=StitchAction.SLIP, _into_st=IntoStitch(_num_worked_into=1), _working_yarn=WorkingYarn(_yarn_action=YarnAction.HELD, _to_side=Side.FRONT))
linen_rnd_2 = StitchInstruction(_row_instr=RowRndInstruction(_row_instr_num=2, _row_or_rnd=RowsOrRounds.RND),
                                _stitch_action=StitchAction.SLIP, _into_st=IntoStitch(_num_worked_into=1), _working_yarn=WorkingYarn(_yarn_action=YarnAction.HELD, _to_side=Side.FRONT))
knit_1 = StitchInstruction(_stitch_action=StitchAction.K, _into_st=IntoStitch(_num_worked_into=1))

linen_st = StitchPattern(name='linen st', _ordered_sts=[linen_rnd_1, sl1_wyif, linen_rnd_2, knit_1],
                         _min_width=MinPattWidth.EVEN,
                         _height=2, _rows_or_rnds=RowsOrRounds.ROUNDS)

print(linen_st)

'''
with open("./stitch_patterns/linen_st.json", mode="w", encoding="utf-8") as write_file:
    json.dump(linen_st.to_dict(), write_file)
'''

with open("./stitch_patterns/stitch_instructions/knit.json", mode="r", encoding="utf-8") as read_file:
    knit_data = json.load(read_file) #, object_hook = lambda d : StitchInstruction(**d))

print(knit_data)
print(type(knit_data))

def getStitchInstructionFromJSON(json_data):
    st_instr = None

    for akey in json_data:
        print(akey, " ", json_data[akey])
        st_instr = StitchInstruction.st_instr_from_dict(json_data["StitchInstruction"])

        return st_instr

kds = getStitchInstructionFromJSON(knit_data)
print("......")
print(kds)

