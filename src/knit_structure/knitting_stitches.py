from src.knit_structure.IntoStitch import IntoStitch
from src.knit_structure.NeedleInstruction import NeedleInstruction
from src.knit_structure.StitchPattern import StitchPattern
from src.knit_structure.enums.IncOrDec import IncOrDec
from src.knit_structure.enums.Side import Side
from src.knit_structure.StitchInstruction import StitchInstruction
from src.knit_structure.WorkingYarn import WorkingYarn
from src.knit_structure.enums.Needle import Needle
from src.knit_structure.enums.NeedleDirection import NeedleDirection
from src.knit_structure.enums.YarnAction import YarnAction
from src.knit_structure.enums.StitchLeg import StitchLeg
from src.knit_structure.enums.StitchAction import StitchAction
from src.knit_structure.enums.WrapDirection import WrapDirection

knit = StitchInstruction(_stitch_action=StitchAction.K, _into_st=IntoStitch(_into_st_leg=StitchLeg.FRONT_LEG,
                                                                            _num_worked_into=1))
alt_knit = StitchInstruction(_stitch_action=StitchAction.K, _into_st=IntoStitch(_into_st_leg=StitchLeg.FRONT_LEG,
                                                                                _num_worked_into=1,
                                                                                _needle_dir=NeedleDirection.KNIT_DIRECTION),
                             _working_yarn=WorkingYarn(_to_side=Side.BACK, _yarn_action=YarnAction.HELD,
                                                       _wrap_direction=WrapDirection.NORMAL, _num_wraps=1))
kbtl = StitchInstruction(_stitch_action=StitchAction.K,
                         _into_st=IntoStitch(_into_st_leg=StitchLeg.BACK_LEG, _num_worked_into=1))
purl = StitchInstruction(_stitch_action=StitchAction.P, _into_st=IntoStitch(_into_st_leg=StitchLeg.FRONT_LEG,
                                                                            _num_worked_into=1))
k2tog = StitchInstruction(_stitch_action=StitchAction.K, _into_st=IntoStitch(_into_st_leg=StitchLeg.FRONT_LEG, _num_worked_into=2))
p2tog = StitchInstruction(_stitch_action=StitchAction.P, _into_st=IntoStitch(_into_st_leg=StitchLeg.FRONT_LEG, _num_worked_into=2))
sl1_knitwise_to_rhn = StitchInstruction(_stitch_action=StitchAction.SLIP, _needle_instr=NeedleInstruction(from_n=Needle.LHN, to_n=Needle.RHN),
                                        _into_st=IntoStitch(_needle_dir=NeedleDirection.KNIT_DIRECTION))
sl1_knitwise_to_rhn_no_working = StitchInstruction(_stitch_action=StitchAction.SLIP,
                                                   _working_yarn=WorkingYarn(WrapDirection.NONE),
                                                   _into_st=IntoStitch(_into_st_leg=StitchLeg.FRONT_LEG,
                                                                       _num_worked_into=1,
                                                                       _needle_dir=NeedleDirection.KNIT_DIRECTION))
sl1_purlwise_to_lhn = StitchInstruction(_stitch_action=StitchAction.SLIP, _needle_instr=NeedleInstruction(from_n=Needle.RHN, to_n=Needle.LHN),
                                        _into_st=IntoStitch(_needle_dir=NeedleDirection.PURL_DIRECTION))
finish_ssk = StitchInstruction(_stitch_action=StitchAction.K, _into_st=IntoStitch(_into_st_leg=StitchLeg.BACK_LEG,
                                                                                  _num_worked_into=2))

knit_st = StitchPattern(name='knit', _ordered_sts=[knit])
purl_st = StitchPattern(name='purl', _ordered_sts=[purl])
kbtl_st = StitchPattern(name='kbtl', _ordered_sts=[kbtl])
k2tog_st = StitchPattern(name='k2tog', _ordered_sts=[k2tog], _inc_or_dec=IncOrDec.DECREASE)
p2tog_st = StitchPattern(name='p2tog', _ordered_sts=[p2tog], _inc_or_dec=IncOrDec.DECREASE)

ssk_st = StitchPattern(name='ssk', _ordered_sts=[sl1_knitwise_to_rhn, sl1_knitwise_to_rhn, sl1_purlwise_to_lhn,
                                  sl1_purlwise_to_lhn, finish_ssk], _height=1, _width=2, _inc_or_dec=IncOrDec.DECREASE)


sl1_purlwise_to_cn = StitchInstruction(_stitch_action=StitchAction.SLIP,
                                       _into_st=IntoStitch(_needle_dir=NeedleDirection.PURL_DIRECTION),
                                       _needle_instr=NeedleInstruction(to_n=Needle.CN))
hold_back = StitchInstruction(_stitch_action=YarnAction.HOLD, _st_side=Side.BACK)
knit_from_cn = StitchInstruction(_stitch_action=StitchAction.K, _needle_instr=NeedleInstruction(from_n=Needle.CN))

c4b_st = StitchPattern(name='C4B', _ordered_sts=[sl1_purlwise_to_cn, sl1_purlwise_to_cn, hold_back, knit, knit, knit_from_cn, knit_from_cn])


print(knit_st, "\n")
print("Alt Knit:", alt_knit, "\n")
print(kbtl_st, "\n")
print(purl_st, "\n")
print(k2tog_st, "\n")
print(p2tog_st, "\n")

print(ssk_st, "\n")
print(c4b_st, "\n")
