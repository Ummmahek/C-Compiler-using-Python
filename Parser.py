from Lexer import TokenType
from AST import *

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.cur_token = self.lexer.get_next_token()
    
    def advance(self):
        self.cur_token = self.lexer.get_next_token()
    
    def parse(self):
        statements = []
        while self.cur_token.type != TokenType.END_OF_FILE:
            statements.append(self.parse_statement())
        return statements
    
    def parse_statement(self):
        token_type = self.cur_token.type
        if token_type == TokenType.SET:
            return self.parse_set()
        if token_type in {TokenType.ADD, TokenType.SUB, TokenType.MUL, TokenType.DIV, TokenType.MOD, TokenType.POW}:
            return self.parse_arithmetic(NodeType[token_type.name])
        if token_type == TokenType.FACT:
            return self.parse_factorial()
        if token_type == TokenType.EXPR:
            return self.parse_expression()
        if token_type == TokenType.IN:
            return self.parse_input()
        if token_type == TokenType.OUT:
            return self.parse_output()
        raise SyntaxError(f"Unexpected token '{self.cur_token.value}'")
    
    def parse_factorial(self):
        self.advance()
        var_name = self.cur_token.value
        self.advance()
        if self.cur_token.type != TokenType.INTEGER:
            raise RuntimeError("Expected an integer for FACT.")
        number = int(self.cur_token.value)
        self.advance()
        return FactorialNode(var_name, number)
    
    def parse_expression(self):
        self.advance()
        var_name = self.cur_token.value
        self.advance()
        if self.cur_token.type != TokenType.LPAREN:
            raise RuntimeError("Expected '(' after EXPR variable.")
        self.advance()
        if self.cur_token.type != TokenType.STRING_LITERAL:
            raise RuntimeError("Expected expression inside double quotes.")
        expression = self.cur_token.value
        self.advance()
        if self.cur_token.type != TokenType.RPAREN:
            raise RuntimeError("Expected ')' after expression.")
        self.advance()
        return ExpressionNode(var_name, expression)
    
    def parse_set(self):
        self.advance()
        var_name = self.cur_token.value
        self.advance()
        if self.cur_token.type not in {TokenType.NUMBER, TokenType.STRING}:
            raise RuntimeError("Expected NUMBER or STRING keyword after variable name.")
        data_type = self.cur_token.type.name
        self.advance()
        if self.cur_token.type != TokenType.LPAREN:
            raise RuntimeError("Expected '(' after data type.")
        self.advance()
        value = self.cur_token.value
        self.advance()
        if self.cur_token.type != TokenType.RPAREN:
            raise RuntimeError("Expected ')' at the end of assignment.")
        self.advance()
        return SetNode(var_name, data_type, value)
    
    def parse_arithmetic(self, op_type):
        self.advance()
        var_name = self.cur_token.value
        self.advance()
        if self.cur_token.type != TokenType.LPAREN:
            raise SyntaxError("Expected '('")
        self.advance()
        params = []
        while self.cur_token.type != TokenType.RPAREN:
            if self.cur_token.type in {TokenType.IDENTIFIER, TokenType.INTEGER}:
                params.append(self.cur_token.value)
                self.advance()
            else:
                raise SyntaxError(f"Unexpected token '{self.cur_token.value}' in arithmetic operation.")
            if self.cur_token.type == TokenType.COMMA:
                self.advance()
        self.advance()
        return ArithmeticNode(var_name, op_type, params)
    
    def parse_output(self):
        self.advance()
        var_name = self.cur_token.value
        self.advance()
        return OutputNode(var_name)
    
    def parse_input(self):
        self.advance()
        var_name = self.cur_token.value
        self.advance()
        if self.cur_token.type not in {TokenType.NUMBER, TokenType.STRING}:
            raise RuntimeError("Expected NUMBER or STRING type for IN statement.")
        data_type = self.cur_token.type.name
        self.advance()
        return InputNode(var_name, data_type)
