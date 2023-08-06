from ccfcsharp.identifier_dfa import identifier_dfa
from ccfcsharp.lexem import Lexem
from ccfcsharp.lexem_type import LexemType
from ccfcsharp.multiline_comment_dfa import multiline_comment_dfa
from ccfcsharp.number_dfa import number_dfa
from ccfcsharp.operator_dfa import operator_dfa
from ccfcsharp.punctuation_char_dfa import punctuation_char_dfa
from ccfcsharp.singleline_comment_dfa import single_line_comment_dfa
from ccfcsharp.string_dfa import string_dfa
from ccfcsharp.whitespace_sequence_dfa import whitespace_sequence_dfa

AUTOMATA = [
    identifier_dfa,
    multiline_comment_dfa,
    single_line_comment_dfa,
    number_dfa,
    string_dfa,
    whitespace_sequence_dfa,
    punctuation_char_dfa,
    operator_dfa
]

# bug:
# we don't get any lexems if there is only one error lexem
class Lexer:

    @staticmethod
    def lex(text):
        lexems = []
        current_position = 0
        current_invalid_lexem = None

        while current_position < len(text):
            current_lexem = None

            for i in range(len(AUTOMATA)):
                automaton = AUTOMATA[i]
                automaton_result = automaton(current_position, text)

                if current_lexem is None or \
                        (automaton_result is not None and
                         automaton_result.offset > current_lexem.offset):
                    current_lexem = automaton_result

            if current_lexem is not None:

                if current_invalid_lexem is not None:
                    lexems.append(current_invalid_lexem)
                    current_invalid_lexem = None

                lexems.append(current_lexem)
                current_position = current_lexem.offset

                continue

            if current_invalid_lexem is None:
                current_invalid_lexem = Lexem(LexemType.INVALID, current_position + 1, text[current_position])
            else:
                current_invalid_lexem.value += text[current_position]
                current_invalid_lexem.offset += 1

            current_position += 1

        return lexems
