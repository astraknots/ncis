from enum import Enum


class StitchAction(Enum):
    K = 'knit'
    P = 'purl'
    HOLD = 'hold'
    SLIP = 'slip'
    NONE = ''

    # YO = 'yarn over'
    # DS = 'duplicate stitch'
