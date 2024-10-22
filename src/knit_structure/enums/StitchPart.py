from enum import Enum


class StitchPart(Enum):
    BELOW_L = 'below stitch on LHN'
    BELOW_R = 'below stitch on RHN'
    BAR = 'the bar between stitches on the needle ' # (last row working yarn between sts)

