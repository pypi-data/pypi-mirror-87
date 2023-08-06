class Lexem:
    def __init__(self, lexem_type, offset, value=None):
        self.lexem_type = lexem_type
        self.offset = offset
        self.value = value

    def __str__(self):
        if self.value is not None:
            return "Lexem: type = " + self.lexem_type.name + ", value = '" + self.value + "', offset = " + str(self.offset)
