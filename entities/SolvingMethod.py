from enum import Enum, auto


class SolvingMethod(Enum):
    RECT_RIGHT = auto(),
    RECT_LEFT = auto(),
    RECT_MIDDLE = auto(),
    TRAP = auto(),
    SIMP = auto()