from ccfcsharp.lexem import Lexem
from ccfcsharp.lexem_type import LexemType


def number_dfa(position, text):

    current_position = position
    dfa_state = 0

    default_result = None

    while current_position < len(text):
        current_char = text[current_position]
        current_position += 1

        if dfa_state == 0:
            if current_char.isnumeric():
                dfa_state = 1
                default_result = Lexem(LexemType.INT, current_position, text[position:current_position])
            elif current_char == '.':
                dfa_state = 2
            else:
                return None
        elif dfa_state == 1:
            if current_char == '.':
                dfa_state = 2
            elif current_char.isnumeric():
                default_result = Lexem(LexemType.INT, current_position, text[position:current_position])
            elif current_char == '_':
                dfa_state = 4
            elif current_char == 'L' or current_char == 'l':
                return Lexem(LexemType.LONG, current_position, text[position:current_position])
            else:
                return Lexem(LexemType.INT, current_position - 1, text[position:current_position - 1])
        elif dfa_state == 2:
            if not current_char.isnumeric():
                return None
            dfa_state = 3
            default_result = Lexem(LexemType.DOUBLE, current_position, text[position:current_position])
        elif dfa_state == 3:
            if current_char.isnumeric():
                default_result = Lexem(LexemType.DOUBLE, current_position, text[position:current_position])
                pass
            elif current_char == '_':
                dfa_state = 5
                pass
            elif current_char == 'D' or current_char == 'd':
                return Lexem(LexemType.DOUBLE, current_position, text[position:current_position])
            elif current_char == 'M' or current_char == 'm':
                return Lexem(LexemType.DECIMAL, current_position, text[position:current_position])
            elif current_char == 'F' or current_char == 'f':
                return Lexem(LexemType.FLOAT, current_position, text[position:current_position])
            else:
                current_position -= 1
                return Lexem(LexemType.DOUBLE, current_position, text[position:current_position])
        elif dfa_state == 4:
            if current_char == '_':
                pass
            elif current_char.isnumeric():
                dfa_state = 1
            else:
                return None
        elif dfa_state == 5:
            if current_char == '_':
                pass
            elif current_char.isnumeric():
                default_result = Lexem(LexemType.DOUBLE, current_position, text[position:current_position])
                dfa_state = 3
            else:
                return default_result

    return default_result