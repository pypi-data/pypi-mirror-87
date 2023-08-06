

# to be improved by \nnn, \unnnn
from ccfcsharp.lexem import Lexem
from ccfcsharp.lexem_type import LexemType


def isEscapeChar(char):
    return char in 'abtrv0fn\\'


#to be improved by escape and/or interpolation
def string_dfa(position, text):

    current_position = position
    dfa_state = 0

    while current_position < len(text):
        current_char = text[current_position]
        current_position += 1

        if dfa_state == 0:
            if current_char == '"':
                dfa_state = 1
            else:
                return None
        elif dfa_state == 1:
            if current_char == '"':
                return Lexem(LexemType.STRING, current_position, text[position:current_position])
            elif current_char == '\\':
                dfa_state = 2
        elif dfa_state == 2:
            if isEscapeChar(current_char):
                dfa_state = 1
            else:
                return None

