class ClassFix:
    def __init__(self, namespace, old_class_name, new_class_name):
        self.namespace = namespace
        self.old_class_name = old_class_name
        self.new_class_name = new_class_name

    def __str__(self):
        #return self.namespace + '.' + self.old_class_name + ' -> ' + self.namespace + '.' + self.new_class_name
        return self.old_class_name + ' -> ' + self.new_class_name