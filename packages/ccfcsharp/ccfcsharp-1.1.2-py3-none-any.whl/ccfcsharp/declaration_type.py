from enum import Enum, auto


class DeclarationType(Enum):
    CLASS = auto(),
    INTERFACE = auto(),
    METHOD = auto(),
    PROPERTY = auto(),
    VARIABLE = auto(),
    PARAMETER = auto(),
    NAMESPACE = auto(),
    USING = auto(),
    CONSTANT = auto(),
    READONLY = auto(),
    FIELD = auto()
