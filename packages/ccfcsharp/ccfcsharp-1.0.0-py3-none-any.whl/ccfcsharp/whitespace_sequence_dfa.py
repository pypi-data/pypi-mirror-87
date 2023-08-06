from ccfcsharp.lexem import Lexem
from ccfcsharp.lexem_type import LexemType

escape_chars_sequence = ' \n\r\t\v\0\f'

def whitespace_sequence_dfa(position, text):

    current_position = position
    dfa_state = 0

    while current_position < len(text):
        current_char = text[current_position]
        current_position += 1

        if dfa_state == 0:
            if current_char in escape_chars_sequence:
                dfa_state = 1
            else:
                return None
        elif dfa_state == 1:
            if current_char not in escape_chars_sequence:
                return Lexem(LexemType.WHITESPACE_SEQUENCE, current_position - 1, text[position:current_position - 1])