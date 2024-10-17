from enum import Enum


class StitchPart(Enum):
    BELOW_L = 'the stitch below stitch on LHN'
    BELOW_R = 'the stitch below stitch on RHN'
    BAR = 'the bar between stitches on the needle (last row working yarn between sts)'

