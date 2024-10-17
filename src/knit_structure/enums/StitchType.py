from enum import Enum


class StitchType(Enum):
    K = 'knit'
    P = 'purl'
    YO = 'yarn over'
    Sl = 'slip stitch'
    DS = 'duplicate stitch'
