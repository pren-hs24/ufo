from enum import Enum

class EdgeState(Enum):
    FREE = 0
    MISSING = 1
    BLOCKED = 2
    UNKNOWN = 3