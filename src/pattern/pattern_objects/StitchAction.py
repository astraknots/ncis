from enum import Enum

from src.pattern.pattern_objects.enums.PatternStitchBase import PatternStitchBase


class IntoStitch(Enum):
    NONE = ""
    STITCH = "st"
    BELOW = "st below"
    BAR = "bar"
    LADDER = "ladder (down)"


class StitchActionType(Enum):
    INCREASE = "Increase"
    DECREASE = "Decrease"
    PASS = "Pass (over)"
    DROP = "Drop"
    SLIP = "Slip"
    TWIST = "Twist"
    CROSS = "Cross"
    HOLD = "Hold"
    NONE = ""


class StitchDirection(Enum):
    LEFT = "Left"
    RIGHT = "Right"
    AS_IF_KNIT = "as if to knit"
    AS_IF_PURL = "as if to purl"
    FRONT = "Front"
    BACK = "Back"
    NONE = ""


class StitchAction:
    action_name = ""
    z = 0
    binary = None
    action_type = StitchActionType.NONE
    into_st = IntoStitch.NONE
    direction = StitchDirection.NONE

    def __init__(self, *args):
        self.action_name = args[0]
        if len(args) > 1:
            self.z = args[1]
            if len(args) > 2:
                self.binary = args[2]
                if len(args) > 3:
                    self.action_type = args[3]
                    if len(args) > 4:
                        self.into_st = args[4]
                        if len(args) > 5:
                            self.direction = args[5]

    def get_str_rep(self):
        binary_name = ""
        if self.binary is not None:
            binary_name = self.binary.name.capitalize()

        into_phrase = ""
        if self.into_st != IntoStitch.NONE:
            into_phrase = f"into {self.into_st.value}"

        direction_phrase = ""
        if self.direction != StitchDirection.NONE:
            if self.direction in [StitchDirection.AS_IF_KNIT, StitchDirection.AS_IF_PURL]:
                direction_phrase = f" {self.direction.value}"
            else:
                direction_phrase = f" to {self.direction.value}"

        into_direction_phrase = f"{into_phrase} {direction_phrase}"
        if self.direction in [StitchDirection.LEFT, StitchDirection.RIGHT]:
            into_direction_phrase = f"{self.direction.value} {into_phrase}"

        if self.binary is None:
            return f"{self.action_name} {self.z} {into_direction_phrase} ({self.action_type.value})"

        return f"{binary_name} {self.z} {self.action_name} {into_phrase} {direction_phrase} ({self.action_type.value})"

    def __str__(self):
        return self.get_str_rep()

    def __repr__(self):
        return self.get_str_rep()

    #def sts_before(self):


k2tog = StitchAction("Together", 2, PatternStitchBase.KNIT, StitchActionType.DECREASE)
p2tog = StitchAction("Together", 2, PatternStitchBase.PURL, StitchActionType.DECREASE)
m1L = StitchAction("Make", 1, None, StitchActionType.INCREASE, IntoStitch.BAR, StitchDirection.LEFT)
yo = StitchAction("Yarn over", 1, None, StitchActionType.INCREASE)
slip_2 = StitchAction("Slip", 2, None, StitchActionType.SLIP, IntoStitch.NONE, StitchDirection.AS_IF_PURL)
drop_1 = StitchAction("Drop", 1, None, StitchActionType.DROP)

StitchActions = [k2tog, p2tog, m1L, yo, slip_2, drop_1]
