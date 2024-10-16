from enum import Enum


class WrapDirection(Enum):
    NORMAL = 'normal, counter-clockwise'
    TWISTED = 'twisted, clockwise'
    NONE = 'no wrap, usually slipped'