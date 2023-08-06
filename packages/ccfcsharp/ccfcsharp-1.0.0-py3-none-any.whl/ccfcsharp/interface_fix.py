class InterfaceFix:
    def __init__(self, namespace, old_name, new_name, message):
        self.namespace = namespace
        self.old_name = old_name
        self.new_name = new_name
        self.message = message

    def __str__(self):
        return self.namespace + '.' + self.old_name + ' -> ' + self.namespace + '.' + self.new_name