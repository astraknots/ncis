from enum import Enum


class Side(Enum):
    NONE = ''
    FRONT = 'front'
    BACK = 'back'

    @staticmethod
    def from_str(side_str):
        if side_str in ('front', 'f'):
            return Side.FRONT
        elif side_str in ('back', 'b'):
            return Side.BACK
        else:
            return Side.NONE
            # raise NotImplementedError