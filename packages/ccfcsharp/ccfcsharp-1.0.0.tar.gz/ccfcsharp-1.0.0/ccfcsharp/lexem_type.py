from enum import Enum

class LexemType(Enum):
    INT = 0,
    FLOAT = 1,
    DOUBLE = 2,
    LONG = 3,
    DECIMAL = 4,
    CHAR = 5,
    STRING = 6,
    IDENTIFIER = 7,
    ABSOLUTE_KEYWORD = 8,
    CONTEXTUAL_KEYWORD = 9,
    BRACE = 10,
    OPERATOR = 11,
    SEPARATOR = 12,
    SINGLELINE_COMMENT = 13,
    MULTILINE_COMMENT = 14,
    DOCUMENTATION_COMMENT = 15,
    WHITESPACE_SEQUENCE = 16,
    INVALID = 17