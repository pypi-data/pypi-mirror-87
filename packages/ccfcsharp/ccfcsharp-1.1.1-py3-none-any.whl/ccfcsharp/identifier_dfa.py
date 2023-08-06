from ccfcsharp.keywords_constants import ABSOLUTE_KEYWORDS, CONTEXTUAL_KEYWORDS
from ccfcsharp.lexem import Lexem
from ccfcsharp.lexem_type import LexemType


def identifier_dfa(position, text):

    current_position = position
    dfa_state = 0

    while current_position < len(text):
        current_char = text[current_position]
        current_position += 1
        if dfa_state == 0:
            if current_char == '_' or current_char == '@' or current_char.isalpha():
                dfa_state = 1
            else:
                return None
        elif dfa_state == 1:
            if not (current_char == '_' or current_char.isalpha() or current_char.isnumeric()):
                return Lexem(define_identifier(text[position:current_position - 1]), current_position - 1,
                             text[position:current_position - 1])

    if dfa_state == 1:
        return Lexem(define_identifier(text[position:current_position]), current_position, text[position:current_position])

def define_identifier(word):
    if word in ABSOLUTE_KEYWORDS:
        return LexemType.ABSOLUTE_KEYWORD
    elif word in CONTEXTUAL_KEYWORDS:
        return LexemType.CONTEXTUAL_KEYWORD
    else:
        return LexemType.IDENTIFIER

