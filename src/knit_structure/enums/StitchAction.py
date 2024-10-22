from enum import Enum


class StitchAction(Enum):
    K = 'knit'
    P = 'purl'
    HOLD = 'hold'
    SLIP = 'slip'
    NONE = ''

    # YO = 'yarn over'
    # DS = 'duplicate stitch'

    @staticmethod
    def from_str(st_action_str):
        if st_action_str in ('knit', 'k'):
            return StitchAction.K
        elif st_action_str in ('purl', 'p'):
            return StitchAction.P
        elif st_action_str in ('hold'):
            return StitchAction.HOLD
        elif st_action_str in ('slip'):
            return StitchAction.SLIP
        else:
            return StitchAction.NONE
            #raise NotImplementedError