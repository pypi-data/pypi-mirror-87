from ccfcsharp.lexem import Lexem
from ccfcsharp.lexem_type import LexemType

braces = '{}()[]'
separators = ',;'

def punctuation_char_dfa(position, text):

    current_char = text[position]

    if current_char in braces:
        return Lexem(LexemType.BRACE, position + 1, text[position:position + 1])
    elif current_char in separators:
        return Lexem(LexemType.SEPARATOR, position + 1, text[position:position + 1])

    return None