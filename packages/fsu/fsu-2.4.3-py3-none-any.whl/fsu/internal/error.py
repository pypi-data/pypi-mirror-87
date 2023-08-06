class ObjectNotExist(Exception):
    def __init__(self, obj):
        self.object = obj

class FieldNotExist(Exception):
    def __init__(self, obj, field):
        self.object = obj
        self.field  = field

class UnsupportedOperator(Exception):
    def __init__(self, op):
        self.op = op
