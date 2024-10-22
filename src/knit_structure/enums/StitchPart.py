from enum import Enum


class StitchPart(Enum):
    BELOW_L = 'below stitch on LHN'
    BELOW_R = 'below stitch on RHN'
    BAR = 'the bar between stitches on the needle' # (last row working yarn between sts)
    NONE = ''

    @staticmethod
    def from_str(st_part_str):
        if st_part_str in ('below l', 'below stitch on LHN'):
            return StitchPart.BELOW_L
        elif st_part_str in ('below stitch on RHN', 'below r'):
            return StitchPart.BELOW_R
        elif st_part_str in ('bar', 'the bar between stitches on the needle'):
            return StitchPart.BAR
        else:
            return StitchPart.NONE
            # raise NotImplementedError
