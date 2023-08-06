class Declaration:
    def __init__(self, declaration_type, offset, lexems):
        self.declaration_type = declaration_type
        self.offset = offset
        self.lexems = lexems

    def __str__(self):
        if self.lexems is not None and len(self.lexems) > 0:
            result = "Declaration of type '" + self.declaration_type.name + "', lexems: \n"
            for lexem in self.lexems:
                result += '\t' + lexem.__str__() + '\n'
            result += "Offset: " + str(self.offset)
            return result

    """
        # without whitespace lexems: 
        def __str__(self):
        if self.lexems is not None and len(self.lexems) > 0:
            result = "Declaration of type '" + self.declaration_type.name + "', lexems: \n"
            for lexem in self.lexems:
                if lexem.lexem_type != LexemType.WHITESPACE_SEQUENCE:
                    result += '\t' + lexem.__str__() + '\n'
            result += "Offset: " + str(self.offset)
            return result
    """