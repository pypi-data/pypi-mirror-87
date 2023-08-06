from ccfcsharp.lexem import Lexem
from ccfcsharp.lexem_type import LexemType


def operator_dfa(position, text):
    if position + 1 < len(text):

        suggested_operator = text[position:position + 2]

        if suggested_operator == '++' or \
            suggested_operator == '--' or \
            suggested_operator == '+=' or \
            suggested_operator == '-=' or \
            suggested_operator == '*=' or \
            suggested_operator == '/=' or \
            suggested_operator == '==' or \
            suggested_operator == '!=' or \
            suggested_operator == '>=' or \
            suggested_operator == '<=' or \
            suggested_operator == '%=' or \
            suggested_operator == '^=' or \
            suggested_operator == '..' or \
            suggested_operator == '&&' or \
            suggested_operator == '||' or \
            suggested_operator == '<<' or \
            suggested_operator == '>>' or \
            suggested_operator == '=>':

            return Lexem(LexemType.OPERATOR, position + 2, text[position:position + 2])

        suggested_operator = text[position]

        if suggested_operator == '+' or \
            suggested_operator == '-' or \
            suggested_operator == '*' or \
            suggested_operator == '/' or \
            suggested_operator == '%' or \
            suggested_operator == '<' or \
            suggested_operator == '>' or \
            suggested_operator == '!' or \
            suggested_operator == '^' or \
            suggested_operator == '~' or \
            suggested_operator == '&' or \
            suggested_operator == '|' or \
            suggested_operator == '.' or \
            suggested_operator == '=' or \
            suggested_operator == '?':

            return Lexem(LexemType.OPERATOR, position + 1, text[position:position + 1])

        return None