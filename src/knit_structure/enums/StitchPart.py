from enum import Enum


class StitchPart(Enum):
    FRONT = 'front'
    BACK = 'back'
    BAR = 'the bar between stitches on the needle'
    BELOW_L = 'st below st on LHN'  # work into st below left stitch 2 rows below
    BELOW_R = 'st below st on RHN'
