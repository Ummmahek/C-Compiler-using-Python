import math
from collections import deque
from AST import *

def precedence(op):
    if op in ('+', '-'):
        return 1
    if op in ('*', '/'):
        return 2
    return 0

def apply_op(a, b, op):
    if op == '+': return a + b
    if op == '-': return a - b
    if op == '*': return a * b
    if op == '/': return a // b  # Integer division
    raise ValueError("Unsupported operator")

class Interpreter:
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table
    
    def get_numerical_value(self, param):
        if self.symbol_table.exists(param):
            val = self.symbol_table.get(param)
            if isinstance(val, int):
                return val
            raise RuntimeError(f"Variable '{param}' is not a NUMBER.")
        if not param.isdigit():
            raise RuntimeError(f"'{param}' is not a valid NUMBER.")
        return int(param)
    
    def evaluate_arithmetic(self, op_type, params):
        if len(params) < 2:
            raise RuntimeError("No parameters for arithmetic operation.")
        if op_type in ['DIV', 'MOD']:
            if len(params) > 2:
                raise RuntimeError(f"Too many parameters for {op_type} operation.")
        result = self.get_numerical_value(params[0])
        for param in params[1:]:
            num = self.get_numerical_value(param)
            if op_type == 'ADD':
                result += num
            elif op_type == 'SUB':
                result -= num
            elif op_type == 'MUL':
                result *= num
            elif op_type == 'DIV':
                if num == 0:
                    raise RuntimeError("Division by zero.")
                result //= num
            elif op_type == 'MOD':
                if num == 0:
                    raise RuntimeError("Modulus by zero.")
                result %= num
            elif op_type == 'POW':
                result = int(math.pow(result, num))
            else:
                raise RuntimeError("Unsupported arithmetic operation.")
        return result
    
    def evaluate_factorial(self, n):
        if n < 0:
            raise RuntimeError("Factorial of negative number is undefined.")
        return math.factorial(n)
    
    def evaluate_expression(self, tokens):
        values = deque()
        ops = deque()
        i = 0
        while i < len(tokens):
            if tokens[i] == ' ':
                i += 1
                continue
            elif tokens[i] == '(':
                ops.append(tokens[i])
            elif tokens[i].isdigit():
                val = 0
                while i < len(tokens) and tokens[i].isdigit():
                    val = (val * 10) + int(tokens[i])
                    i += 1
                values.append(val)
                i -= 1
            elif tokens[i] == ')':
                while ops and ops[-1] != '(':
                    val2 = values.pop()
                    val1 = values.pop()
                    op = ops.pop()
                    values.append(apply_op(val1, val2, op))
                ops.pop()
            else:
                while ops and precedence(ops[-1]) >= precedence(tokens[i]):
                    val2 = values.pop()
                    val1 = values.pop()
                    op = ops.pop()
                    values.append(apply_op(val1, val2, op))
                ops.append(tokens[i])
            i += 1
        while ops:
            val2 = values.pop()
            val1 = values.pop()
            op = ops.pop()
            values.append(apply_op(val1, val2, op))
        return values.pop()
    
    def execute(self, node):
        if isinstance(node, SetNode):
            value = node.value
            if node.data_type == 'NUMBER':
                if not value.isdigit():
                    raise RuntimeError(f"'{value}' is not a valid NUMBER.")
                self.symbol_table.set(node.var_name, int(value))
            elif node.data_type == 'STRING':
                self.symbol_table.set(node.var_name, value)
        elif isinstance(node, ArithmeticNode):
            result = self.evaluate_arithmetic(node.op_type.name, node.params)
            self.symbol_table.set(node.var_name, result)
        elif isinstance(node, OutputNode):
            val = self.symbol_table.get(node.var_name)
            print(f"{node.var_name} = {val}")
        elif isinstance(node, FactorialNode):
            result = self.evaluate_factorial(node.number)
            self.symbol_table.set(node.var_name, result)
        elif isinstance(node, ExpressionNode):
            result = self.evaluate_expression(node.expression)
            self.symbol_table.set(node.var_name, result)
        elif isinstance(node, InputNode):
            user_input = input(f"Enter value for {node.var_name}: ")
            if node.data_type == 'NUMBER':
                if not user_input.isdigit():
                    raise RuntimeError(f"Invalid input. Expected NUMBER but received '{user_input}'.")
                self.symbol_table.set(node.var_name, int(user_input))
            else:
                self.symbol_table.set(node.var_name, user_input)
