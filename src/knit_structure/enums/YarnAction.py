from enum import Enum


class YarnAction(Enum):
    HOLD = 'hold'
    HELD = 'held'
    WRAP = 'wrap'
    WRAPPED = 'wrapped'
    NONE = ''
