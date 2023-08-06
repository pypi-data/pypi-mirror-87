import codecs
import io
import ntpath
import os
import re

import chardet

from ccfcsharp.class_fix import ClassFix
from ccfcsharp.declaration import Declaration
from ccfcsharp.declaration_type import DeclarationType
from ccfcsharp.interface_fix import InterfaceFix
from ccfcsharp.lexem_type import LexemType
from ccfcsharp.lexer import Lexer
from ccfcsharp.naming_convention_fix import NamingConventionFix


class CodeConventionFixer:
    error_id = 0
    cs_file_extension = '.cs'
    classes_to_fix = []
    interfaces_to_fix = []
    methods_to_fix = []
    constants_to_fix = []
    variables_to_fix = []
    parameters_to_fix = []
    properties_to_fix = []

    # current_lexem_position is for lexem to check for being type identifier
    @staticmethod
    def handle_var_prop_method_ending(lexems, current_lexem_position, declarations, additional_lexems = 0):
        res = CodeConventionFixer.is_variable_type_lexem(lexems[current_lexem_position],
                                                         current_lexem_position, lexems)
        if len(res) > 0:
            # constructor path
            if len(res) == 1 and CodeConventionFixer.is_next_open_parenthesis(lexems, current_lexem_position):
                declarations.append(Declaration(DeclarationType.METHOD,
                                                lexems[current_lexem_position + 2].offset,
                                                lexems[
                                                current_lexem_position - additional_lexems:current_lexem_position + 3]))
                return 3
            elif lexems[current_lexem_position + 1 + len(res) - 1].value == '[':
                if CodeConventionFixer.is_next_open_brace(lexems, current_lexem_position + 3 + len(res)):
                    declarations.append(Declaration(DeclarationType.PROPERTY,
                                                    lexems[current_lexem_position + 6 + len(res) - 1].offset,
                                                    lexems[
                                                    current_lexem_position - additional_lexems:current_lexem_position + 7 + len(res) - 1]))
                    return 7 + len(res) - 1
                elif CodeConventionFixer.is_next_open_parenthesis(lexems, current_lexem_position + 3 + len(res)):
                    declarations.append(Declaration(DeclarationType.METHOD,
                                                    lexems[current_lexem_position + 6 + len(res) - 1].offset,
                                                    lexems[
                                                    current_lexem_position - additional_lexems:current_lexem_position + 7 + len(
                                                        res) - 1]))
                    return 7 + len(res) - 1
                else:

                    declarations.append(Declaration(DeclarationType.VARIABLE,
                                                    lexems[current_lexem_position + 4 + len(res) - 1].offset,
                                                    lexems[
                                                    current_lexem_position - additional_lexems:current_lexem_position + 5 + len(res) - 1]))
                    return 5 + len(res) - 1
            else:
                if CodeConventionFixer.is_next_open_brace(lexems, current_lexem_position + 1 + len(res)):
                    declarations.append(Declaration(DeclarationType.PROPERTY,
                                                    lexems[current_lexem_position + 4 + len(res) - 1].offset,
                                                    lexems[
                                                    current_lexem_position - additional_lexems:current_lexem_position + 5 + len(res) - 1]))
                    return 5 + len(res) - 1
                elif CodeConventionFixer.is_next_open_parenthesis(lexems, current_lexem_position + 1 + len(res)):
                    declarations.append(Declaration(DeclarationType.METHOD,
                                                    lexems[current_lexem_position + 4 + len(res) - 1].offset,
                                                    lexems[
                                                    current_lexem_position - additional_lexems:current_lexem_position + 5 + len(
                                                        res) - 1]))
                    return 5 + len(res) - 1
                else:
                    if lexems[current_lexem_position + 2 + len(res) - 1].lexem_type == LexemType.IDENTIFIER:
                        # if lexems[current_lexem_position + 2 + len(res) - 1 - 2] - type
                        # check after type static and before static and so on if we have constant (btw with static not possible)
                        # CHECK THIS STUFF IN EVERY VARIABLE END BRANCH
                        # if lexems[current_lexem_position + 2 + len(res) - 1 - 4].value == 'readonly'
                        declarations.append(Declaration(DeclarationType.VARIABLE,
                                                        lexems[current_lexem_position + 2 + len(res) - 1].offset,
                                                        lexems[current_lexem_position - additional_lexems:current_lexem_position + 3 + len(
                                                            res) - 1]))
                        return 3 + len(res) - 1
        elif lexems[current_lexem_position].value == 'void':
            declarations.append(Declaration(DeclarationType.METHOD,
                                            lexems[current_lexem_position + 4].offset,
                                            lexems[
                                            current_lexem_position - additional_lexems:current_lexem_position + 5]))
            return 5
        return 0

    # current_lexem_position is for lexem to check if the next is open brace
    @staticmethod
    def handle_var_prop_param_ending(lexems, current_lexem_position, declarations, additional_lexems = 0):
        if lexems[current_lexem_position].lexem_type != LexemType.IDENTIFIER:
            return 0

        if CodeConventionFixer.is_next_open_brace(lexems, current_lexem_position):
            declarations.append(Declaration(DeclarationType.PROPERTY,
                                            lexems[current_lexem_position + 2].offset,
                                            lexems[current_lexem_position - additional_lexems:current_lexem_position + 3]))
            return 3
        elif CodeConventionFixer.is_next_comma_or_close_parenthesis(lexems, current_lexem_position):
            declarations.append(Declaration(DeclarationType.PARAMETER,
                                            lexems[current_lexem_position].offset,
                                            lexems[current_lexem_position - additional_lexems:current_lexem_position + 1]))
            return 1
        else:
            if lexems[current_lexem_position].lexem_type == LexemType.IDENTIFIER:
                declarations.append(Declaration(DeclarationType.VARIABLE,
                                                lexems[current_lexem_position].offset,
                                                lexems[
                                                current_lexem_position - additional_lexems:current_lexem_position + 1]))
                return 1
        return 0

    @staticmethod
    def is_next_open_brace(lexems, current_lexem_position):
        return current_lexem_position + 2 < len(lexems) \
            and (lexems[current_lexem_position + 1].value == '{'
                or (lexems[current_lexem_position + 2].value == '{'
                    and lexems[current_lexem_position + 1].lexem_type == LexemType.WHITESPACE_SEQUENCE))

    @staticmethod
    def is_next_open_parenthesis(lexems, current_lexem_position):
        return current_lexem_position + 2 < len(lexems) \
            and (lexems[current_lexem_position + 1].value == '('
                or (lexems[current_lexem_position + 2].value == '('
                    and lexems[current_lexem_position + 1].lexem_type == LexemType.WHITESPACE_SEQUENCE))

    @staticmethod
    def is_next_comma_or_close_parenthesis(lexems, current_lexem_position):
        return current_lexem_position + 2 < len(lexems) \
             and (lexems[current_lexem_position + 1].value == ','
             or lexems[current_lexem_position + 1].value == ')'
             or ((lexems[current_lexem_position + 2].value == ','
             or lexems[current_lexem_position + 2].value == ')')
                  and lexems[current_lexem_position + 1].lexem_type == LexemType.WHITESPACE_SEQUENCE))

    @staticmethod
    def is_access_modifier(lexem):
        # for simplicity we don't handle fancy "protected internal", "private protected" etc.
        return lexem.value == 'public' \
                or lexem.value == 'internal' \
                or lexem.value == 'private' \
                or lexem.value == 'protected'

    """ Interfaces included """
    @staticmethod
    def is_custom_class(lexem, text):
        classes = CodeConventionFixer.find_class_declarations(text)
        for cls in classes:
            for i in range(len(cls.lexems)):
                if (cls.lexems[i].value == 'class' or cls.lexems[i].value == 'interface') and cls.lexems[i+2].value == lexem.value:
                    return True
        return False

    @staticmethod
    def is_variable_type_lexem(lexem, lexem_start, lexems):
        result = []
        if (lexem.lexem_type == LexemType.ABSOLUTE_KEYWORD
                and lexem.value == 'string') \
                or (lexem.lexem_type == LexemType.ABSOLUTE_KEYWORD
                    and lexem.value == 'float') \
                or (lexem.lexem_type == LexemType.ABSOLUTE_KEYWORD
                    and lexem.value == 'double') \
                or (lexem.lexem_type == LexemType.ABSOLUTE_KEYWORD
                    and lexem.value == 'decimal') \
                or (lexem.lexem_type == LexemType.ABSOLUTE_KEYWORD
                    and lexem.value == 'int') \
                or (lexem.lexem_type == LexemType.ABSOLUTE_KEYWORD
                    and lexem.value == 'uint') \
                or (lexem.lexem_type == LexemType.ABSOLUTE_KEYWORD
                    and lexem.value == 'ulong') \
                or (lexem.lexem_type == LexemType.ABSOLUTE_KEYWORD
                    and lexem.value == 'long') \
                or (lexem.lexem_type == LexemType.ABSOLUTE_KEYWORD
                    and lexem.value == 'ushort') \
                or (lexem.lexem_type == LexemType.ABSOLUTE_KEYWORD
                    and lexem.value == 'byte') \
                or (lexem.lexem_type == LexemType.ABSOLUTE_KEYWORD
                    and lexem.value == 'sbyte') \
                or (lexem.lexem_type == LexemType.ABSOLUTE_KEYWORD
                    and lexem.value == 'short') \
                or (lexem.lexem_type == LexemType.ABSOLUTE_KEYWORD
                    and lexem.value == 'char') \
                or (lexem.lexem_type == LexemType.ABSOLUTE_KEYWORD
                    and lexem.value == 'bool') \
                or (lexem.lexem_type == LexemType.ABSOLUTE_KEYWORD
                    and lexem.value == 'object'):
            result.append(lexem)
            return result

        current_lexem_position = lexem_start
        while current_lexem_position < len(lexems) \
                and (lexems[current_lexem_position].lexem_type == LexemType.IDENTIFIER
                     or (lexems[current_lexem_position].lexem_type == LexemType.OPERATOR
                         and lexems[current_lexem_position].value == '.')):
            current_lexem_position += 1
        if current_lexem_position != lexem_start:
            while lexem_start != current_lexem_position:
                result.append(lexems[lexem_start])
                lexem_start += 1
            return result

        return result

    """ Interfaces included """
    @staticmethod
    def find_class_declarations(lexems):
        declarations = []

        #lexems = Lexer.lex(text)
        current_lexem_position = 0

        while current_lexem_position < len(lexems):
            current_lexem = lexems[current_lexem_position]

            if CodeConventionFixer.is_access_modifier(current_lexem):
                # +2 because of the expected whitespace sequence between semantic lexems
                if lexems[current_lexem_position + 2].value == 'class':
                    declarations.append(Declaration(DeclarationType.CLASS,
                                                    lexems[current_lexem_position + 4].offset,
                                                    lexems[current_lexem_position:current_lexem_position + 5]))
                    current_lexem_position += 5
                elif lexems[current_lexem_position + 2].value == 'interface':
                    declarations.append(Declaration(DeclarationType.INTERFACE,
                                                    lexems[current_lexem_position + 4].offset,
                                                    lexems[current_lexem_position:current_lexem_position + 5]))
                    current_lexem_position += 5
                elif lexems[current_lexem_position + 2].value == 'static' \
                    and lexems[current_lexem_position + 4].value == 'class':
                    declarations.append(Declaration(DeclarationType.CLASS,
                                                    lexems[current_lexem_position + 6].offset,
                                                    lexems[current_lexem_position:current_lexem_position + 7]))
                    current_lexem_position += 7

            current_lexem_position += 1

        return declarations

    # UNUSED
    # finds variables of "non-primitive" classes
    @staticmethod
    def find_class_identifiers(lexems):
        identifiers = []

        #lexems = Lexer.lex(text)
        current_lexem_position = 0

        while current_lexem_position < len(lexems):
            current_lexem = lexems[current_lexem_position]

			#CSharp.Action action = new Action();
			#Action action1;

            #start_position = current_lexem_position
            while current_lexem_position < len(lexems) \
                    and lexems[current_lexem_position].lexem_type != LexemType.IDENTIFIER:
                current_lexem_position += 1

            # find type
            start_position = current_lexem_position
            while current_lexem_position < len(lexems) \
                    and (lexems[current_lexem_position].lexem_type == LexemType.IDENTIFIER
                        or (lexems[current_lexem_position].lexem_type == LexemType.OPERATOR
                        and lexems[current_lexem_position].value == '.')):
                current_lexem_position += 1

            # find identifier
            if current_lexem_position + 1 < len(lexems) \
                    and lexems[current_lexem_position].lexem_type == LexemType.WHITESPACE_SEQUENCE \
                    and lexems[current_lexem_position + 1].lexem_type == LexemType.IDENTIFIER:
                if current_lexem_position + 2 < len(lexems) \
                    and lexems[current_lexem_position + 2].lexem_type == LexemType.WHITESPACE_SEQUENCE \
                    and current_lexem_position + 3 < len(lexems):
                    current_lexem_position += 1
                if ((lexems[current_lexem_position + 2].lexem_type == LexemType.OPERATOR
                    and lexems[current_lexem_position + 2].value == '=')
                or (lexems[current_lexem_position + 2].lexem_type == LexemType.SEPARATOR
                    and lexems[current_lexem_position + 2].value == ';')):

                    # TODO: check if it is class field
                    identifiers.append(Declaration(DeclarationType.VARIABLE,
                                                    lexems[current_lexem_position + 2].offset,
                                                    lexems[start_position:current_lexem_position + 3]))

            current_lexem_position += 1

        return identifiers

    # at this moment, we don't handle events and delegates
    @staticmethod
    def find_declarations(lexems):
        declarations = []

        #lexems = Lexer.lex(text)
        current_lexem_position = 0

        while current_lexem_position < len(lexems):
            current_lexem = lexems[current_lexem_position]
            if CodeConventionFixer.is_access_modifier(current_lexem):
                # +2 because of the expected whitespace sequence between semantic lexems
                # after class modifiers we cannot have 'var'
                if lexems[current_lexem_position + 2].value == 'static' \
                        or lexems[current_lexem_position + 2].value == 'const':
                    current_lexem_position += CodeConventionFixer.handle_var_prop_method_ending(lexems,
                                                                                                current_lexem_position + 4,
                                                                                                declarations, 4) + 4
                else:
                    current_lexem_position += CodeConventionFixer.handle_var_prop_method_ending(lexems,
                                                                                                current_lexem_position + 2,
                                                                                                declarations, 2) + 2
            elif current_lexem_position + 4 < len(lexems) and \
                    (lexems[current_lexem_position].value == 'static'
                    or lexems[current_lexem_position].value == 'const'):
                current_lexem_position += CodeConventionFixer.handle_var_prop_method_ending(lexems,
                                                                                            current_lexem_position + 2,
                                                                                            declarations, 2) + 2

            elif current_lexem.lexem_type == LexemType.CONTEXTUAL_KEYWORD \
                and current_lexem.value == 'var':
                declarations.append(Declaration(DeclarationType.VARIABLE,
                                                lexems[current_lexem_position + 2].offset,
                                                lexems[current_lexem_position:current_lexem_position + 3]))
                current_lexem_position += 3

            # only this branch can result in method parameter
            else:
                res = CodeConventionFixer.is_variable_type_lexem(lexems[current_lexem_position],
                                                                 current_lexem_position, lexems)
                if len(res) > 0:
                    if lexems[current_lexem_position + 1 + len(res) - 1].value == '[':
                        current_lexem_position += len(res) + 3 + CodeConventionFixer.handle_var_prop_param_ending\
                            (lexems, current_lexem_position + 3 + len(res), declarations, 3 + len(res))
                    elif lexems[current_lexem_position + 1 + len(res) - 1].lexem_type == LexemType.WHITESPACE_SEQUENCE:
                        current_lexem_position += len(res) + 1 + CodeConventionFixer.handle_var_prop_param_ending\
                            (lexems, current_lexem_position + 1 + len(res), declarations, 1 + len(res))

            current_lexem_position += 1

        return declarations

    # Well, at this moment, no static imports...
    @staticmethod
    def find_using_directives(lexems):
        declarations = []

        #lexems = Lexer.lex(text)
        current_lexem_position = 0

        while current_lexem_position < len(lexems):
            current_lexem = lexems[current_lexem_position]

            # here we should make sure we won't touch disposable using constructions
            if current_lexem.value == 'using' and \
                lexems[current_lexem_position + 2].lexem_type == LexemType.IDENTIFIER:
                start_lexem_position = current_lexem_position
                while current_lexem.value != ';':
                    current_lexem_position += 1
                    current_lexem = lexems[current_lexem_position]
                declarations.append(Declaration(DeclarationType.USING,
                                                lexems[current_lexem_position].offset,
                                                lexems[start_lexem_position:current_lexem_position + 1]))

            current_lexem_position += 1

        return declarations

    @staticmethod
    def find_namespace_declarations(lexems):
        declarations = []

        #lexems = Lexer.lex(text)
        current_lexem_position = 0

        while current_lexem_position < len(lexems):
            current_lexem = lexems[current_lexem_position]

            if current_lexem.value == 'namespace':
                start_lexem_position = current_lexem_position
                while current_lexem.value != '{':
                    current_lexem_position += 1
                    current_lexem = lexems[current_lexem_position]
                declarations.append(Declaration(DeclarationType.NAMESPACE,
                                                lexems[current_lexem_position - 1].offset,
                                                lexems[start_lexem_position:current_lexem_position]))

            current_lexem_position += 1

        return declarations

    @staticmethod
    def is_camel_case(value: str):
        result = re.match(r'[a-z]+((\d)|([A-Z0-9][a-z0-9]+))*([A-Z])?', value)
        return (result is not None and result.start() == 0 and result.end() == len(value))

    @staticmethod
    def is_pascal_case(value: str):
        result = re.match(r'([A-Z][a-z0-9]+)((\d)|([A-Z0-9][a-z0-9]+))*([A-Z])?', value)
        return (result is not None and result.start() == 0 and result.end() == len(value))

    @staticmethod
    def get_error_msg(filepath, offset, text):
        CodeConventionFixer.error_id = CodeConventionFixer.error_id + 1
        return '#' + str(CodeConventionFixer.error_id) + ': File Path: ' + \
                filepath + '. Offset: ' + str(offset) + '. Error: ' + text + '\n'

    @staticmethod
    def to_camel_case(value: str):
        new_name = ""
        current_case = -1  # symb = 0, digit = 1, lower = 2, upper = 3
        for letter in value:
            if letter.isalpha():
                if letter.isupper():
                    if current_case == 3 or current_case == -1:
                        new_name += letter.lower()
                    else:
                        new_name += letter
                    current_case = 3
                elif letter.lower():
                    if current_case == 0 or current_case == 1:
                        new_name += letter.upper()
                    else:
                        new_name += letter
                    current_case = 2
            elif letter.isnumeric():
                new_name += letter
                current_case = 1
            else:
                current_case = 0
        return new_name

    @staticmethod
    def to_pascal_case(value: str):
        new_name = ""
        current_case = -1  # symb = 0, digit = 1, lower = 2, upper = 3
        for letter in value:
            if letter.isalpha():
                if letter.isupper():
                    if current_case == 3:
                        new_name += letter.lower()
                    else:
                        new_name += letter
                    current_case = 3
                elif letter.lower():
                    if current_case == 0 or current_case == 1:
                        new_name += letter.upper()
                        current_case = 2
                    elif current_case == -1:
                        new_name += letter.upper()
                        current_case = 3
                    else:
                        new_name += letter
                        current_case = 2

            elif letter.isnumeric():
                new_name += letter
                current_case = 1
            else:
                current_case = 0
        return new_name

    @staticmethod
    def verify_project_conventions(project_path):
        files_to_analyze = []
        for root, dirs, files in os.walk(project_path):
            for file in files:
                if file.endswith(CodeConventionFixer.cs_file_extension):
                    files_to_analyze.append(os.path.join(root, file))
                    #print(os.path.join(root, file))

        for file in files_to_analyze:
            CodeConventionFixer.verify_file_conventions(file)

    @staticmethod
    def verify_directory_conventions(directory_path):
        files_to_analyze = []
        for file in os.listdir(directory_path):
            if file.endswith(CodeConventionFixer.cs_file_extension):
                files_to_analyze.append(os.path.join(directory_path, file))
                #print(os.path.join(directory_path, file))

        for file in files_to_analyze:
            CodeConventionFixer.verify_file_conventions(file)

    @staticmethod
    def verify_file_conventions(file_path):

        bytes = min(32, os.path.getsize(file_path))
        raw = open(file_path, 'rb').read(bytes)

        if raw.startswith(codecs.BOM_UTF8):
            encoding = 'utf-8-sig'
        else:
            result = chardet.detect(raw)
            encoding = result['encoding']

        f = io.open(file_path, 'r', encoding=encoding)
        text = f.read()
        f.close()

        lexems = Lexer.lex(text)

        # index all lexems for future convs fixing "just-in-lexem"
        for i, lexem in enumerate(lexems, start=0):
            lexem.number = i
            #print("Lexem {}: {}".format(i, lexem.number))

        usings = CodeConventionFixer.find_using_directives(lexems)
        classes_interfaces = CodeConventionFixer.find_class_declarations(lexems)
        namespaces = CodeConventionFixer.find_namespace_declarations(lexems)
        decls = CodeConventionFixer.find_declarations(lexems)
        methods = []
        variables = []
        parameters = []
        props = []
        classes = []
        interfaces = []
        constants = []
        non_constants = []

        for item in classes_interfaces:
            if item.declaration_type == DeclarationType.CLASS:
                classes.append(item)
            else:
                interfaces.append(item)

        for dec in decls:
            if dec.declaration_type == DeclarationType.METHOD:
                methods.append(dec)
            elif dec.declaration_type == DeclarationType.VARIABLE:
                variables.append(dec)
            elif dec.declaration_type == DeclarationType.PARAMETER:
                parameters.append(dec)
            elif dec.declaration_type == DeclarationType.PROPERTY:
                props.append(dec)

        for item in variables:
            if item.lexems[0].value == 'const' or item.lexems[2].value == 'const':
                constants.append(item)
                item.declaration_type = DeclarationType.CONSTANT
            else:
                non_constants.append(item)

        f = open(file_path + '_verification.log', 'w')
        f.write(file_path + ' VERIFICATION LOG\n')

        filename = ntpath.basename(file_path)
        if not CodeConventionFixer.is_pascal_case(filename[0:(len(filename) - len(CodeConventionFixer.cs_file_extension))]):
            f.write(CodeConventionFixer.get_error_msg(file_path, -1,
                                                      'Filename is not in pascal case: ' + filename))

        #print('\nUsings: =====================================\n')
        #for item in usings:
        #    print(item)

        #print('\nNamespaces: =====================================\n')
        for item in namespaces:
            #print(item)
            for lexem in item.lexems:
                if lexem.lexem_type == LexemType.IDENTIFIER and not CodeConventionFixer.is_pascal_case(lexem.value):
                    f.write(CodeConventionFixer.get_error_msg(file_path, lexem.offset,
                                                              'Namespace part is not in pascal case: ' + lexem.value))

        #print('\nClasses: =====================================\n')
        for item in classes:
            #print(item)
            if not CodeConventionFixer.is_pascal_case(item.lexems[len(item.lexems) - 1].value):
                f.write(CodeConventionFixer.get_error_msg(file_path, item.lexems[len(item.lexems) - 1].offset,
                                                          'Class name is not in pascal case: ' + item.lexems[len(item.lexems) - 1].value))

        #print('\nInterfaces: =====================================\n')
        for item in interfaces:
            #print(item)
            name = item.lexems[len(item.lexems) - 1].value
            if not name[0] == 'I':
                f.write(CodeConventionFixer.get_error_msg(file_path, item.lexems[len(item.lexems) - 1].offset,
                                                          'Interface name doesn\'t start with \'I\': ' + name))
                if not CodeConventionFixer.is_pascal_case(name):
                    f.write(CodeConventionFixer.get_error_msg(file_path, item.lexems[len(item.lexems) - 1].offset,
                                                              'Interface name is not in pascal case: ' + name))

            elif not CodeConventionFixer.is_pascal_case(name[1:len(name)]):
                f.write(CodeConventionFixer.get_error_msg(file_path, item.lexems[len(item.lexems) - 1].offset,
                                                          'Interface name is not in pascal case: ' + name))

        #print('\nMethods: =====================================\n')
        for item in methods:
            #print(item)
            name = item.lexems[len(item.lexems) - 3].value
            if not CodeConventionFixer.is_pascal_case(name):
                f.write(CodeConventionFixer.get_error_msg(file_path, item.lexems[len(item.lexems) - 3].offset,
                                                          'Method name is not in pascal case: ' + name))

        #print('\nConstants: =====================================\n')
        for item in constants:
            #print(item)
            name = item.lexems[len(item.lexems) - 1].value
            if not CodeConventionFixer.is_pascal_case(name):
                f.write(CodeConventionFixer.get_error_msg(file_path, item.lexems[len(item.lexems) - 1].offset,
                                                          'Constant name is not in pascal case: ' + name))

        #print('\nVariables: =====================================\n')
        for item in non_constants:
            #print(item)
            name = item.lexems[len(item.lexems) - 1].value
            if not CodeConventionFixer.is_camel_case(name):
                f.write(CodeConventionFixer.get_error_msg(file_path, item.lexems[len(item.lexems) - 1].offset,
                                                          'Variable name is not in camel case: ' + name))

        #print('\nParameters: =====================================\n')
        for item in parameters:
            #print(item)
            name = item.lexems[len(item.lexems) - 1].value
            if not CodeConventionFixer.is_camel_case(name):
                f.write(CodeConventionFixer.get_error_msg(file_path, item.lexems[len(item.lexems) - 1].offset,
                                                          'Method parameter name is not in camel case: ' + name))

        #print('\nProps: =====================================\n')
        for item in props:
            #print(item)
            name = item.lexems[len(item.lexems) - 3].value
            if not CodeConventionFixer.is_pascal_case(name):
                f.write(CodeConventionFixer.get_error_msg(file_path, item.lexems[len(item.lexems) - 3].offset,
                                                          'Property name is not in pascal case: ' + name))

        f.close()

    @staticmethod
    def get_namespace_name(namespace_declaration: Declaration):
        namespace_name = ''
        i = 2
        while i < len(namespace_declaration.lexems) - 1:
            namespace_name += namespace_declaration.lexems[i].value
            i += 1
        return namespace_name

    @staticmethod
    def get_file_text(file_path):
        bytes = min(32, os.path.getsize(file_path))
        raw = open(file_path, 'rb').read(bytes)

        if raw.startswith(codecs.BOM_UTF8):
            encoding = 'utf-8-sig'
        else:
            result = chardet.detect(raw)
            encoding = result['encoding']

        f = io.open(file_path, 'r', encoding=encoding)
        text = f.read()
        f.close()

        return text

    @staticmethod
    def clear_convention_violations():
        CodeConventionFixer.classes_to_fix = []
        CodeConventionFixer.interfaces_to_fix = []
        CodeConventionFixer.methods_to_fix = []
        CodeConventionFixer.constants_to_fix = []
        CodeConventionFixer.variables_to_fix = []
        CodeConventionFixer.parameters_to_fix = []
        CodeConventionFixer.properties_to_fix = []

    @staticmethod
    def find_convention_violations_in_project(project_path):
        files_to_analyze = []
        for root, dirs, files in os.walk(project_path):
            for file in files:
                if file.endswith(CodeConventionFixer.cs_file_extension):
                    files_to_analyze.append(os.path.join(root, file))

        CodeConventionFixer.clear_convention_violations()

        for file in files_to_analyze:
            CodeConventionFixer.internal_find_convention_violations_in_file(file)

    @staticmethod
    def find_convention_violations_in_directory(directory_path):
        files_to_analyze = []
        for file in os.listdir(directory_path):
            if file.endswith(CodeConventionFixer.cs_file_extension):
                files_to_analyze.append(os.path.join(directory_path, file))

        CodeConventionFixer.clear_convention_violations()

        for file in files_to_analyze:
            CodeConventionFixer.internal_find_convention_violations_in_file(file)

    @staticmethod
    def find_convention_violations_in_file(file_path):

        CodeConventionFixer.clear_convention_violations()
        CodeConventionFixer.internal_find_convention_violations_in_file(file_path)

    @staticmethod
    def internal_find_convention_violations_in_file(file_path):

        # somewhere upper in call stack we should do found violations clearing

        text = CodeConventionFixer.get_file_text(file_path)
        lexems = Lexer.lex(text)
        classes_interfaces = CodeConventionFixer.find_class_declarations(lexems)
        classes = []
        interfaces = []
        namespaces = CodeConventionFixer.find_namespace_declarations(lexems)
        namespace_name = CodeConventionFixer.get_namespace_name(namespaces[0])

        declarations = CodeConventionFixer.find_declarations(lexems)

        constants = []
        variables = []
        parameters = []
        methods = []
        props = []

        for dec in declarations:
            if dec.declaration_type == DeclarationType.METHOD:
                methods.append(dec)
            elif dec.declaration_type == DeclarationType.VARIABLE:
                if dec.lexems[0].value == 'const' or dec.lexems[2].value == 'const':
                    constants.append(dec)
                    dec.declaration_type = DeclarationType.CONSTANT
                else:
                    variables.append(dec)
            elif dec.declaration_type == DeclarationType.PARAMETER:
                parameters.append(dec)
            elif dec.declaration_type == DeclarationType.PROPERTY:
                props.append(dec)

        for item in classes_interfaces:
            if item.declaration_type == DeclarationType.CLASS:
                classes.append(item)
            else:
                interfaces.append(item)

        # Adding this file class naming fixes to classes_to_fix
        for item in classes:
            name = item.lexems[len(item.lexems) - 1].value
            if not CodeConventionFixer.is_pascal_case(name):
                new_name = CodeConventionFixer.to_pascal_case(name)
                CodeConventionFixer.classes_to_fix.append(ClassFix(namespace_name, name, new_name))

        # Adding this file class naming fixes to interfaces_to_fix
        for item in interfaces:
            name = item.lexems[len(item.lexems) - 1].value
            if not name[0] == 'I':
                msg = 'Interface name doesn\'t start with \'I\''
                new_name = 'I' + name
                isInPascal = CodeConventionFixer.is_pascal_case(name)
                if not isInPascal:
                    new_name = 'I' + CodeConventionFixer.to_pascal_case(name)
                    msg += ' and is not in pascal case: ' + name + '. Fixed to: ' + new_name
                else:
                    msg += ': ' + name + '. Fixed to: ' + new_name

                CodeConventionFixer.interfaces_to_fix.append(InterfaceFix(namespace_name, name, new_name, msg))

            elif not CodeConventionFixer.is_pascal_case(name[1:len(name)]):
                new_name = 'I' + CodeConventionFixer.to_pascal_case(name[1:len(name)])
                msg = 'Interface name is not in pascal case: ' + name + '. Fixed to: ' + new_name
                CodeConventionFixer.interfaces_to_fix.append(InterfaceFix(namespace_name, name, new_name, msg))

        # Adding this file method naming fixes to methods_to_fix
        for item in methods:
            name = item.lexems[len(item.lexems) - 3].value
            if not CodeConventionFixer.is_pascal_case(name):
                new_name = CodeConventionFixer.to_pascal_case(name)
                msg = 'Method name is not in pascal case: ' + name + '. Fixed to: ' + new_name
                CodeConventionFixer.methods_to_fix.append(NamingConventionFix(namespace_name, name, new_name, msg))

        # Adding this file constant naming fixes to constants_to_fix
        for item in constants:
            name = item.lexems[len(item.lexems) - 1].value
            if not CodeConventionFixer.is_pascal_case(name):
                new_name = CodeConventionFixer.to_pascal_case(name)
                msg = 'Constant name is not in pascal case: ' + name + '. Fixed to: ' + new_name
                CodeConventionFixer.constants_to_fix.append(NamingConventionFix(namespace_name, name, new_name, msg))

        # Adding this file variable naming fixes to variables_to_fix
        for item in variables:
            name = item.lexems[len(item.lexems) - 1].value
            old_name = name
            if not CodeConventionFixer.is_camel_case(name):
                if name[0] == '_':
                    name = name[1:len(name)]
                new_name = CodeConventionFixer.to_camel_case(name)
                msg = 'Variable name is not in camel case: ' + old_name + '. Fixed to: ' + new_name
                CodeConventionFixer.variables_to_fix.append(NamingConventionFix(namespace_name, name, new_name, msg))

        # Adding this file parameter naming fixes to parameters_to_fix
        for item in parameters:
            name = item.lexems[len(item.lexems) - 1].value
            old_name = name
            if not CodeConventionFixer.is_camel_case(name):
                if name[0] == '_':
                    name = name[1:len(name)]
                new_name = CodeConventionFixer.to_camel_case(name)
                msg = 'Method parameter name is not in camel case: ' + old_name + '. Fixed to: ' + new_name
                CodeConventionFixer.parameters_to_fix.append(NamingConventionFix(namespace_name, name, new_name, msg))

        # Adding this file properties naming fixes to properties_to_fix
        for item in props:
            name = item.lexems[len(item.lexems) - 3].value
            if not CodeConventionFixer.is_pascal_case(name):
                new_name = CodeConventionFixer.to_pascal_case(name)
                msg = 'Property name is not in pascal case: ' + name + '. Fixed to: ' + new_name
                CodeConventionFixer.properties_to_fix.append(NamingConventionFix(namespace_name, name, new_name, msg))

    @staticmethod
    def internal_fix_file_conventions(file_path):

        text = CodeConventionFixer.get_file_text(file_path)
        lexems = Lexer.lex(text)

        fixing_log = open(file_path + '_fixing.log', 'w')
        fixing_log.write(file_path + ' FIXING LOG\n')

        namespaces = CodeConventionFixer.find_namespace_declarations(lexems)
        namespace_name = CodeConventionFixer.get_namespace_name(namespaces[0])
        usings = CodeConventionFixer.find_using_directives(lexems)
        using_namespaces = []
        for using in usings:
            name = CodeConventionFixer.get_namespace_name(using)
            using_namespaces.append(name)

        new_file = open(file_path[0:len(file_path) - len(CodeConventionFixer.cs_file_extension)] + '_fixed.cs', 'w')

        for class_to_fix in CodeConventionFixer.classes_to_fix:
            if namespace_name == class_to_fix.namespace or class_to_fix.namespace in using_namespaces:
                for lexem in lexems:
                    if lexem.value == class_to_fix.old_class_name:
                        lexem.value = class_to_fix.new_class_name
                        fixing_log.write(CodeConventionFixer.get_error_msg(file_path, lexem.offset,
                                                                           'Class name is not in pascal case: ' +
                                                                           class_to_fix.old_class_name +
                                                                           '. Fixed to: ' +
                                                                           class_to_fix.new_class_name
                                                                           ))

        for interface in CodeConventionFixer.interfaces_to_fix:
            if namespace_name == interface.namespace or interface.namespace in using_namespaces:
                for lexem in lexems:
                    if lexem.value == interface.old_name:
                        lexem.value = interface.new_name
                        fixing_log.write(CodeConventionFixer.get_error_msg(file_path, lexem.offset, interface.message))

        for method in CodeConventionFixer.methods_to_fix:
            if namespace_name == method.namespace or method.namespace in using_namespaces:
                for lexem in lexems:
                    if lexem.value == method.old_name:
                        lexem.value = method.new_name
                        fixing_log.write(CodeConventionFixer.get_error_msg(file_path, lexem.offset, method.message))

        for property in CodeConventionFixer.properties_to_fix:
            if namespace_name == property.namespace or property.namespace in using_namespaces:
                for lexem in lexems:
                    if lexem.value == property.old_name:
                        lexem.value = property.new_name
                        fixing_log.write(CodeConventionFixer.get_error_msg(file_path, lexem.offset, property.message))

        for constant in CodeConventionFixer.constants_to_fix:
            if namespace_name == constant.namespace or constant.namespace in using_namespaces:
                for lexem in lexems:
                    if lexem.value == constant.old_name:
                        lexem.value = constant.new_name
                        fixing_log.write(CodeConventionFixer.get_error_msg(file_path, lexem.offset, constant.message))

        for variable in CodeConventionFixer.variables_to_fix:
            if namespace_name == variable.namespace or variable.namespace in using_namespaces:
                for lexem in lexems:
                    if lexem.value == variable.old_name:
                        lexem.value = variable.new_name
                        fixing_log.write(CodeConventionFixer.get_error_msg(file_path, lexem.offset, variable.message))

        for parameter in CodeConventionFixer.parameters_to_fix:
            if namespace_name == parameter.namespace or parameter.namespace in using_namespaces:
                for lexem in lexems:
                    if lexem.value == parameter.old_name:
                        lexem.value = parameter.new_name
                        fixing_log.write(CodeConventionFixer.get_error_msg(file_path, lexem.offset, parameter.message))


        for lexem in lexems:
            new_file.write(lexem.value)

    @staticmethod
    def fix_file_conventions(file_path):

        CodeConventionFixer.find_convention_violations_in_file(file_path)
        CodeConventionFixer.internal_fix_file_conventions(file_path)

    @staticmethod
    def fix_directory_conventions(directory_path):

        CodeConventionFixer.find_convention_violations_in_directory(directory_path)

        files_to_fix = []
        for file in os.listdir(directory_path):
            if file.endswith(CodeConventionFixer.cs_file_extension):
                files_to_fix.append(os.path.join(directory_path, file))

        for file in files_to_fix:
            CodeConventionFixer.internal_fix_file_conventions(file)

    @staticmethod
    def fix_project_conventions(project_path):

        CodeConventionFixer.find_convention_violations_in_project(project_path)

        files_to_fix = []
        for root, dirs, files in os.walk(project_path):
            for file in files:
                if file.endswith(CodeConventionFixer.cs_file_extension):
                    files_to_fix.append(os.path.join(root, file))

        for file in files_to_fix:
            CodeConventionFixer.internal_fix_file_conventions(file)

    @staticmethod
    def fix_file_conventions_old(file_path):

        text = CodeConventionFixer.get_file_text(file_path)

        lexems = Lexer.lex(text)

        usings = CodeConventionFixer.find_using_directives(lexems)
        classes_interfaces = CodeConventionFixer.find_class_declarations(lexems)
        namespaces = CodeConventionFixer.find_namespace_declarations(lexems)
        decls = CodeConventionFixer.find_declarations(lexems)
        methods = []
        variables = []
        parameters = []
        props = []
        classes = []
        interfaces = []
        constants = []
        non_constants = []

        for item in classes_interfaces:
            if item.declaration_type == DeclarationType.CLASS:
                classes.append(item)
            else:
                interfaces.append(item)

        for dec in decls:
            if dec.declaration_type == DeclarationType.METHOD:
                methods.append(dec)
            elif dec.declaration_type == DeclarationType.VARIABLE:
                variables.append(dec)
            elif dec.declaration_type == DeclarationType.PARAMETER:
                parameters.append(dec)
            elif dec.declaration_type == DeclarationType.PROPERTY:
                props.append(dec)

        for item in variables:
            if item.lexems[0].value == 'const' or item.lexems[2].value == 'const':
                constants.append(item)
                item.declaration_type = DeclarationType.CONSTANT
            else:
                non_constants.append(item)

        f = open(file_path + '_fixing.log', 'w')
        f.write(file_path + ' FIXING LOG\n')

        filename = ntpath.basename(file_path)
        if not CodeConventionFixer.is_pascal_case(
                filename[0:(len(filename) - len(CodeConventionFixer.cs_file_extension))]):
            f.write(CodeConventionFixer.get_error_msg(file_path, -1,
                                                      'Filename is not in pascal case: ' + filename))

        # print('\nUsings: =====================================\n')
        # for item in usings:
        #    print(item)

        '''
        print('\nNamespaces: =====================================\n')
        for item in namespaces:
            # print(item)
            for lexem in item.lexems:
                if lexem.lexem_type == LexemType.IDENTIFIER and not CodeConventionFixer.is_pascal_case(lexem.value):
                    f.write(CodeConventionFixer.get_error_msg(file_path, lexem.offset,
                                                              'Namespace part is not in pascal case: ' + lexem.value))
        '''

        print('\nClasses: =====================================\n')
        # fixing class naming convs in THIS file, adding these convs fixes to classes_to_fix
        # Better would be:
        # Adding THIS file convs fixes to classes_to_fix
        for item in classes:
            # print(item)
            name = item.lexems[len(item.lexems) - 1].value
            if not CodeConventionFixer.is_pascal_case(name):
                new_name = CodeConventionFixer.to_pascal_case(name)
                #f.write(CodeConventionFixer.get_error_msg(file_path, item.lexems[len(item.lexems) - 1].offset,
                #                                          'Class name is not in pascal case: ' + name +
                #                                          '. Fixed to: ' + new_name))
                #new_file = open(file_path[0:len(file_path)-len(CodeConventionFixer.cs_file_extension)] + '_fixed.cs', 'w')
                #item.lexems[len(item.lexems) - 1].value = new_name

                #for lexem in lexems:
                    #print(lexem)
                    #if lexem.value == name:
                        #lexem.value = new_name
                        #f.write(CodeConventionFixer.get_error_msg(file_path, lexem.offset,
                        #                                          'Class name is not in pascal case: ' + name +
                        #                                          '. Fixed to: ' + new_name))
                    #new_file.write(lexem.value)
                #new_file.close()

                namespace_name = CodeConventionFixer.get_namespace_name(namespaces[0])

                CodeConventionFixer.classes_to_fix.append(ClassFix(namespace_name, name, new_name))
                #print(ClassFix(namespace_name, name, new_name))

                '''
                2) затречим все переменные этого класса
                3) затречим все вызовы методов и пропов этого КЛАССА (статики)
                4) затречим все вызовы методов и пропов ПЕРЕМЕННЫХ этого класса (экземплярные)
                '''

        print('\nInterfaces: =====================================\n')
        for item in interfaces:
            # print(item)
            name = item.lexems[len(item.lexems) - 1].value
            if not name[0] == 'I':
                msg = 'Interface name doesn\'t start with \'I\''
                new_name = 'I' + name
                isInPascal = CodeConventionFixer.is_pascal_case(name)
                if not isInPascal:
                    new_name = 'I' + CodeConventionFixer.to_pascal_case(name)
                    msg += ' and is not in pascal case: ' + name + '. Fixed to: ' + new_name
                else:
                    msg += ': ' + name + '. Fixed to: ' + new_name

                f.write(CodeConventionFixer.get_error_msg(file_path, item.lexems[len(item.lexems) - 1].offset, msg))

            elif not CodeConventionFixer.is_pascal_case(name[1:len(name)]):
                new_name = 'I' + CodeConventionFixer.to_pascal_case(name[1:len(name)])
                f.write(CodeConventionFixer.get_error_msg(file_path, item.lexems[len(item.lexems) - 1].offset,
                                                          'Interface name is not in pascal case: ' + name +
                                                          '. Fixed to: ' + new_name))

        print('\nMethods: =====================================\n')
        for item in methods:
            # print(item)
            name = item.lexems[len(item.lexems) - 3].value
            if not CodeConventionFixer.is_pascal_case(name):
                new_name = CodeConventionFixer.to_pascal_case(name)
                f.write(CodeConventionFixer.get_error_msg(file_path, item.lexems[len(item.lexems) - 3].offset,
                                                          'Method name is not in pascal case: ' + name +
                                                          '. Fixed to: ' + new_name))

        print('\nConstants: =====================================\n')
        for item in constants:
            # print(item)
            name = item.lexems[len(item.lexems) - 1].value
            if not CodeConventionFixer.is_pascal_case(name):
                new_name = CodeConventionFixer.to_pascal_case(name)
                f.write(CodeConventionFixer.get_error_msg(file_path, item.lexems[len(item.lexems) - 1].offset,
                                                          'Constant name is not in pascal case: ' + name +
                                                          '. Fixed to: ' + new_name))

        print('\nVariables: =====================================\n')
        for item in non_constants:
            # print(item)
            name = item.lexems[len(item.lexems) - 1].value
            old_name = name
            if not CodeConventionFixer.is_camel_case(name):
                if name[0] == '_':
                    name = name[1:len(name)]
                new_name = CodeConventionFixer.to_camel_case(name)
                f.write(CodeConventionFixer.get_error_msg(file_path, item.lexems[len(item.lexems) - 1].offset,
                                                          'Variable name is not in camel case: ' + old_name +
                                                          '. Fixed to: ' + new_name))

        print('\nParameters: =====================================\n')
        for item in parameters:
            # print(item)
            name = item.lexems[len(item.lexems) - 1].value
            old_name = name
            if not CodeConventionFixer.is_camel_case(name):
                if name[0] == '_':
                    name = name[1:len(name)]
                new_name = CodeConventionFixer.to_camel_case(name)
                f.write(CodeConventionFixer.get_error_msg(file_path, item.lexems[len(item.lexems) - 1].offset,
                                                          'Method parameter name is not in camel case: ' + old_name +
                                                          '. Fixed to: ' + new_name))

        print('\nProps: =====================================\n')
        for item in props:
            # print(item)
            name = item.lexems[len(item.lexems) - 3].value
            if not CodeConventionFixer.is_pascal_case(name):
                new_name = CodeConventionFixer.to_pascal_case(name)
                f.write(CodeConventionFixer.get_error_msg(file_path, item.lexems[len(item.lexems) - 3].offset,
                                                          'Property name is not in pascal case: ' + name +
                                                          '. Fixed to: ' + new_name))

        f.close()