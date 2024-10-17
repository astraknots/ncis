from src.knit_structure.IntoStitch import IntoStitch
from src.knit_structure.NeedleInstruction import NeedleInstruction
from src.knit_structure.enums.Side import Side
from src.knit_structure.StitchInstruction import StitchInstruction
from src.knit_structure.WorkingYarn import WorkingYarn
from src.knit_structure.enums.Needle import Needle
from src.knit_structure.enums.NeedleDirection import NeedleDirection
from src.knit_structure.enums.StitchPart import StitchPart
from src.knit_structure.enums.StitchType import StitchType
from src.knit_structure.enums.WrapDirection import WrapDirection

knit = StitchInstruction()
purl = StitchInstruction(stitch_type=StitchType.P, worked=WorkingYarn(WrapDirection.NORMAL))
k2tog = StitchInstruction(stitch_type=StitchType.K, into=IntoStitch(num_worked_into=2))
p2tog = StitchInstruction(stitch_type=StitchType.P, into=IntoStitch(num_worked_into=2))
sl1_knitwise_to_rhn = StitchInstruction(stitch_type=StitchType.Sl, worked=WorkingYarn(WrapDirection.NONE, wy_held=Side.BACK),
                        into=IntoStitch(needle_dir=NeedleDirection.KNIT_DIRECTION))
sl1_knitwise_to_rhn_no_working = StitchInstruction(stitch_type=StitchType.Sl, worked=WorkingYarn(WrapDirection.NONE),
                        into=IntoStitch(into_st=StitchPart.FRONT, num_worked_into=1, needle_dir=NeedleDirection.KNIT_DIRECTION))
sl1_purlwise_to_lhn = StitchInstruction(stitch_type=StitchType.Sl, worked=WorkingYarn(WrapDirection.NONE),
                                        needle=NeedleInstruction(from_n=Needle.RHN, to_n=Needle.LHN),
                        into=IntoStitch(num_worked_into=1, needle_dir=NeedleDirection.PURL_DIRECTION))
ssk = StitchInstruction(stitch_type=StitchType.K, into=IntoStitch(into_st=StitchPart.BACK, num_worked_into=2, needle_dir=NeedleDirection.KNIT_DIRECTION))

sl1_purlwise_to_cn = StitchInstruction(stitch_type=StitchType.Sl, worked=WorkingYarn(WrapDirection.NONE),
                                       into=IntoStitch(needle_dir=NeedleDirection.PURL_DIRECTION), needle=NeedleInstruction(to_n=Needle.CN))
hold_back = StitchInstruction(stitch_type=StitchType.HOLD, into=IntoStitch(into_st=StitchPart.BACK))
knit_from_cn = StitchInstruction(stitch_type=StitchType.K, needle=NeedleInstruction(from_n=Needle.CN))



print("Knit:", knit)
print("Purl:", purl)
print("k2tog:", k2tog)
print("p2tog:", p2tog)
print("ssk:", sl1_knitwise_to_rhn, ",\n ", sl1_knitwise_to_rhn_no_working, ",\n", sl1_purlwise_to_lhn, ",\n", sl1_purlwise_to_lhn, ",\n", ssk)
print("c4b:", sl1_purlwise_to_cn, ",\n ", sl1_purlwise_to_cn, ",\n ", hold_back, ",\n ", knit, ",\n ", knit, ",\n ", knit_from_cn, ",\n ", knit_from_cn)

