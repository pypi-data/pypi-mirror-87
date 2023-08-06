from ccfcsharp.lexem import Lexem
from ccfcsharp.lexem_type import LexemType


def multiline_comment_dfa(position, text):

    current_position = position
    dfa_state = 0

    while current_position < len(text):
        current_char = text[current_position]
        current_position += 1

        if dfa_state == 0:
            if current_char == '/':
                dfa_state = 1
            else:
                return None
        elif dfa_state == 1:
            if current_char == '*':
                dfa_state = 2
            else:
                return None
        elif dfa_state == 2:
            if current_char == '*':
                dfa_state = 3
        elif dfa_state == 3:
            if current_char == '/':
                return Lexem(LexemType.MULTILINE_COMMENT, current_position, text[position:current_position])
            else:
                dfa_state = 2
    return None
