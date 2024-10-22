from enum import Enum


class StitchLeg(Enum):
    FRONT_LEG = 'front leg'
    BACK_LEG = 'back leg'
    NONE = ''

    @staticmethod
    def from_str(st_leg_str):
        if st_leg_str in ('front', 'front leg'):
            return StitchLeg.FRONT_LEG
        elif st_leg_str in ('back', 'back leg'):
            return StitchLeg.BACK_LEG
        else:
            return StitchLeg.NONE
            # raise NotImplementedError