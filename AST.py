from enum import Enum, auto

class NodeType(Enum):
    SET = auto()
    ADD = auto()
    SUB = auto()
    MUL = auto()
    DIV = auto()
    POW = auto()
    FACT = auto()
    EXPR = auto()
    IN = auto()
    OUT = auto()
    MOD = auto()

class ASTNode:
    def print(self):
        raise NotImplementedError("Subclasses must implement print()")

class SetNode(ASTNode):
    def __init__(self, var_name, data_type, value):
        self.var_name = var_name
        self.data_type = data_type
        self.value = value
    
    def print(self):
        print(f"SET {self.var_name} {'NUMBER' if self.data_type == 'NUMBER' else 'STRING'} ({self.value})")

class ArithmeticNode(ASTNode):
    def __init__(self, var_name, op_type, params):
        self.var_name = var_name
        self.op_type = op_type
        self.params = params
    
    def print(self):
        print(f"Arithmetic {self.var_name} ({' '.join(self.params)})")

class FactorialNode(ASTNode):
    def __init__(self, var_name, number):
        self.var_name = var_name
        self.number = number
    
    def print(self):
        print(f"FACT {self.var_name} {self.number}")

class ExpressionNode(ASTNode):
    def __init__(self, var_name, expression):
        self.var_name = var_name
        self.expression = expression
    
    def print(self):
        print(f"EXPR {self.var_name} ({self.expression})")

class OutputNode(ASTNode):
    def __init__(self, var_name):
        self.var_name = var_name
    
    def print(self):
        print(f"OUT {self.var_name}")

class InputNode(ASTNode):
    def __init__(self, var_name, data_type):
        self.var_name = var_name
        self.data_type = data_type
    
    def print(self):
        print(f"INPUT {self.var_name} {'NUMBER' if self.data_type == 'NUMBER' else 'STRING'}")
