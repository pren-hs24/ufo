from enum import Enum

class NodeState(Enum):
    UNKNOWN = 0
    FREE = 1
    BLOCKED = 2