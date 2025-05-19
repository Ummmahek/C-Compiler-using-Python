import re
from enum import Enum, auto

class TokenType(Enum):
    SET = auto()
    ADD = auto()
    SUB = auto()
    MUL = auto()
    DIV = auto()
    MOD = auto()
    POW = auto()
    FACT = auto()
    EXPR = auto()
    IN = auto()
    OUT = auto()
    NUMBER = auto()
    STRING = auto()
    IDENTIFIER = auto()
    INTEGER = auto()
    STRING_LITERAL = auto()
    LPAREN = auto()
    RPAREN = auto()
    COMMA = auto()
    END_OF_FILE = auto()
    INVALID = auto()
    COMMENT = auto()

class Token:
    def __init__(self, token_type, value):
        self.type = token_type
        self.value = value
    
    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)})"

class Lexer:
    def __init__(self, source):
        self.source = source
        self.cur_pos = 0
        self.cur_char = self.source[self.cur_pos] if self.source else '\0'
        self.keywords = {
            "SET": TokenType.SET,
            "ADD": TokenType.ADD,
            "SUB": TokenType.SUB,
            "MUL": TokenType.MUL,
            "DIV": TokenType.DIV,
            "MOD": TokenType.MOD,
            "POW": TokenType.POW,
            "FACT": TokenType.FACT,
            "EXPR": TokenType.EXPR,
            "IN": TokenType.IN,
            "OUT": TokenType.OUT,
            "NUMBER": TokenType.NUMBER,
            "STRING": TokenType.STRING,
        }
    
    def advance(self):
        self.cur_pos += 1
        self.cur_char = self.source[self.cur_pos] if self.cur_pos < len(self.source) else '\0'
    
    def get_identifier(self):
        result = ''
        while self.cur_char.isalnum() or self.cur_char == '_':
            result += self.cur_char
            self.advance()
        return Token(self.keywords.get(result, TokenType.IDENTIFIER), result)
    
    def get_number(self):
        result = ''
        while self.cur_char.isdigit():
            result += self.cur_char
            self.advance()
        return Token(TokenType.INTEGER, result)
    
    def get_string(self):
        result = ''
        self.advance()
        while self.cur_char != '"' and self.cur_char != '\0':
            result += self.cur_char
            self.advance()
        if self.cur_char == '"':
            self.advance()
            return Token(TokenType.STRING_LITERAL, result)
        else:
            raise RuntimeError("Unterminated string")
    
    def get_next_token(self):
        while self.cur_char != '\0':
            if self.cur_char.isspace():
                self.advance()
                continue
            if self.cur_char == '#':
                while self.cur_char != '\n' and self.cur_char != '\0':
                    self.advance()
                return self.get_next_token()
            if self.cur_char.isalpha():
                return self.get_identifier()
            if self.cur_char.isdigit():
                return self.get_number()
            if self.cur_char == '"':
                return self.get_string()
            if self.cur_char == '(':
                self.advance()
                return Token(TokenType.LPAREN, '(')
            if self.cur_char == ')':
                self.advance()
                return Token(TokenType.RPAREN, ')')
            if self.cur_char == ',':
                self.advance()
                return Token(TokenType.COMMA, ',')
            raise RuntimeError(f"Unrecognized character '{self.cur_char}'")
        return Token(TokenType.END_OF_FILE, '')
